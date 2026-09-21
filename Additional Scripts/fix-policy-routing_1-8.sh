#!/bin/bash

set -u

###############################################################################
# CONFIGURATION
###############################################################################

FRONTEND_NET="10.101.26.0/23"
FRONTEND_GW="10.101.26.1"

MIDDLEEND_NET="10.101.28.0/23"
MIDDLEEND_GW="10.101.28.1"

BACKEND_NET="10.101.30.0/23"
BACKEND_GW="10.101.30.1"

CLUSTER_NET="10.101.44.0/23"

FRONTEND_IF="vlan126"
MIDDLEEND_IF="vlan128"
BACKEND_IF="bond2"
CLUSTER_IF="vlan144"

BOND_SLAVE1="ens2f0"
BOND_SLAVE2="ens2f1"

FRONTEND_TABLE="frontend"
MIDDLEEND_TABLE="middleend"
BACKEND_TABLE="backend"
CLUSTER_TABLE="cluster"

FRONTEND_TABLE_ID=100
MIDDLEEND_TABLE_ID=200
BACKEND_TABLE_ID=300
CLUSTER_TABLE_ID=400


###############################################################################
# FUNCTIONS
###############################################################################

banner() {
    echo
    echo "========================================="
    echo " $1"
    echo "========================================="
}


###############################################################################
# ROOT CHECK
###############################################################################

if [ "$(id -u)" -ne 0 ]; then
    echo "ERROR: This script must be run as root."
    exit 1
fi


###############################################################################
# DETECT HOST NUMBER AUTOMATICALLY
#
# Examples:
# tvsnvrapp001mp -> 1
# tvsnvrapp005mp -> 5
# tvsnvrapp008mp -> 8
###############################################################################

banner "DETECTING SERVER NUMBER"

HOSTNAME_SHORT=$(hostname -s)

echo "Hostname: ${HOSTNAME_SHORT}"

if [[ "$HOSTNAME_SHORT" =~ ([0-9]{3})mp$ ]]; then
    NODE_NUMBER=$((10#${BASH_REMATCH[1]}))
else
    echo "ERROR: Cannot determine node number from hostname:"
    echo "${HOSTNAME_SHORT}"
    echo
    echo "Expected hostname ending similar to:"
    echo "xxx001mp"
    echo "xxx002mp"
    echo "xxx008mp"
    exit 1
fi

echo "Detected node number: ${NODE_NUMBER}"


###############################################################################
# CALCULATE IP LAST OCTET
#
# Node 001 -> 11
# Node 002 -> 12
# Node 003 -> 13
#
# Formula:
# NODE_NUMBER + 10
###############################################################################

HOST_OCTET=$((NODE_NUMBER + 10))

echo "Calculated IP last octet: ${HOST_OCTET}"


###############################################################################
# DEFINE IP ADDRESSES
###############################################################################

FRONTEND_IP="10.101.26.${HOST_OCTET}"
MIDDLEEND_IP="10.101.28.${HOST_OCTET}"
BACKEND_IP="10.101.30.${HOST_OCTET}"
CLUSTER_IP="10.101.44.${HOST_OCTET}"


banner "NETWORK CONFIGURATION"

echo "Frontend:  ${FRONTEND_IP}"
echo "Middleend: ${MIDDLEEND_IP}"
echo "Backend:   ${BACKEND_IP}"
echo "Cluster:   ${CLUSTER_IP}"


###############################################################################
# CONFIGURE ROUTING TABLE NAMES
###############################################################################

banner "CONFIGURING ROUTING TABLES"

RT_TABLES="/etc/iproute2/rt_tables"

grep -qE "^${FRONTEND_TABLE_ID}[[:space:]]+${FRONTEND_TABLE}$" "$RT_TABLES" || \
    echo "${FRONTEND_TABLE_ID} ${FRONTEND_TABLE}" >> "$RT_TABLES"

grep -qE "^${MIDDLEEND_TABLE_ID}[[:space:]]+${MIDDLEEND_TABLE}$" "$RT_TABLES" || \
    echo "${MIDDLEEND_TABLE_ID} ${MIDDLEEND_TABLE}" >> "$RT_TABLES"

grep -qE "^${BACKEND_TABLE_ID}[[:space:]]+${BACKEND_TABLE}$" "$RT_TABLES" || \
    echo "${BACKEND_TABLE_ID} ${BACKEND_TABLE}" >> "$RT_TABLES"

grep -qE "^${CLUSTER_TABLE_ID}[[:space:]]+${CLUSTER_TABLE}$" "$RT_TABLES" || \
    echo "${CLUSTER_TABLE_ID} ${CLUSTER_TABLE}" >> "$RT_TABLES"

echo "100 frontend configured"
echo "200 middleend configured"
echo "300 backend configured"
echo "400 cluster configured"


###############################################################################
# VERIFY NETWORKMANAGER CONNECTIONS
###############################################################################

banner "VERIFYING NETWORK CONNECTIONS"

for CON in \
    "$FRONTEND_IF" \
    "$MIDDLEEND_IF" \
    "$BACKEND_IF" \
    "$CLUSTER_IF" \
    "$BOND_SLAVE1" \
    "$BOND_SLAVE2"
do
    if ! nmcli connection show "$CON" >/dev/null 2>&1; then
        echo "ERROR: NetworkManager connection '${CON}' does not exist."
        exit 1
    fi
done

echo "All required connections exist."


###############################################################################
# CONFIGURE BOND2 AS IEEE 802.3AD / LACP
###############################################################################

banner "CONFIGURING BOND2 FOR LACP"

echo "Configuring:"
echo "Mode: 802.3ad"
echo "LACP rate: fast"
echo "MII monitoring: 100"
echo "Transmit hash policy: layer3+4"

nmcli connection modify "$BACKEND_IF" \
    bond.options \
    "mode=802.3ad,lacp_rate=fast,miimon=100,xmit_hash_policy=layer3+4"


###############################################################################
# ENSURE SLAVES BELONG TO BOND2
###############################################################################

banner "VERIFYING BOND2 SLAVES"

BOND_UUID=$(nmcli -g connection.uuid connection show "$BACKEND_IF")

echo "bond2 UUID: ${BOND_UUID}"

nmcli connection modify "$BOND_SLAVE1" \
    connection.master "$BOND_UUID" \
    connection.slave-type bond

nmcli connection modify "$BOND_SLAVE2" \
    connection.master "$BOND_UUID" \
    connection.slave-type bond

echo "${BOND_SLAVE1} configured as bond slave."
echo "${BOND_SLAVE2} configured as bond slave."


###############################################################################
# RESTART BOND
###############################################################################

banner "RESTARTING BOND2"

echo "Stopping bond slaves..."

nmcli connection down "$BOND_SLAVE1" 2>/dev/null || true
nmcli connection down "$BOND_SLAVE2" 2>/dev/null || true

echo "Stopping bond2..."

nmcli connection down "$BACKEND_IF" 2>/dev/null || true

sleep 3

echo "Starting bond2..."

nmcli connection up "$BACKEND_IF"

sleep 2

echo "Starting bond slaves..."

nmcli connection up "$BOND_SLAVE1" 2>/dev/null || true
nmcli connection up "$BOND_SLAVE2" 2>/dev/null || true

echo
echo "Waiting for LACP convergence..."

sleep 10


###############################################################################
# VERIFY BOND MODE
###############################################################################

banner "VERIFYING BOND2 MODE"

cat "/proc/net/bonding/${BACKEND_IF}"

if ! grep -q "IEEE 802.3ad Dynamic link aggregation" \
    "/proc/net/bonding/${BACKEND_IF}"; then

    echo
    echo "ERROR: bond2 is NOT running in IEEE 802.3ad mode."
    exit 1
fi

echo
echo "SUCCESS: bond2 is running in IEEE 802.3ad / LACP mode."


###############################################################################
# VERIFY ACTIVE AGGREGATOR
###############################################################################

banner "VERIFYING LACP AGGREGATOR"

ACTIVE_PORTS=$(grep -A10 "Active Aggregator Info" \
    "/proc/net/bonding/${BACKEND_IF}" \
    | grep "Number of ports" \
    | awk '{print $5}')

echo "Active LACP ports: ${ACTIVE_PORTS:-0}"

if [ "${ACTIVE_PORTS:-0}" -lt 2 ]; then

    echo
    echo "WARNING: bond2 does not currently have 2 active ports."
    echo
    echo "The bond configuration is correct, but LACP convergence"
    echo "may still be in progress or the switch configuration"
    echo "should be checked."

else

    echo "SUCCESS: Both ports are active in the LACP aggregator."

fi


###############################################################################
# CLEAR BACKEND NEIGHBOR CACHE
###############################################################################

banner "CLEARING BACKEND NEIGHBOR CACHE"

ip neigh flush dev "$BACKEND_IF" 2>/dev/null || true


###############################################################################
# OPTIONAL ARP TEST
#
# IMPORTANT:
# ARPING FAILURE DOES NOT STOP THE SCRIPT.
# Some systems/environments show successful IP traffic even when
# arping behaves inconsistently.
###############################################################################

banner "VERIFYING BACKEND GATEWAY ARP"

arping -I "$BACKEND_IF" -c 3 "$BACKEND_GW" || true


###############################################################################
# CONFIGURE NETWORKMANAGER ADDRESSES
###############################################################################

banner "VERIFYING IP ADDRESSES"

echo "Frontend:"
ip -br addr show "$FRONTEND_IF"

echo
echo "Middleend:"
ip -br addr show "$MIDDLEEND_IF"

echo
echo "Backend:"
ip -br addr show "$BACKEND_IF"

echo
echo "Cluster:"
ip -br addr show "$CLUSTER_IF"


###############################################################################
# REMOVE OLD POLICY RULES
###############################################################################

banner "REMOVING OLD POLICY RULES"

# Remove priority 92 rule
while ip rule show | grep -q \
    "to ${BACKEND_NET} lookup ${BACKEND_TABLE}"; do

    ip rule del to "$BACKEND_NET" table "$BACKEND_TABLE" 2>/dev/null || true

done


# Remove source-based rules
ip rule del priority 100 2>/dev/null || true
ip rule del priority 200 2>/dev/null || true
ip rule del priority 300 2>/dev/null || true
ip rule del priority 400 2>/dev/null || true


# Remove middleend destination rules
for PRIORITY in 501 502 503 504 505 506; do
    ip rule del priority "$PRIORITY" 2>/dev/null || true
done


# Remove backend destination rules
for PRIORITY in 601 602 603 604 605 606 607 608; do
    ip rule del priority "$PRIORITY" 2>/dev/null || true
done


###############################################################################
# FLUSH POLICY ROUTING TABLES
###############################################################################

banner "FLUSHING POLICY ROUTING TABLES"

for TABLE in \
    "$FRONTEND_TABLE" \
    "$MIDDLEEND_TABLE" \
    "$BACKEND_TABLE" \
    "$CLUSTER_TABLE"
do

    echo "Flushing table ${TABLE}"

    ip route flush table "$TABLE" 2>/dev/null || true

done


###############################################################################
# CONFIGURE FRONTEND ROUTING TABLE
###############################################################################

banner "CONFIGURING FRONTEND"

ip route add "$FRONTEND_NET" \
    dev "$FRONTEND_IF" \
    src "$FRONTEND_IP" \
    table "$FRONTEND_TABLE"

ip route add default \
    via "$FRONTEND_GW" \
    dev "$FRONTEND_IF" \
    table "$FRONTEND_TABLE"


###############################################################################
# CONFIGURE MIDDLEEND ROUTING TABLE
###############################################################################

banner "CONFIGURING MIDDLEEND"

ip route add "$MIDDLEEND_NET" \
    dev "$MIDDLEEND_IF" \
    src "$MIDDLEEND_IP" \
    table "$MIDDLEEND_TABLE"

ip route add default \
    via "$MIDDLEEND_GW" \
    dev "$MIDDLEEND_IF" \
    table "$MIDDLEEND_TABLE"


###############################################################################
# CONFIGURE BACKEND ROUTING TABLE
###############################################################################

banner "CONFIGURING BACKEND"

ip route add "$BACKEND_NET" \
    dev "$BACKEND_IF" \
    src "$BACKEND_IP" \
    table "$BACKEND_TABLE"

ip route add default \
    via "$BACKEND_GW" \
    dev "$BACKEND_IF" \
    table "$BACKEND_TABLE"


###############################################################################
# CONFIGURE CLUSTER ROUTING TABLE
###############################################################################

banner "CONFIGURING CLUSTER"

ip route add "$CLUSTER_NET" \
    dev "$CLUSTER_IF" \
    src "$CLUSTER_IP" \
    table "$CLUSTER_TABLE"


###############################################################################
# ADD BACKEND SUBNET PRIORITY RULE
#
# THIS IS THE CRITICAL RULE.
#
# It ensures traffic to 10.101.30.0/23 always uses the backend
# routing table BEFORE the source-based frontend rule can interfere.
###############################################################################

banner "CONFIGURING BACKEND SUBNET PRIORITY RULE"

ip rule add priority 92 \
    to "$BACKEND_NET" \
    lookup "$BACKEND_TABLE"

echo "Priority 92 backend subnet rule configured."


###############################################################################
# SOURCE-BASED POLICY ROUTING
###############################################################################

banner "CONFIGURING SOURCE-BASED POLICY ROUTING"

ip rule add priority 100 \
    from "$FRONTEND_IP" \
    lookup "$FRONTEND_TABLE"

ip rule add priority 200 \
    from "$MIDDLEEND_IP" \
    lookup "$MIDDLEEND_TABLE"

ip rule add priority 300 \
    from "$BACKEND_IP" \
    lookup "$BACKEND_TABLE"

ip rule add priority 400 \
    from "$CLUSTER_IP" \
    lookup "$CLUSTER_TABLE"


###############################################################################
# MIDDLEEND DESTINATIONS
###############################################################################

banner "CONFIGURING MIDDLEEND DESTINATIONS"

MIDDLEEND_DESTINATIONS=(
    "10.130.2.0/23"
    "10.130.4.0/23"
    "10.130.6.0/23"
    "10.130.8.0/23"
    "10.130.12.0/23"
    "10.130.26.0/23"
)

PRIORITY=501

for NETWORK in "${MIDDLEEND_DESTINATIONS[@]}"; do

    ip rule add priority "$PRIORITY" \
        to "$NETWORK" \
        lookup "$MIDDLEEND_TABLE"

    PRIORITY=$((PRIORITY + 1))

done


###############################################################################
# BACKEND DESTINATIONS
###############################################################################

banner "CONFIGURING BACKEND DESTINATIONS"

BACKEND_DESTINATIONS=(
    "10.101.0.0/23"
    "10.101.2.0/23"
    "10.101.4.0/23"
    "10.101.6.0/23"
    "10.120.0.0/23"
    "10.102.2.0/23"
    "10.102.4.0/23"
    "10.102.6.0/23"
)

PRIORITY=601

for NETWORK in "${BACKEND_DESTINATIONS[@]}"; do

    ip rule add priority "$PRIORITY" \
        to "$NETWORK" \
        lookup "$BACKEND_TABLE"

    PRIORITY=$((PRIORITY + 1))

done


###############################################################################
# CLEAR ROUTE CACHE / NEIGHBOR CACHE
###############################################################################

banner "CLEARING NETWORK CACHES"

ip route flush cache 2>/dev/null || true

ip neigh flush dev "$BACKEND_IF" 2>/dev/null || true


###############################################################################
# FINAL BOND STATUS
###############################################################################

banner "FINAL BOND STATUS"

cat "/proc/net/bonding/${BACKEND_IF}"


###############################################################################
# POLICY ROUTING
###############################################################################

banner "POLICY ROUTING"

ip rule show


###############################################################################
# BACKEND ROUTING TABLE
###############################################################################

banner "BACKEND ROUTING TABLE"

ip route show table "$BACKEND_TABLE"


###############################################################################
# BACKEND GATEWAY ROUTE TEST
###############################################################################

banner "BACKEND GATEWAY ROUTE TEST"

ip route get "$BACKEND_GW"

echo

ip route get "$BACKEND_GW" from "$BACKEND_IP"


###############################################################################
# BACKEND GATEWAY CONNECTIVITY TEST
###############################################################################

banner "BACKEND GATEWAY TEST"

echo "Testing explicitly through bond2..."

ping -I "$BACKEND_IF" -c 5 "$BACKEND_GW" || true


###############################################################################
# NORMAL ROUTING TEST
###############################################################################

banner "NORMAL BACKEND ROUTING TEST"

echo "Expected result:"
echo "${BACKEND_GW} dev ${BACKEND_IF} table ${BACKEND_TABLE}"

echo

ip route get "$BACKEND_GW"


###############################################################################
# NORMAL PING TEST
###############################################################################

banner "NORMAL BACKEND GATEWAY PING TEST"

ping -c 5 "$BACKEND_GW" || true


###############################################################################
# FINAL RESULT
###############################################################################

banner "CONFIGURATION COMPLETED"

echo "Hostname:       ${HOSTNAME_SHORT}"
echo "Node number:    ${NODE_NUMBER}"
echo "Host octet:     ${HOST_OCTET}"
echo
echo "Frontend IP:    ${FRONTEND_IP}"
echo "Middleend IP:   ${MIDDLEEND_IP}"
echo "Backend IP:     ${BACKEND_IP}"
echo "Cluster IP:     ${CLUSTER_IP}"
echo
echo "Backend bond:   ${BACKEND_IF}"
echo "Bond mode:      IEEE 802.3ad / LACP"
echo
echo "IMPORTANT:"
echo "The backend subnet rule at priority 92 ensures that"
echo "${BACKEND_NET} is always routed through the backend"
echo "routing table."
