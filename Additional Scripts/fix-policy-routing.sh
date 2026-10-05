#!/bin/bash
#
# ============================================================================
# NVR Policy Routing Correction
# ============================================================================
#
# Target: NVR application blades / CLNVRM030
#
# Existing interfaces:
#   Frontend  : vlan126 on bond1
#   Middleend : vlan128 on bond0
#   Backend   : bond2
#
# Routing tables:
#   100 = frontend
#   200 = middleend
#   300 = backend
#
# IMPORTANT VIP DESIGN:
#
#   Pacemaker VIPs:
#       10.101.27.35
#       10.101.27.36
#       10.101.27.37
#       10.101.27.38
#       10.101.27.39
#       10.101.27.40
#       10.101.27.41
#
#   These VIPs MUST use the FRONTEND routing table when they are used
#   as source addresses.
#
#   The VIP source rules are installed on EVERY NVR node.
#   This is intentional because Pacemaker can move a VIP from one node
#   to another node.
#
#   Example:
#
#       from 10.101.27.41/32 lookup frontend
#
#   This must have a priority lower than the destination rule:
#
#       to 10.130.42.0/23 lookup middleend
#
#   Therefore:
#
#       107 -> VIP source rule
#       507 -> destination rule
#
#   VIP traffic therefore selects FRONTEND before the middleend
#   destination rule can be evaluated.
#
# Usage:
#
#   ./fix-policy-routing.sh
#       Dry-run
#
#   ./fix-policy-routing.sh --apply
#       Apply runtime policy routing changes
#
# IMPORTANT:
#   - Does not create/delete VLANs.
#   - Does not modify NetworkManager profiles.
#   - Does not modify vlan144 / cluster networking.
#   - Does not flush the entire routing configuration.
#   - Changes runtime routes and policy rules only.
#   - Run this script on ALL NVR nodes.
#
# ============================================================================

set -Eeuo pipefail


###############################################################################
# CONFIGURATION
###############################################################################

# ---------------------------------------------------------------------------
# Frontend
# ---------------------------------------------------------------------------

FRONT_IF="vlan126"
FRONT_GW="10.101.26.1"
FRONT_TABLE="100"
FRONT_TABLE_NAME="frontend"
FRONT_SRC_PRIORITY="100"


# ---------------------------------------------------------------------------
# Middleend
# ---------------------------------------------------------------------------

MIDDLE_IF="vlan128"
MIDDLE_GW="10.101.28.1"
MIDDLE_TABLE="200"
MIDDLE_TABLE_NAME="middleend"
MIDDLE_SRC_PRIORITY="200"


# ---------------------------------------------------------------------------
# Backend
# ---------------------------------------------------------------------------

BACK_IF="bond2"
BACK_GW="10.101.30.1"
BACK_TABLE="300"
BACK_TABLE_NAME="backend"
BACK_SRC_PRIORITY="300"


# ---------------------------------------------------------------------------
# Backend local subnet
#
# Must bypass frontend catch-all.
# ---------------------------------------------------------------------------

BACKEND_LOCAL_NET="10.101.30.0/23"
BACKEND_LOCAL_PRIORITY="400"


# ---------------------------------------------------------------------------
# Frontend catch-all
#
# Must be evaluated after all specific destination/source rules.
# ---------------------------------------------------------------------------

FRONT_CATCHALL_PRIORITY="9999"


# ---------------------------------------------------------------------------
# Pacemaker VIP source rules
#
# IMPORTANT:
# These rules are installed on EVERY NVR node.
#
# Do NOT remove them simply because a VIP is not currently local.
#
# If Pacemaker moves the VIP, the routing rule is already present on
# the destination node.
# ---------------------------------------------------------------------------

VIP_SOURCE_IPS=(
    "10.101.27.35"
    "10.101.27.36"
    "10.101.27.37"
    "10.101.27.38"
    "10.101.27.39"
    "10.101.27.40"
    "10.101.27.41"
)

VIP_SOURCE_PRIORITIES=(
    "101"
    "102"
    "103"
    "104"
    "105"
    "106"
    "107"
)


# ---------------------------------------------------------------------------
# Middleend remote networks
# ---------------------------------------------------------------------------

MIDDLEEND_REMOTE_NETS=(
    "10.101.18.0/23"
    "10.101.42.0/23"
)

MIDDLEEND_REMOTE_PRIORITIES=(
    "401"
    "402"
)


# ---------------------------------------------------------------------------
# Middleend destination networks
#
# 10.130.42.0/23 is the Ansible network.
#
# This MUST remain in the middleend table because traffic to the
# Ansible network from normal middleend traffic uses vlan128.
#
# VIP traffic is handled BEFORE this rule by the VIP source rules
# at priorities 101-107.
# ---------------------------------------------------------------------------

MIDDLEEND_DEST_NETS=(
    "10.130.2.0/23"
    "10.130.4.0/23"
    "10.130.6.0/23"
    "10.130.8.0/23"
    "10.130.12.0/23"
    "10.130.26.0/23"
    "10.130.42.0/23"
)

MIDDLEEND_DEST_PRIORITIES=(
    "501"
    "502"
    "503"
    "504"
    "505"
    "506"
    "507"
)


# ---------------------------------------------------------------------------
# Backend destination networks
# ---------------------------------------------------------------------------

BACKEND_DEST_NETS=(
    "10.101.0.0/23"
    "10.101.2.0/23"
    "10.101.4.0/23"
    "10.101.6.0/23"
    "10.120.0.0/23"
    "10.102.2.0/23"
    "10.102.4.0/23"
    "10.102.6.0/23"
)

BACKEND_DEST_PRIORITIES=(
    "601"
    "602"
    "603"
    "604"
    "605"
    "606"
    "607"
    "608"
)


###############################################################################
# EXECUTION MODE
###############################################################################

MODE="DRY-RUN"

if [[ "${1:-}" == "--apply" ]]; then

    MODE="APPLY"

elif [[ $# -gt 0 ]]; then

    echo "Usage: $0 [--apply]"
    exit 1

fi


###############################################################################
# LOGGING
###############################################################################

log() {

    echo "[$(date '+%F %T')] $*"

}


section() {

    echo
    echo "=================================================="
    echo " $*"
    echo "=================================================="

}


run_cmd() {

    if [[ "$MODE" == "APPLY" ]]; then

        "$@"

    else

        printf '[DRY-RUN] '
        printf '%q ' "$@"
        echo

    fi

}


###############################################################################
# ROOT / DEPENDENCIES
###############################################################################

if [[ "$EUID" -ne 0 ]]; then

    echo "ERROR: Run this script as root."
    exit 1

fi


for cmd in ip python3 awk; do

    if ! command -v "$cmd" >/dev/null 2>&1; then

        echo "ERROR: Required command not found: $cmd"
        exit 1

    fi

done


###############################################################################
# HEADER
###############################################################################

section "NVR Policy Routing Correction"

echo "Host : $(hostname -s)"
echo "Mode : $MODE"


###############################################################################
# EXISTING INTERFACES
###############################################################################

section "Existing interfaces"

ip -br address


for iface in "$FRONT_IF" "$MIDDLE_IF" "$BACK_IF"; do

    if ! ip link show dev "$iface" >/dev/null 2>&1; then

        echo "ERROR: Required interface $iface does not exist."
        exit 1

    fi

    if ! ip -o link show dev "$iface" | grep -q "UP"; then

        echo "WARNING: Interface $iface may be down."

    fi

done


###############################################################################
# DETECT IPV4 ADDRESSES
###############################################################################

get_ipv4_cidr() {

    local iface="$1"

    ip -o -4 addr show dev "$iface" scope global |
        awk '{print $4}' |
        head -n1

}


FRONT_CIDR="$(get_ipv4_cidr "$FRONT_IF")"
MIDDLE_CIDR="$(get_ipv4_cidr "$MIDDLE_IF")"
BACK_CIDR="$(get_ipv4_cidr "$BACK_IF")"


if [[ -z "$FRONT_CIDR" ||
      -z "$MIDDLE_CIDR" ||
      -z "$BACK_CIDR" ]]; then

    echo "ERROR: Could not detect all required IPv4 addresses."

    echo "Frontend : $FRONT_CIDR"
    echo "Middleend: $MIDDLE_CIDR"
    echo "Backend  : $BACK_CIDR"

    exit 1

fi


# Source IP addresses, without prefix.

FRONT_SRC="${FRONT_CIDR%/*}"
MIDDLE_SRC="${MIDDLE_CIDR%/*}"
BACK_SRC="${BACK_CIDR%/*}"


###############################################################################
# CALCULATE NETWORK PREFIXES
###############################################################################

get_network_prefix() {

    python3 - "$1" <<'PY'
import ipaddress
import sys

try:

    print(ipaddress.ip_interface(sys.argv[1]).network)

except ValueError as exc:

    print(
        f"Invalid interface CIDR: {exc}",
        file=sys.stderr
    )

    sys.exit(1)

PY

}


FRONT_NET="$(get_network_prefix "$FRONT_CIDR")"
MIDDLE_NET="$(get_network_prefix "$MIDDLE_CIDR")"
BACK_NET="$(get_network_prefix "$BACK_CIDR")"


###############################################################################
# DISPLAY DETECTED ADDRESSES
###############################################################################

section "Detected existing addresses"

echo "Frontend address : $FRONT_CIDR"
echo "Frontend network : $FRONT_NET"
echo "Frontend source  : $FRONT_SRC"

echo

echo "Middleend address : $MIDDLE_CIDR"
echo "Middleend network : $MIDDLE_NET"
echo "Middleend source  : $MIDDLE_SRC"

echo

echo "Backend address : $BACK_CIDR"
echo "Backend network : $BACK_NET"
echo "Backend source  : $BACK_SRC"


###############################################################################
# VALIDATE GATEWAYS
###############################################################################

validate_gateway() {

    local iface="$1"
    local gateway="$2"
    local cidr="$3"

    if ! python3 - "$gateway" "$cidr" <<'PY'
import ipaddress
import sys

try:

    gateway = ipaddress.ip_address(sys.argv[1])
    network = ipaddress.ip_interface(sys.argv[2]).network

    if gateway.version != 4:
        sys.exit(1)

    sys.exit(0 if gateway in network else 1)

except ValueError:

    sys.exit(1)

PY
    then

        echo "ERROR: Gateway $gateway is not in subnet $cidr on $iface."
        return 1

    fi

    echo "Gateway $gateway validated on $iface ($cidr)"

}


section "Validate gateways"

validate_gateway \
    "$FRONT_IF" \
    "$FRONT_GW" \
    "$FRONT_CIDR" ||
    exit 1

validate_gateway \
    "$MIDDLE_IF" \
    "$MIDDLE_GW" \
    "$MIDDLE_CIDR" ||
    exit 1

validate_gateway \
    "$BACK_IF" \
    "$BACK_GW" \
    "$BACK_CIDR" ||
    exit 1


###############################################################################
# ROUTING TABLE NAMES
###############################################################################

RT_TABLES="/etc/iproute2/rt_tables"

section "Verify routing table names"

if ! grep -qE "^${FRONT_TABLE}[[:space:]]+${FRONT_TABLE_NAME}$" "$RT_TABLES"; then

    echo "${FRONT_TABLE} ${FRONT_TABLE_NAME}" >> "$RT_TABLES"

    echo "Added:"
    echo "  ${FRONT_TABLE} ${FRONT_TABLE_NAME}"

fi


if ! grep -qE "^${MIDDLE_TABLE}[[:space:]]+${MIDDLE_TABLE_NAME}$" "$RT_TABLES"; then

    echo "${MIDDLE_TABLE} ${MIDDLE_TABLE_NAME}" >> "$RT_TABLES"

    echo "Added:"
    echo "  ${MIDDLE_TABLE} ${MIDDLE_TABLE_NAME}"

fi


if ! grep -qE "^${BACK_TABLE}[[:space:]]+${BACK_TABLE_NAME}$" "$RT_TABLES"; then

    echo "${BACK_TABLE} ${BACK_TABLE_NAME}" >> "$RT_TABLES"

    echo "Added:"
    echo "  ${BACK_TABLE} ${BACK_TABLE_NAME}"

fi


###############################################################################
# CURRENT POLICY RULES
###############################################################################

section "Current policy rules"

ip -4 rule show


###############################################################################
# CURRENT ROUTING TABLES
###############################################################################

section "Current routing tables"

for table in \
    "$FRONT_TABLE" \
    "$MIDDLE_TABLE" \
    "$BACK_TABLE"
do

    echo
    echo "--- Table $table ---"

    ip -4 route show table "$table" || true

done


###############################################################################
# MANAGED PRIORITIES
#
# IMPORTANT:
#
# 100  frontend source
# 101-107 VIP sources
# 200  middleend source
# 300  backend source
# 400  backend local destination
# 401-402 middleend remote destinations
# 501-507 middleend destination networks
# 601-608 backend destination networks
# 9999 frontend catch-all
#
###############################################################################

MANAGED_PRIORITIES=(

    "$FRONT_SRC_PRIORITY"

    "${VIP_SOURCE_PRIORITIES[@]}"

    "$MIDDLE_SRC_PRIORITY"

    "$BACK_SRC_PRIORITY"

    "$BACKEND_LOCAL_PRIORITY"

    "${MIDDLEEND_REMOTE_PRIORITIES[@]}"

    "${MIDDLEEND_DEST_PRIORITIES[@]}"

    "${BACKEND_DEST_PRIORITIES[@]}"

    "$FRONT_CATCHALL_PRIORITY"

)


###############################################################################
# REMOVE EXISTING MANAGED RULES
###############################################################################

section "Remove existing managed policy rules"

for priority in "${MANAGED_PRIORITIES[@]}"; do

    while ip -4 rule del priority "$priority" 2>/dev/null; do

        log "Removed existing rule at priority $priority"

    done

done


###############################################################################
# FRONTEND ROUTING TABLE
###############################################################################

section "Configure frontend table $FRONT_TABLE"

run_cmd ip -4 route replace "$FRONT_NET" \
    dev "$FRONT_IF" \
    scope link \
    src "$FRONT_SRC" \
    table "$FRONT_TABLE"


run_cmd ip -4 route replace default \
    via "$FRONT_GW" \
    dev "$FRONT_IF" \
    src "$FRONT_SRC" \
    table "$FRONT_TABLE"


###############################################################################
# MIDDLEEND ROUTING TABLE
###############################################################################

section "Configure middleend table $MIDDLE_TABLE"

run_cmd ip -4 route replace "$MIDDLE_NET" \
    dev "$MIDDLE_IF" \
    scope link \
    src "$MIDDLE_SRC" \
    table "$MIDDLE_TABLE"


run_cmd ip -4 route replace default \
    via "$MIDDLE_GW" \
    dev "$MIDDLE_IF" \
    src "$MIDDLE_SRC" \
    table "$MIDDLE_TABLE"


for net in "${MIDDLEEND_REMOTE_NETS[@]}"; do

    run_cmd ip -4 route replace "$net" \
        via "$MIDDLE_GW" \
        dev "$MIDDLE_IF" \
        table "$MIDDLE_TABLE"

done


###############################################################################
# BACKEND ROUTING TABLE
###############################################################################

section "Configure backend table $BACK_TABLE"

run_cmd ip -4 route replace "$BACK_NET" \
    dev "$BACK_IF" \
    scope link \
    src "$BACK_SRC" \
    table "$BACK_TABLE"


run_cmd ip -4 route replace default \
    via "$BACK_GW" \
    dev "$BACK_IF" \
    src "$BACK_SRC" \
    table "$BACK_TABLE"


###############################################################################
# NORMAL SOURCE-BASED RULES
###############################################################################

section "Configure normal source-based rules"


# ---------------------------------------------------------------------------
# Frontend primary address
# ---------------------------------------------------------------------------

run_cmd ip -4 rule add \
    priority "$FRONT_SRC_PRIORITY" \
    from "$FRONT_SRC/32" \
    table "$FRONT_TABLE"


# ---------------------------------------------------------------------------
# Middleend primary address
# ---------------------------------------------------------------------------

run_cmd ip -4 rule add \
    priority "$MIDDLE_SRC_PRIORITY" \
    from "$MIDDLE_SRC/32" \
    table "$MIDDLE_TABLE"


# ---------------------------------------------------------------------------
# Backend primary address
# ---------------------------------------------------------------------------

run_cmd ip -4 rule add \
    priority "$BACK_SRC_PRIORITY" \
    from "$BACK_SRC/32" \
    table "$BACK_TABLE"


###############################################################################
# PACEMAKER VIP SOURCE RULES
#
# THIS IS THE IMPORTANT FIX.
#
# These rules MUST have a priority lower than 501-507.
#
# Example:
#
#   107 from 10.101.27.41/32 lookup frontend
#   507 to 10.130.42.0/23 lookup middleend
#
# Linux evaluates priority 107 first.
#
###############################################################################

section "Configure Pacemaker VIP source rules"

for i in "${!VIP_SOURCE_IPS[@]}"; do

    vip="${VIP_SOURCE_IPS[$i]}"
    priority="${VIP_SOURCE_PRIORITIES[$i]}"

    echo "VIP $vip -> priority $priority -> $FRONT_TABLE_NAME"

    run_cmd ip -4 rule add \
        priority "$priority" \
        from "$vip/32" \
        table "$FRONT_TABLE"

done


###############################################################################
# BACKEND LOCAL SUBNET RULE
###############################################################################

section "Configure backend local subnet rule"

run_cmd ip -4 rule add \
    priority "$BACKEND_LOCAL_PRIORITY" \
    to "$BACKEND_LOCAL_NET" \
    table "$BACK_TABLE"


###############################################################################
# MIDDLEEND REMOTE DESTINATION RULES
###############################################################################

section "Configure middleend remote destination rules"

for i in "${!MIDDLEEND_REMOTE_NETS[@]}"; do

    net="${MIDDLEEND_REMOTE_NETS[$i]}"
    priority="${MIDDLEEND_REMOTE_PRIORITIES[$i]}"

    echo "$priority -> $net -> $MIDDLE_TABLE_NAME"

    run_cmd ip -4 rule add \
        priority "$priority" \
        to "$net" \
        table "$MIDDLE_TABLE"

done


###############################################################################
# MIDDLEEND DESTINATION RULES
###############################################################################

section "Configure middleend destination rules"

for i in "${!MIDDLEEND_DEST_NETS[@]}"; do

    net="${MIDDLEEND_DEST_NETS[$i]}"
    priority="${MIDDLEEND_DEST_PRIORITIES[$i]}"

    echo "$priority -> $net -> $MIDDLE_TABLE_NAME"

    run_cmd ip -4 rule add \
        priority "$priority" \
        to "$net" \
        table "$MIDDLE_TABLE"

done


###############################################################################
# BACKEND DESTINATION RULES
###############################################################################

section "Configure backend destination rules"

for i in "${!BACKEND_DEST_NETS[@]}"; do

    net="${BACKEND_DEST_NETS[$i]}"
    priority="${BACKEND_DEST_PRIORITIES[$i]}"

    echo "$priority -> $net -> $BACK_TABLE_NAME"

    run_cmd ip -4 rule add \
        priority "$priority" \
        to "$net" \
        table "$BACK_TABLE"

done


###############################################################################
# FRONTEND CATCH-ALL
###############################################################################

section "Configure frontend catch-all"

run_cmd ip -4 rule add \
    priority "$FRONT_CATCHALL_PRIORITY" \
    to 0.0.0.0/0 \
    table "$FRONT_TABLE"


###############################################################################
# FINAL POLICY RULES
###############################################################################

section "Final policy rules"

if [[ "$MODE" == "APPLY" ]]; then

    ip -4 rule show

else

    echo "Dry-run only: policy rules were not changed."

fi


###############################################################################
# FINAL ROUTING TABLES
###############################################################################

section "Final routing tables"

if [[ "$MODE" == "APPLY" ]]; then

    for table in \
        "$FRONT_TABLE" \
        "$MIDDLE_TABLE" \
        "$BACK_TABLE"
    do

        echo
        echo "--- Table $table ---"

        ip -4 route show table "$table"

    done

else

    echo "Dry-run only: routing tables were not changed."

fi


###############################################################################
# ROUTE LOOKUP VERIFICATION
###############################################################################

section "Route lookup verification"

if [[ "$MODE" == "APPLY" ]]; then


    # -----------------------------------------------------------------------
    # Backend local subnet
    # -----------------------------------------------------------------------

    echo
    echo "===== BACKEND LOCAL SUBNET ====="

    ip -4 route get 10.101.30.11


    # -----------------------------------------------------------------------
    # Backend gateway
    # -----------------------------------------------------------------------

    echo
    echo "===== BACKEND GATEWAY ====="

    ip -4 route get \
        "$BACK_GW" \
        from "$BACK_SRC"


    # -----------------------------------------------------------------------
    # Middleend local subnet
    # -----------------------------------------------------------------------

    echo
    echo "===== MIDDLEEND LOCAL SUBNET ====="

    ip -4 route get 10.101.28.11


    # -----------------------------------------------------------------------
    # Frontend local subnet
    # -----------------------------------------------------------------------

    echo
    echo "===== FRONTEND LOCAL SUBNET ====="

    ip -4 route get 10.101.26.11


    # -----------------------------------------------------------------------
    # Middleend remote subnet
    # -----------------------------------------------------------------------

    echo
    echo "===== MIDDLEEND REMOTE SUBNET ====="

    ip -4 route get 10.101.18.11


    # -----------------------------------------------------------------------
    # Ansible network
    # -----------------------------------------------------------------------

    echo
    echo "===== ANSIBLE NETWORK ====="

    echo "Expected normal traffic:"
    echo "10.130.42.181 -> middleend"

    ip -4 route get 10.130.42.181


    # -----------------------------------------------------------------------
    # VIP -> Ansible route verification
    #
    # Every VIP should use FRONTEND.
    # -----------------------------------------------------------------------

    echo
    echo "===== PACEMAKER VIP -> ANSIBLE ROUTING ====="

    for vip in "${VIP_SOURCE_IPS[@]}"; do

        echo
        echo "VIP: $vip"

        ip -4 route get \
            10.130.42.181 \
            from "$vip"

    done


else

    echo
    echo "Dry-run only: route lookup verification skipped."

fi


###############################################################################
# FINAL VIP RULE VERIFICATION
###############################################################################

section "Pacemaker VIP policy rules"

if [[ "$MODE" == "APPLY" ]]; then

    echo
    echo "Expected VIP rules:"
    echo

    for i in "${!VIP_SOURCE_IPS[@]}"; do

        vip="${VIP_SOURCE_IPS[$i]}"
        priority="${VIP_SOURCE_PRIORITIES[$i]}"

        echo "$priority: from $vip/32 lookup $FRONT_TABLE_NAME"

    done

    echo
    echo "Actual:"
    echo

    ip -4 rule show | grep -E \
        'from 10\.101\.27\.(35|36|37|38|39|40|41)' ||
        true

fi


###############################################################################
# COMPLETION
###############################################################################

section "Completed"

if [[ "$MODE" == "APPLY" ]]; then

    echo "Policy routing changes applied to runtime."
    echo
    echo "Frontend interface : $FRONT_IF"
    echo "Frontend gateway   : $FRONT_GW"
    echo
    echo "Middleend interface: $MIDDLE_IF"
    echo "Middleend gateway  : $MIDDLE_GW"
    echo
    echo "Backend interface  : $BACK_IF"
    echo "Backend gateway    : $BACK_GW"
    echo
    echo "Pacemaker VIPs     : ${#VIP_SOURCE_IPS[@]}"
    echo
    echo "IMPORTANT:"
    echo "VIP source rules are installed regardless of the current"
    echo "Pacemaker location of the VIP."
    echo
    echo "NetworkManager profiles were not modified."
    echo "No VLAN interfaces were created or deleted."
    echo "No cluster networking was modified."

else

    echo "Dry-run completed."
    echo
    echo "Use:"
    echo
    echo "    $0 --apply"
    echo
    echo "to apply the runtime policy routing changes."

fi