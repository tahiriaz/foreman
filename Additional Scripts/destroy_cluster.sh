#!/bin/bash
#
# ============================================================================
# Pacemaker / Corosync Cluster Destruction and Recovery
# ============================================================================
#
# RHEL 8.10 / PCS
#
# Purpose:
#   - Automatically detect the current cluster name
#   - Automatically detect cluster nodes
#   - Use COROSYNC ring1 addresses for node access
#   - Back up cluster configuration
#   - Stop Pacemaker / Corosync on every detected node
#   - Destroy PCS configuration
#   - Remove Corosync configuration
#   - Remove local Pacemaker CIB
#   - Keep pcsd installed, enabled and running
#   - Verify all nodes after cleanup
#
# IMPORTANT:
#   This is a DESTRUCTIVE operation.
#
#   Node communication for this script uses:
#
#       ring1_addr
#
#   Expected network:
#
#       10.101.28.X
#
#   The script will NOT fall back to ring0_addr.
#
# ============================================================================

set -Eeuo pipefail

# ============================================================================
# 1. GLOBAL VARIABLES
# ============================================================================

CLUSTER=""
BACKUP=""
STAMP=$(date +%Y%m%d-%H%M%S)

KNOWN_HOSTS="/root/.ssh/known_hosts"
COROSYNC_CONF="/etc/corosync/corosync.conf"

declare -a NODE_NAMES=()
declare -a NODE_IPS=()

declare -a REACHABLE=()
declare -a UNREACHABLE=()

declare -a BACKUP_FAILURES=()
declare -a STOP_FAILURES=()
declare -a DESTROY_FAILURES=()
declare -a CLEANUP_FAILURES=()
declare -a VERIFY_FAILURES=()

SSH_OPTS=(
    -o ConnectTimeout=15
    -o ConnectionAttempts=2
    -o ServerAliveInterval=10
    -o ServerAliveCountMax=2
    -o StrictHostKeyChecking=accept-new
    -o UserKnownHostsFile="$KNOWN_HOSTS"
    -o PreferredAuthentications=password,keyboard-interactive
    -o PubkeyAuthentication=yes
    -o LogLevel=ERROR
)

# ============================================================================
# 2. FUNCTIONS
# ============================================================================

die()
{
    echo
    echo "ERROR: $*" >&2
    exit 1
}

log()
{
    echo
    echo "[$(date '+%F %T')] $*"
}

separator()
{
    echo
    echo "=================================================="
}

# ============================================================================
# 3. REQUIREMENTS
# ============================================================================

[[ $EUID -eq 0 ]] ||
    die "Run this script as root."

command -v pcs >/dev/null 2>&1 ||
    die "pcs command not found."

command -v ssh >/dev/null 2>&1 ||
    die "ssh command not found."

command -v sshpass >/dev/null 2>&1 ||
    die "sshpass is required. Install it first."

command -v timeout >/dev/null 2>&1 ||
    die "timeout command not found."

command -v awk >/dev/null 2>&1 ||
    die "awk command not found."

command -v getent >/dev/null 2>&1 ||
    die "getent command not found."

mkdir -p /root/.ssh
chmod 700 /root/.ssh

touch "$KNOWN_HOSTS"
chmod 600 "$KNOWN_HOSTS"

# ============================================================================
# 4. DETECT CLUSTER NAME
# ============================================================================

log "Detecting cluster name"

PCS_CLUSTER_NAME=""

# --------------------------------------------------------------------------
# Method 1: pcs config
# --------------------------------------------------------------------------

if pcs config >/tmp/pcs-config-detect.$$ 2>/dev/null; then

    PCS_CLUSTER_NAME=$(
        awk -F': ' '
            BEGIN { IGNORECASE=1 }
            /^Cluster Name:/ {
                print $2
                exit
            }
        ' /tmp/pcs-config-detect.$$
    )

fi

rm -f /tmp/pcs-config-detect.$$

# --------------------------------------------------------------------------
# Method 2: pcs status
# --------------------------------------------------------------------------

if [[ -z "$PCS_CLUSTER_NAME" ]]; then

    PCS_CLUSTER_NAME=$(
        pcs status --full 2>/dev/null |
        awk -F': ' '
            BEGIN { IGNORECASE=1 }
            /^Cluster name:/ {
                print $2
                exit
            }
        '
    )

fi

# --------------------------------------------------------------------------
# Method 3: corosync.conf
# --------------------------------------------------------------------------

if [[ -z "$PCS_CLUSTER_NAME" && -f "$COROSYNC_CONF" ]]; then

    PCS_CLUSTER_NAME=$(
        awk '
            BEGIN {
                IGNORECASE=1
            }

            /^[[:space:]]*cluster_name[[:space:]]*:/ {
                line=$0
                sub(/^[^:]*:[[:space:]]*/, "", line)
                gsub(/[";]/, "", line)
                gsub(/^[[:space:]]+|[[:space:]]+$/, "", line)
                print line
                exit
            }
        ' "$COROSYNC_CONF"
    )

fi

CLUSTER="${PCS_CLUSTER_NAME:-}"

[[ -n "$CLUSTER" ]] ||
    die "Unable to automatically determine the cluster name."

echo
echo "Detected cluster:"
echo
echo "    $CLUSTER"

# ============================================================================
# 5. VERIFY COROSYNC CONFIGURATION
# ============================================================================

[[ -f "$COROSYNC_CONF" ]] ||
    die "Cannot detect cluster nodes because $COROSYNC_CONF does not exist."

# ============================================================================
# 6. DETECT NODES USING ring1_addr
# ============================================================================

log "Detecting cluster nodes using ring1_addr"

echo
echo "The script will use ring1 addresses only."
echo "Expected ring1 network: 10.101.28.X"
echo

TMP_NODE_FILE=$(mktemp)

#
# Parse Corosync node blocks.
#
# Expected structure:
#
# nodelist {
#
#     node {
#         ring0_addr: 10.x.x.x
#         ring1_addr: 10.101.28.x
#         nodeid: 1
#     }
#
#     node {
#         ring0_addr: 10.x.x.x
#         ring1_addr: 10.101.28.x
#         nodeid: 2
#     }
#
# }
#
awk '
    /nodelist[[:space:]]*\{/ {
        in_nodelist=1
    }

    in_nodelist && /node[[:space:]]*\{/ {

        in_node=1
        name=""
        ring1=""
    }

    in_node && /name[[:space:]]*:/ {

        line=$0
        sub(/^[^:]*:[[:space:]]*/, "", line)
        gsub(/[;"[:space:]]/, "", line)

        name=line
    }

    in_node && /ring1_addr[[:space:]]*:/ {

        line=$0
        sub(/^[^:]*:[[:space:]]*/, "", line)
        gsub(/[;"[:space:]]/, "", line)

        ring1=line
    }

    in_node && /^[[:space:]]*}[[:space:]]*$/ {

        if (ring1 != "") {

            if (name == "")
                name=ring1

            print name "|" ring1
        }

        in_node=0
    }
' "$COROSYNC_CONF" > "$TMP_NODE_FILE"

#
# If no node blocks were parsed, try a simpler parser.
#
if [[ ! -s "$TMP_NODE_FILE" ]]; then

    awk '
        /ring1_addr[[:space:]]*:/ {

            line=$0
            sub(/^[^:]*:[[:space:]]*/, "", line)
            gsub(/[;"[:space:]]/, "", line)

            print line "|" line
        }
    ' "$COROSYNC_CONF" > "$TMP_NODE_FILE"

fi

while IFS='|' read -r name addr; do

    [[ -n "${name:-}" ]] || continue
    [[ -n "${addr:-}" ]] || continue

    NODE_NAMES+=("$name")
    NODE_IPS+=("$addr")

done < "$TMP_NODE_FILE"

rm -f "$TMP_NODE_FILE"

(( ${#NODE_NAMES[@]} > 0 )) ||
    die "No ring1_addr entries were found in $COROSYNC_CONF."

# ============================================================================
# 7. VALIDATE ring1 ADDRESSES
# ============================================================================

log "Validating ring1 addresses"

for ((i=0; i<${#NODE_IPS[@]}; i++)); do

    name="${NODE_NAMES[i]}"
    addr="${NODE_IPS[i]}"

    #
    # The requested network is 10.101.28.X.
    #
    if [[ "$addr" =~ ^10\.101\.28\.[0-9]{1,3}$ ]]; then

        continue

    fi

    #
    # If Corosync contains a hostname instead of an IP,
    # resolve it.
    #
    if [[ "$addr" =~ ^[a-zA-Z0-9._-]+$ ]]; then

        RESOLVED_IP=$(
            getent ahostsv4 "$addr" 2>/dev/null |
            awk 'NR==1 {print $1}'
        )

        if [[ -z "$RESOLVED_IP" ]]; then

            die "Unable to resolve ring1 address '$addr' for node '$name'."

        fi

        if [[ ! "$RESOLVED_IP" =~ ^10\.101\.28\.[0-9]{1,3}$ ]]; then

            die "ring1 address for '$name' resolves to $RESOLVED_IP, not 10.101.28.X."

        fi

        NODE_IPS[i]="$RESOLVED_IP"

        continue

    fi

    die "Invalid ring1 address '$addr' for node '$name'. Expected 10.101.28.X."

done

# ============================================================================
# 8. DISPLAY DETECTED CLUSTER
# ============================================================================

separator
echo "AUTOMATIC CLUSTER DISCOVERY"
separator

echo
echo "Cluster:"
echo
echo "    $CLUSTER"

echo
echo "Communication network:"
echo
echo "    Corosync ring1"
echo "    10.101.28.X"

echo
echo "Nodes detected:"
echo

for ((i=0; i<${#NODE_NAMES[@]}; i++)); do

    printf "    %-30s %s\n" \
        "${NODE_NAMES[i]}" \
        "${NODE_IPS[i]}"

done

echo
echo "Source:"
echo
echo "    $COROSYNC_CONF"

# ============================================================================
# 9. CHECK DUPLICATE NODE NAMES
# ============================================================================

for ((i=0; i<${#NODE_NAMES[@]}; i++)); do

    for ((j=i+1; j<${#NODE_NAMES[@]}; j++)); do

        [[ "${NODE_NAMES[i]}" != "${NODE_NAMES[j]}" ]] ||
            die "Duplicate node name detected: ${NODE_NAMES[i]}"

    done

done

# ============================================================================
# 10. CHECK DUPLICATE IP ADDRESSES
# ============================================================================

for ((i=0; i<${#NODE_IPS[@]}; i++)); do

    for ((j=i+1; j<${#NODE_IPS[@]}; j++)); do

        [[ "${NODE_IPS[i]}" != "${NODE_IPS[j]}" ]] ||
            die "Duplicate ring1 IP detected: ${NODE_IPS[i]}"

    done

done

# ============================================================================
# 11. CONFIRM CLUSTER
# ============================================================================

echo
echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
echo "WARNING: DESTRUCTIVE OPERATION"
echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
echo
echo "The following cluster will be destroyed:"
echo
echo "    $CLUSTER"
echo
echo "Communication network:"
echo
echo "    ring1 / 10.101.28.X"
echo
echo "Detected nodes:"
echo

for ((i=0; i<${#NODE_NAMES[@]}; i++)); do

    printf "    %-30s %s\n" \
        "${NODE_NAMES[i]}" \
        "${NODE_IPS[i]}"

done

echo
echo "The following will be removed from every reachable node:"
echo
echo "    Pacemaker cluster configuration"
echo "    Corosync configuration"
echo "    Corosync authkey"
echo "    Local Pacemaker CIB"
echo
echo "The following will NOT be removed:"
echo
echo "    Application data"
echo "    NFS data"
echo "    Network configuration"
echo "    PCS packages"
echo "    pcsd"
echo

read -r -p "Type the detected cluster name [$CLUSTER]: " ANSWER

[[ "$ANSWER" == "$CLUSTER" ]] ||
    die "Cluster name confirmation failed."

echo

read -r -p "Type DESTROY to continue: " ANSWER

[[ "$ANSWER" == "DESTROY" ]] ||
    die "Cancelled."

# ============================================================================
# 12. CREATE BACKUP DIRECTORY
# ============================================================================

BACKUP="/root/cluster-reset-${CLUSTER}-${STAMP}"

mkdir -p "$BACKUP"
chmod 700 "$BACKUP"

printf '%s\n' "$CLUSTER" > "$BACKUP/cluster-name.txt"

cp -a "$COROSYNC_CONF" \
    "$BACKUP/corosync.conf.original" \
    2>/dev/null || true

cp -a "$KNOWN_HOSTS" \
    "$BACKUP/known_hosts" \
    2>/dev/null || true

#
# Save detected inventory.
#
{
    echo "# Automatically detected cluster inventory"
    echo "# Cluster: $CLUSTER"
    echo "# Network: Corosync ring1"
    echo "# Network range: 10.101.28.X"
    echo "# Generated: $(date)"
    echo

    for ((i=0; i<${#NODE_NAMES[@]}; i++)); do
        echo "${NODE_NAMES[i]} ${NODE_IPS[i]}"
    done

} > "$BACKUP/detected-inventory.txt"

echo
echo "Backup directory:"
echo
echo "    $BACKUP"

# ============================================================================
# 13. SSH PASSWORD
# ============================================================================

echo
echo "Enter the root SSH password for the cluster nodes."
echo "The password is requested once."

read -r -s -p "Root SSH password: " SSHPASS
echo

[[ -n "$SSHPASS" ]] ||
    die "Empty password."

export SSHPASS

# ============================================================================
# 14. SSH FUNCTION
# ============================================================================

ssh_run()
{
    local ip="$1"
    shift

    timeout 120 \
        sshpass -e ssh \
        "${SSH_OPTS[@]}" \
        "root@${ip}" "$@"
}

# ============================================================================
# 15. PRE-FLIGHT CONNECTIVITY
# ============================================================================

log "Checking connectivity to all detected ring1 addresses"

for ((i=0; i<${#NODE_IPS[@]}; i++)); do

    ip="${NODE_IPS[i]}"
    name="${NODE_NAMES[i]}"

    echo
    echo "Checking $name ($ip)"

    if ssh_run "$ip" "hostname -f"; then

        REACHABLE+=("$ip")

    else

        echo "WARNING: $name is unreachable through ring1 address $ip."
        UNREACHABLE+=("$ip")

    fi

done

separator
echo "CONNECTIVITY SUMMARY"
separator

echo
echo "Detected nodes:   ${#NODE_IPS[@]}"
echo "Reachable nodes:  ${#REACHABLE[@]}"
echo "Unreachable:      ${#UNREACHABLE[@]}"

if (( ${#UNREACHABLE[@]} > 0 )); then

    echo
    echo "WARNING: Some cluster nodes are unreachable through ring1."

    for ip in "${UNREACHABLE[@]}"; do
        echo "    $ip"
    done

    echo
    echo "Those nodes will NOT be modified."

fi

(( ${#REACHABLE[@]} > 0 )) ||
    die "No cluster nodes are reachable through ring1. Nothing was changed."

# ============================================================================
# 16. BACKUP ALL REACHABLE NODES
# ============================================================================

log "Creating backups on all reachable nodes"

for ((i=0; i<${#NODE_IPS[@]}; i++)); do

    ip="${NODE_IPS[i]}"
    name="${NODE_NAMES[i]}"

    #
    # Skip unreachable nodes.
    #
    if [[ ! " ${REACHABLE[*]} " =~ " ${ip} " ]]; then
        continue
    fi

    echo
    echo "===== BACKUP: $name ($ip) ====="

    REMOTE_BACKUP_DIR="$BACKUP/$name"

    if ! ssh_run "$ip" \
        "mkdir -p '$REMOTE_BACKUP_DIR' && chmod 700 '$REMOTE_BACKUP_DIR'"; then

        echo "WARNING: Could not create backup directory on $name"
        BACKUP_FAILURES+=("$ip")
        continue

    fi

    if ssh_run "$ip" "bash -s" <<REMOTE_BACKUP
set +e

DEST='$REMOTE_BACKUP_DIR'

mkdir -p "\$DEST"

echo "===== DATE =====" > "\$DEST/backup-info.txt"
date >> "\$DEST/backup-info.txt"

echo >> "\$DEST/backup-info.txt"
echo "===== HOSTNAME =====" >> "\$DEST/backup-info.txt"
hostname -f >> "\$DEST/backup-info.txt" 2>&1

echo >> "\$DEST/backup-info.txt"
echo "===== PCS STATUS =====" >> "\$DEST/backup-info.txt"
pcs status --full >> "\$DEST/backup-info.txt" 2>&1

echo >> "\$DEST/backup-info.txt"
echo "===== PCS CONFIG =====" >> "\$DEST/backup-info.txt"
pcs config >> "\$DEST/backup-info.txt" 2>&1

echo >> "\$DEST/backup-info.txt"
echo "===== PCS CONSTRAINTS =====" >> "\$DEST/backup-info.txt"
pcs constraint config >> "\$DEST/backup-info.txt" 2>&1

echo >> "\$DEST/backup-info.txt"
echo "===== PCS RESOURCES =====" >> "\$DEST/backup-info.txt"
pcs resource config >> "\$DEST/backup-info.txt" 2>&1

echo >> "\$DEST/backup-info.txt"
echo "===== PCS STONITH =====" >> "\$DEST/backup-info.txt"
pcs stonith config >> "\$DEST/backup-info.txt" 2>&1

echo >> "\$DEST/backup-info.txt"
echo "===== SERVICE STATUS =====" >> "\$DEST/backup-info.txt"
systemctl status corosync pacemaker pcsd >> "\$DEST/backup-info.txt" 2>&1

echo >> "\$DEST/backup-info.txt"
echo "===== SERVICE ENABLED =====" >> "\$DEST/backup-info.txt"
systemctl is-enabled corosync pacemaker pcsd >> "\$DEST/backup-info.txt" 2>&1

#
# Backup Corosync configuration.
#
if test -e /etc/corosync/corosync.conf; then
    cp -a /etc/corosync/corosync.conf "\$DEST/"
fi

#
# Backup complete Corosync directory.
#
if test -d /etc/corosync; then
    cp -a /etc/corosync "\$DEST/corosync-directory"
fi

#
# Backup Pacemaker CIB.
#
if test -d /var/lib/pacemaker/cib; then
    cp -a /var/lib/pacemaker/cib "\$DEST/"
fi

#
# Backup PCS data.
#
if test -d /var/lib/pcsd; then
    cp -a /var/lib/pcsd "\$DEST/pcsd-directory"
fi

exit 0
REMOTE_BACKUP
    then

        echo "Backup completed on $name"

    else

        echo "WARNING: Backup failed on $name"
        BACKUP_FAILURES+=("$ip")

    fi

done

# ============================================================================
# 17. STOP CLUSTER SERVICES
# ============================================================================

log "Stopping Pacemaker and Corosync on reachable nodes"

for ip in "${REACHABLE[@]}"; do

    echo
    echo "===== STOPPING CLUSTER SERVICES: $ip ====="

    if ssh_run "$ip" "bash -s" <<'REMOTE_STOP'
set +e

echo "Stopping Pacemaker using PCS..."
pcs cluster stop 2>/dev/null

echo "Stopping Pacemaker service..."
systemctl stop pacemaker

echo "Stopping Corosync service..."
systemctl stop corosync

#
# Wait for services to stop.
#
for i in {1..15}; do

    PACEMAKER_ACTIVE=0
    COROSYNC_ACTIVE=0

    systemctl is-active --quiet pacemaker && PACEMAKER_ACTIVE=1
    systemctl is-active --quiet corosync && COROSYNC_ACTIVE=1

    if (( PACEMAKER_ACTIVE == 0 && COROSYNC_ACTIVE == 0 )); then
        break
    fi

    sleep 2

done

if systemctl is-active --quiet pacemaker; then
    echo "FAIL: Pacemaker is still active"
    exit 1
fi

if systemctl is-active --quiet corosync; then
    echo "FAIL: Corosync is still active"
    exit 1
fi

echo "PASS: Pacemaker and Corosync stopped"

exit 0
REMOTE_STOP
    then

        echo "Cluster services stopped on $ip"

    else

        echo "WARNING: Failed to stop cluster services on $ip"
        STOP_FAILURES+=("$ip")

    fi

done

# ============================================================================
# 18. DESTROY PCS CONFIGURATION
# ============================================================================

log "Destroying PCS configuration"

for ip in "${REACHABLE[@]}"; do

    echo
    echo "===== DESTROY PCS: $ip ====="

    if ssh_run "$ip" "bash -s" <<'REMOTE_DESTROY'
set +e

#
# Try standard PCS destruction.
#
pcs cluster destroy

PCS_RC=$?

echo
echo "pcs cluster destroy exit code: $PCS_RC"

#
# Ensure cluster services are stopped.
#
systemctl stop pacemaker
systemctl stop corosync

#
# Disable automatic startup.
#
systemctl disable pacemaker
systemctl disable corosync

#
# Backup and remove Corosync configuration.
#
if test -e /etc/corosync/corosync.conf; then

    cp -a /etc/corosync/corosync.conf \
        "/root/corosync.conf.pre-reset.$(date +%Y%m%d-%H%M%S)"

    rm -f /etc/corosync/corosync.conf

fi

#
# Backup and remove Corosync authkey.
#
if test -e /etc/corosync/authkey; then

    cp -a /etc/corosync/authkey \
        "/root/corosync-authkey.pre-reset.$(date +%Y%m%d-%H%M%S)"

    rm -f /etc/corosync/authkey

fi

#
# Move Pacemaker CIB instead of deleting it.
#
if test -d /var/lib/pacemaker/cib; then

    mv /var/lib/pacemaker/cib \
       "/var/lib/pacemaker/cib.pre-reset.$(date +%Y%m%d-%H%M%S)"

fi

#
# Stop services again.
#
systemctl stop pacemaker
systemctl stop corosync

#
# Keep pcsd available for future cluster creation.
#
systemctl enable pcsd
systemctl restart pcsd

#
# Verify.
#
if systemctl is-active --quiet pacemaker; then

    echo "FAIL: Pacemaker is still active"
    exit 1

fi

if systemctl is-active --quiet corosync; then

    echo "FAIL: Corosync is still active"
    exit 1

fi

if test -e /etc/corosync/corosync.conf; then

    echo "FAIL: corosync.conf still exists"
    exit 1

fi

echo
echo "PASS: PCS destruction completed"

exit 0
REMOTE_DESTROY
    then

        echo "PCS destruction completed on $ip"

    else

        echo "WARNING: PCS destruction failed on $ip"
        DESTROY_FAILURES+=("$ip")

    fi

done

# ============================================================================
# 19. FINAL SERVICE CLEANUP
# ============================================================================

log "Applying final service cleanup"

for ip in "${REACHABLE[@]}"; do

    echo
    echo "===== FINAL CLEANUP: $ip ====="

    if ssh_run "$ip" "bash -s" <<'REMOTE_FINAL'
set +e

systemctl stop pacemaker
systemctl stop corosync

systemctl disable pacemaker
systemctl disable corosync

systemctl enable pcsd
systemctl start pcsd

#
# Final service checks.
#

if systemctl is-active --quiet pacemaker; then

    echo "FAIL: Pacemaker active"
    exit 1

fi

if systemctl is-active --quiet corosync; then

    echo "FAIL: Corosync active"
    exit 1

fi

if ! systemctl is-active --quiet pcsd; then

    echo "FAIL: pcsd inactive"
    exit 1

fi

if ! systemctl is-enabled --quiet pcsd; then

    echo "FAIL: pcsd not enabled"
    exit 1

fi

echo "PASS: Final service state correct"

exit 0
REMOTE_FINAL
    then

        echo "Final cleanup completed on $ip"

    else

        echo "WARNING: Final cleanup failed on $ip"
        CLEANUP_FAILURES+=("$ip")

    fi

done

# ============================================================================
# 20. FINAL VERIFICATION
# ============================================================================

log "Final verification"

for ((i=0; i<${#NODE_IPS[@]}; i++)); do

    ip="${NODE_IPS[i]}"
    name="${NODE_NAMES[i]}"

    #
    # Unreachable nodes cannot be verified.
    #
    if [[ ! " ${REACHABLE[*]} " =~ " ${ip} " ]]; then

        VERIFY_FAILURES+=("$ip")
        continue

    fi

    separator
    echo "FINAL VERIFICATION"
    echo "Node: $name"
    echo "Ring1: $ip"
    separator

    if ssh_run "$ip" "bash -s" <<'REMOTE_VERIFY'
set +e

FAILED=0

echo
echo "--- Service status ---"

for svc in pacemaker corosync pcsd; do

    printf "%-12s " "$svc"
    systemctl is-active "$svc"

done

echo
echo "--- Service enabled state ---"

for svc in pacemaker corosync pcsd; do

    printf "%-12s " "$svc"
    systemctl is-enabled "$svc"

done

echo
echo "--- Corosync configuration ---"

if test -e /etc/corosync/corosync.conf; then

    echo "FAIL: /etc/corosync/corosync.conf exists"
    FAILED=1

else

    echo "PASS: corosync.conf absent"

fi

echo
echo "--- Corosync process ---"

if pgrep -a -x corosync; then

    echo "FAIL: corosync process exists"
    FAILED=1

else

    echo "PASS: no corosync process"

fi

echo
echo "--- Pacemaker process ---"

if pgrep -a -x pacemakerd; then

    echo "FAIL: pacemakerd process exists"
    FAILED=1

else

    echo "PASS: no pacemakerd process"

fi

echo
echo "--- Pacemaker service ---"

if systemctl is-active --quiet pacemaker; then

    echo "FAIL: pacemaker active"
    FAILED=1

else

    echo "PASS: pacemaker inactive"

fi

echo
echo "--- Corosync service ---"

if systemctl is-active --quiet corosync; then

    echo "FAIL: corosync active"
    FAILED=1

else

    echo "PASS: corosync inactive"

fi

echo
echo "--- pcsd service ---"

if systemctl is-active --quiet pcsd &&
   systemctl is-enabled --quiet pcsd; then

    echo "PASS: pcsd active and enabled"

else

    echo "FAIL: pcsd is not active and enabled"
    FAILED=1

fi

echo
echo "--- Pacemaker enabled state ---"

if systemctl is-enabled --quiet pacemaker; then

    echo "FAIL: pacemaker still enabled"
    FAILED=1

else

    echo "PASS: pacemaker disabled"

fi

echo
echo "--- Corosync enabled state ---"

if systemctl is-enabled --quiet corosync; then

    echo "FAIL: corosync still enabled"
    FAILED=1

else

    echo "PASS: corosync disabled"

fi

if (( FAILED != 0 )); then

    echo
    echo "RESULT: FAIL"
    exit 1

fi

echo
echo "RESULT: PASS"

exit 0
REMOTE_VERIFY
    then

        echo
        echo "PASS: $name"

    else

        echo
        echo "FAIL: $name"
        VERIFY_FAILURES+=("$ip")

    fi

done

# ============================================================================
# 21. SUMMARY
# ============================================================================

unset SSHPASS

separator
echo "CLUSTER RESET SUMMARY"
separator

echo
echo "Cluster:               $CLUSTER"
echo "Address source:        ring1_addr"
echo "Ring1 network:         10.101.28.X"
echo "Detected nodes:        ${#NODE_IPS[@]}"
echo "Reachable nodes:       ${#REACHABLE[@]}"
echo "Unreachable nodes:     ${#UNREACHABLE[@]}"
echo "Backup failures:       ${#BACKUP_FAILURES[@]}"
echo "Stop failures:         ${#STOP_FAILURES[@]}"
echo "Destroy failures:      ${#DESTROY_FAILURES[@]}"
echo "Cleanup failures:      ${#CLEANUP_FAILURES[@]}"
echo "Verification failures: ${#VERIFY_FAILURES[@]}"
echo
echo "Backup:"
echo "    $BACKUP"
echo

if (( ${#UNREACHABLE[@]} > 0 )); then

    echo "Unreachable nodes:"
    printf '    %s\n' "${UNREACHABLE[@]}"
    echo

fi

if (( ${#VERIFY_FAILURES[@]} > 0 )); then

    echo "Nodes requiring manual recovery:"
    printf '    %s\n' "${VERIFY_FAILURES[@]}"
    echo

fi

if (( ${#BACKUP_FAILURES[@]} > 0 )); then

    echo "Backup failures:"
    printf '    %s\n' "${BACKUP_FAILURES[@]}"
    echo

fi

if (( ${#STOP_FAILURES[@]} > 0 )); then

    echo "Stop failures:"
    printf '    %s\n' "${STOP_FAILURES[@]}"
    echo

fi

if (( ${#DESTROY_FAILURES[@]} > 0 )); then

    echo "Destroy failures:"
    printf '    %s\n' "${DESTROY_FAILURES[@]}"
    echo

fi

if (( ${#CLEANUP_FAILURES[@]} > 0 )); then

    echo "Cleanup failures:"
    printf '    %s\n' "${CLEANUP_FAILURES[@]}"
    echo

fi

# ============================================================================
# 22. FINAL RESULT
# ============================================================================

if (( ${#UNREACHABLE[@]} > 0 ||
      ${#VERIFY_FAILURES[@]} > 0 ||
      ${#BACKUP_FAILURES[@]} > 0 ||
      ${#STOP_FAILURES[@]} > 0 ||
      ${#DESTROY_FAILURES[@]} > 0 ||
      ${#CLEANUP_FAILURES[@]} > 0 )); then

    echo "=================================================="
    echo "RESULT: INCOMPLETE"
    echo "=================================================="
    echo
    echo "Do NOT create the new cluster until the failed"
    echo "nodes have been manually reviewed."
    echo
    exit 1

fi

echo "=================================================="
echo "RESULT: RESET COMPLETED"
echo "=================================================="
echo
echo "Cluster: $CLUSTER"
echo
echo "Address source:"
echo "    ring1_addr"
echo "    10.101.28.X"
echo
echo "Pacemaker:"
echo "    stopped and disabled"
echo
echo "Corosync:"
echo "    stopped and disabled"
echo "    configuration removed"
echo
echo "pcsd:"
echo "    active and enabled"
echo
echo "Backup:"
echo "    $BACKUP"
echo
echo "All detected nodes passed verification."
echo
echo "The nodes are ready for fresh cluster setup."
echo "=================================================="

exit 0