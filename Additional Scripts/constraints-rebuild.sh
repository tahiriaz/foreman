#!/bin/bash
#
# ============================================================================
# Pacemaker Constraint Rebuild Script
# ============================================================================
#
# Purpose:
#   1. Discover NVR resources and groups from the live CIB.
#   2. Validate all discovered resources before modifying constraints.
#   3. Back up the CIB.
#   4. Delete all existing constraints.
#   5. Rebuild NVR placement, isolation, and Picata/NFS dependencies.
#
# Requirements:
#   - RHEL 8 / Python 3.6+
#   - pcs, cibadmin, Python 3
#   - Run as root on a Pacemaker cluster node.
#
# Resource naming conventions derived from the supplied configuration:
#   <cluster>-vip
#   <cluster>-nfsrecNN
#   <cluster>-picataNN
#   <cluster>-pctcfg-updater
#   rg-<cluster>-core
#
# IMPORTANT:
#   This script deletes ALL constraints in the cluster, including constraints
#   unrelated to NVR services. Review this before running in production.
#
# ============================================================================

set -Eeuo pipefail
umask 077

SCRIPT_NAME="$(basename "$0")"
LOG_FILE="/var/log/constraints-rebuild.log"
BACKUP_DIR="/root/cib-backups"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP_FILE="${BACKUP_DIR}/cib-before-constraints-${TIMESTAMP}.xml"

AUTO_CONFIRM="${AUTO_CONFIRM:-NO}"

mkdir -p "$BACKUP_DIR"
touch "$LOG_FILE"
chmod 600 "$LOG_FILE"

exec > >(tee -a "$LOG_FILE") 2>&1

log() {
    printf '[%s] %s\n' "$(date '+%F %T')" "$*"
}

die() {
    log "ERROR: $*"
    exit 1
}

for cmd in pcs cibadmin python3; do
    command -v "$cmd" >/dev/null 2>&1 ||
        die "Required command not found: $cmd"
done

[[ $EUID -eq 0 ]] || die "Run this script as root."

log "============================================================"
log "Pacemaker NVR constraint rebuild"
log "============================================================"

# ---------------------------------------------------------------------------
# 1. Capture and validate the live CIB
# ---------------------------------------------------------------------------

CIB_XML="$(mktemp /tmp/nvr-cib.XXXXXX.xml)"
trap 'rm -f "$CIB_XML"' EXIT

cibadmin --query > "$CIB_XML" ||
    die "Could not retrieve the live CIB."

[[ -s "$CIB_XML" ]] || die "The retrieved CIB is empty."

# ---------------------------------------------------------------------------
# 2. Discover and validate resources using Python 3.6-compatible syntax
#
# Output format:
#   cluster|vip|core_group|nfsrec1,nfsrec2,...|picata1,picata2,...|updater
#
# Discovery is based on actual resource IDs and resource agent definitions.
# Resource IDs are not individually hardcoded.
# ---------------------------------------------------------------------------

DISCOVERY_FILE="$(mktemp /tmp/nvr-discovery.XXXXXX)"
trap 'rm -f "$CIB_XML" "$DISCOVERY_FILE"' EXIT

python3 - "$CIB_XML" "$DISCOVERY_FILE" <<'PYTHON'
from __future__ import print_function

import re
import sys
import xml.etree.ElementTree as ET

cib_path = sys.argv[1]
output_path = sys.argv[2]

try:
    root = ET.parse(cib_path).getroot()
except Exception as exc:
    sys.stderr.write("Cannot parse CIB XML: %s\n" % exc)
    sys.exit(1)

resources_root = root.find("./configuration/resources")

if resources_root is None:
    sys.stderr.write("CIB has no configuration/resources section.\n")
    sys.exit(1)

# Map primitive IDs to their primitive XML element and parent group.
primitives = {}
groups = {}

def walk_resources(parent, parent_group=None):
    for child in list(parent):
        tag = child.tag.split("}")[-1]

        if tag == "group":
            gid = child.get("id")
            if not gid:
                continue

            groups[gid] = child
            walk_resources(child, gid)

        elif tag == "clone" or tag == "master":
            # Discover primitives inside wrappers as well, but retain the
            # wrapper's existence. These are not automatically considered
            # direct members of a CORE group.
            walk_resources(child, parent_group)

        elif tag == "primitive":
            rid = child.get("id")
            if rid:
                primitives[rid] = {
                    "xml": child,
                    "group": parent_group
                }

walk_resources(resources_root)

def primitive_agent(primitive):
    meta = primitive.find("meta_attributes")
    return (
        primitive.get("class", ""),
        primitive.get("provider", ""),
        primitive.get("type", "")
    )

def get_clusters():
    result = set()

    for rid, info in primitives.items():
        if not rid.endswith("-vip"):
            continue

        cls, provider, agent = primitive_agent(info["xml"])

        if cls == "ocf" and provider == "heartbeat" and agent == "IPaddr2":
            cluster = rid[:-4]

            if re.match(r"^clnvrm[0-9]+$", cluster):
                result.add(cluster)

    return sorted(result)

clusters = get_clusters()

if not clusters:
    sys.stderr.write(
        "No NVR VIP resources found matching the supplied naming pattern.\n"
    )
    sys.exit(1)

output = []

for cluster in clusters:
    vip = cluster + "-vip"

    if vip not in primitives:
        sys.stderr.write("Missing VIP resource: %s\n" % vip)
        sys.exit(1)

    core_group = "rg-" + cluster + "-core"

    if core_group not in groups:
        sys.stderr.write(
            "Missing expected CORE group: %s\n" % core_group
        )
        sys.exit(1)

    # Ensure the CORE group actually contains at least one primitive.
    core_members = []

    for rid, info in primitives.items():
        if info["group"] == core_group:
            core_members.append(rid)

    if not core_members:
        sys.stderr.write(
            "CORE group %s has no direct primitive members.\n" % core_group
        )
        sys.exit(1)

    # Discover exactly four NFSREC primitives, each using Filesystem.
    nfs_pattern = re.compile(
        r"^" + re.escape(cluster) + r"-nfsrec([0-9]+)$"
    )

    nfs_resources = []

    for rid, info in primitives.items():
        match = nfs_pattern.match(rid)

        if not match:
            continue

        cls, provider, agent = primitive_agent(info["xml"])

        if cls == "ocf" and provider == "heartbeat" and agent == "Filesystem":
            nfs_resources.append((int(match.group(1)), rid))

    nfs_resources.sort()

    if len(nfs_resources) != 4:
        sys.stderr.write(
            "%s: expected exactly 4 NFSREC Filesystem resources; found %d.\n"
            % (cluster, len(nfs_resources))
        )
        sys.exit(1)

    nfs_numbers = [number for number, rid in nfs_resources]

    if nfs_numbers != [1, 2, 3, 4]:
        sys.stderr.write(
            "%s: NFSREC numbering must be 01, 02, 03, 04; found %s.\n"
            % (cluster, nfs_numbers)
        )
        sys.exit(1)

    nfs_ids = [rid for number, rid in nfs_resources]

    # Discover Picata systemd resources.
    picata_pattern = re.compile(
        r"^" + re.escape(cluster) + r"-picata([0-9]+)$"
    )

    picata_resources = []

    for rid, info in primitives.items():
        match = picata_pattern.match(rid)

        if not match:
            continue

        cls, provider, agent = primitive_agent(info["xml"])

        if cls == "systemd" and agent.startswith("picata-"):
            picata_resources.append((int(match.group(1)), rid))

    picata_resources.sort()

    if not picata_resources:
        sys.stderr.write(
            "%s: no Picata systemd resources discovered.\n" % cluster
        )
        sys.exit(1)

    picata_ids = [rid for number, rid in picata_resources]

    # Discover exactly one configuration updater.
    updater_id = cluster + "-pctcfg-updater"

    if updater_id not in primitives:
        sys.stderr.write(
            "%s: missing updater resource %s.\n" % (cluster, updater_id)
        )
        sys.exit(1)

    cls, provider, agent = primitive_agent(
        primitives[updater_id]["xml"]
    )

    if cls != "systemd" or agent != "configuration-updater":
        sys.stderr.write(
            "%s: updater has unexpected resource agent.\n" % cluster
        )
        sys.exit(1)

    # Validate that each Picata instance has a corresponding NFSREC mount.
    nfs_set = set(nfs_ids)

    for number, picata_id in picata_resources:
        expected_nfs = "%s-nfsrec%02d" % (cluster, number)

        if expected_nfs not in nfs_set:
            sys.stderr.write(
                "%s: Picata %s has no matching NFSREC mount %s.\n"
                % (cluster, picata_id, expected_nfs)
            )
            sys.exit(1)

    output.append(
        "|".join([
            cluster,
            vip,
            core_group,
            ",".join(nfs_ids),
            ",".join(picata_ids),
            updater_id
        ])
    )

# Write the complete discovery result only after every cluster validates.
with open(output_path, "w") as handle:
    handle.write("\n".join(output) + "\n")

print("Discovered and validated %d NVR clusters." % len(output))

for line in output:
    fields = line.split("|")
    print(
        "%s: VIP=%s CORE=%s NFSREC=%d Picata=%d updater=%s"
        % (
            fields[0],
            fields[1],
            fields[2],
            len(fields[3].split(",")),
            len(fields[4].split(",")),
            fields[5]
        )
    )
PYTHON

[[ -s "$DISCOVERY_FILE" ]] ||
    die "Resource discovery returned no results."

# ---------------------------------------------------------------------------
# 3. Confirm and back up the CIB
# ---------------------------------------------------------------------------

log "The following operation will delete ALL existing constraints."
log "Discovered NVR clusters:"
cat "$DISCOVERY_FILE"

if [[ "$AUTO_CONFIRM" != "YES" ]]; then
    echo
    read -r -p "Type YES to back up the CIB and rebuild constraints: " ANSWER
    [[ "$ANSWER" == "YES" ]] ||
        die "Cancelled by operator."
fi

log "Creating CIB backup: $BACKUP_FILE"

pcs cluster cib "$BACKUP_FILE" ||
    die "Failed to create CIB backup."

[[ -s "$BACKUP_FILE" ]] ||
    die "CIB backup file is empty."

chmod 600 "$BACKUP_FILE"

log "CIB backup completed."

# ---------------------------------------------------------------------------
# 4. Delete all existing constraints
# ---------------------------------------------------------------------------

log "Deleting all existing Pacemaker constraints..."

CONSTRAINT_XML="$(mktemp /tmp/nvr-constraints.XXXXXX.xml)"
trap 'rm -f "$CIB_XML" "$DISCOVERY_FILE" "$CONSTRAINT_XML"' EXIT

cibadmin --query --scope constraints > "$CONSTRAINT_XML" ||
    die "Could not retrieve current constraints."

mapfile -t CONSTRAINT_IDS < <(
    python3 - "$CONSTRAINT_XML" <<'PYTHON'
from __future__ import print_function

import sys
import xml.etree.ElementTree as ET

root = ET.parse(sys.argv[1]).getroot()

for element in list(root):
    cid = element.get("id")
    if cid:
        print(cid)
PYTHON
)

for constraint_id in "${CONSTRAINT_IDS[@]}"; do
    log "Deleting constraint: $constraint_id"
    pcs constraint delete "$constraint_id" ||
        die "Failed to delete constraint $constraint_id"
done

log "Existing constraints deleted: ${#CONSTRAINT_IDS[@]}"

# ---------------------------------------------------------------------------
# 5. Rebuild constraints
# ---------------------------------------------------------------------------

# Keep IDs deterministic and descriptive.
#
# Colocation:
#   Every resource in one NVR is colocated with its VIP at INFINITY.
#
# Anti-colocation:
#   Every pair of NVR VIPs is mutually anti-colocated.
#
# Ordering:
#   CORE group starts before NFSREC mounts.
#   Each NFSREC mount starts before its matching Picata service.
#
# No ordering constraints are created for the configuration updater.

declare -a CLUSTERS=()
declare -A VIPS=()

while IFS='|' read -r cluster vip core nfs_csv picata_csv updater; do
    [[ -n "$cluster" ]] || continue

    CLUSTERS+=("$cluster")
    VIPS["$cluster"]="$vip"

    log "------------------------------------------------------------"
    log "Building constraints for $cluster"
    log "VIP: $vip"
    log "CORE: $core"
    log "NFSREC: $nfs_csv"
    log "Picata: $picata_csv"
    log "Updater: $updater"
    log "------------------------------------------------------------"

    # VIP and CORE group must run on the same node.
    pcs constraint colocation add \
        "$core" with "$vip" INFINITY \
        id="col-${cluster}-core-vip" ||
        die "Failed CORE/VIP colocation for $cluster"

    # NFSREC resources must run on the same node as the VIP.
    IFS=',' read -r -a nfs_array <<< "$nfs_csv"

    for nfs in "${nfs_array[@]}"; do
        pcs constraint colocation add \
            "$nfs" with "$vip" INFINITY \
            id="col-${cluster}-${nfs}-vip" ||
            die "Failed NFSREC/VIP colocation for $nfs"

        # CORE must start before the NFSREC mount.
        pcs constraint order \
            start "$core" then start "$nfs" \
            kind=Mandatory \
            id="ord-${cluster}-core-${nfs}" ||
            die "Failed CORE/NFSREC ordering for $nfs"
    done

    # Picata services must run on the same node as the VIP.
    IFS=',' read -r -a picata_array <<< "$picata_csv"

    for picata in "${picata_array[@]}"; do
        suffix="${picata##*picata}"
        nfs="$(printf '%s-nfsrec%02d' "$cluster" "$((10#$suffix))")"

        pcs constraint colocation add \
            "$picata" with "$vip" INFINITY \
            id="col-${cluster}-${picata}-vip" ||
            die "Failed Picata/VIP colocation for $picata"

        # NFS mount must start before its corresponding Picata service.
        # Mandatory ordering also gives reverse stop ordering.
        pcs constraint order \
            start "$nfs" then start "$picata" \
            kind=Mandatory \
            id="ord-${cluster}-${nfs}-${picata}" ||
            die "Failed NFSREC/Picata ordering for $picata"
    done

   # ---------------------------------------------------------------
    # Configuration updater dependencies
    #
    # The updater requires /etc/picata to be mounted first.
    # The /etc filesystem is provided by the nfsetc01 resource,
    # which is a member of the CORE resource group.
    #
    # Ensure:
    #   1. Updater is colocated with the cluster VIP.
    #   2. nfsetc01 starts before the configuration updater.
    # ---------------------------------------------------------------

    etc_resource="${cluster}-nfsetc01"

    # Updater must run on the same node as its VIP.
    pcs constraint colocation add \
        "$updater" with "$vip" INFINITY \
        id="col-${cluster}-updater-vip" ||
        die "Failed updater/VIP colocation for $cluster"

    # /etc/picata must be mounted before the updater starts.
    pcs constraint order \
        start "$etc_resource" then start "$updater" \
        kind=Mandatory \
        id="ord-${cluster}-etc-${updater}" ||
        die "Failed /etc/picata/updater ordering for $cluster"
done < "$DISCOVERY_FILE"

# ---------------------------------------------------------------------------
# 6. Pairwise anti-colocation between NVR VIPs
# ---------------------------------------------------------------------------

log "Creating pairwise anti-colocation constraints between NVR VIPs..."

for ((i = 0; i < ${#CLUSTERS[@]}; i++)); do
    for ((j = i + 1; j < ${#CLUSTERS[@]}; j++)); do
        cluster_a="${CLUSTERS[$i]}"
        cluster_b="${CLUSTERS[$j]}"

        vip_a="${VIPS[$cluster_a]}"
        vip_b="${VIPS[$cluster_b]}"

        pcs constraint colocation add \
            "$vip_a" with "$vip_b" -INFINITY \
            id="anti-${cluster_a}-${cluster_b}" ||
            die "Failed anti-colocation between $cluster_a and $cluster_b"
    done
done

# ---------------------------------------------------------------------------
# 7. Final verification
# ---------------------------------------------------------------------------

log "Constraint rebuild completed."
log "Displaying current constraints..."

pcs constraint config ||
    die "Unable to display rebuilt constraints."

log "============================================================"
log "NVR constraint rebuild completed successfully."
log "CIB backup: $BACKUP_FILE"
log "Log file: $LOG_FILE"
log "============================================================"