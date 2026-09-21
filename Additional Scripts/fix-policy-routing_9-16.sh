#!/bin/bash
#
# fix-policy-routing_9-16.sh
#
# Policy Based Routing configuration
# TVS NVR Blades 9 through 16
#

set -u

echo "========================================="
echo " Policy Routing Fix - Blades 9 to 16"
echo "========================================="
echo

# --------------------------------------------------
# Root check
# --------------------------------------------------

if [ "$(id -u)" -ne 0 ]; then
    echo "ERROR: This script must be run as root."
    exit 1
fi

# --------------------------------------------------
# Check interfaces
# --------------------------------------------------

for IFACE in vlan126 vlan128 vlan144 bond2; do

    if ! ip link show "$IFACE" >/dev/null 2>&1; then
        echo "ERROR: Interface $IFACE does not exist."
        exit 1
    fi

done

# --------------------------------------------------
# Get IP addresses
# --------------------------------------------------

FRONTEND_IP=$(ip -4 -o addr show vlan126 | awk '{print $4}' | cut -d/ -f1 | head -1)
MIDDLEEND_IP=$(ip -4 -o addr show vlan128 | awk '{print $4}' | cut -d/ -f1 | head -1)
CLUSTER_IP=$(ip -4 -o addr show vlan144 | awk '{print $4}' | cut -d/ -f1 | head -1)
BACKEND_IP=$(ip -4 -o addr show bond2 | awk '{print $4}' | cut -d/ -f1 | head -1)

echo "Detected IP addresses:"
echo "-----------------------------------------"
echo "Frontend  vlan126 : $FRONTEND_IP"
echo "Middleend vlan128 : $MIDDLEEND_IP"
echo "Cluster   vlan144 : $CLUSTER_IP"
echo "Backend   bond2   : $BACKEND_IP"
echo

if [ -z "$FRONTEND_IP" ] || \
   [ -z "$MIDDLEEND_IP" ] || \
   [ -z "$CLUSTER_IP" ] || \
   [ -z "$BACKEND_IP" ]; then

    echo "ERROR: Could not detect all interface IP addresses."
    exit 1

fi

# --------------------------------------------------
# Gateways
# --------------------------------------------------

FRONTEND_GW="10.101.26.1"
MIDDLEEND_GW="10.101.28.1"
BACKEND_GW="10.101.30.1"

# --------------------------------------------------
# Network prefixes
# --------------------------------------------------

FRONTEND_NET="10.101.26.0/23"
MIDDLEEND_NET="10.101.28.0/23"
CLUSTER_NET="10.101.44.0/23"
BACKEND_NET="10.101.30.0/23"

# --------------------------------------------------
# Ensure rt_tables entries
# --------------------------------------------------

echo "Checking routing table definitions..."

grep -qE '^100[[:space:]]+frontend$' /etc/iproute2/rt_tables || \
echo "100 frontend" >> /etc/iproute2/rt_tables

grep -qE '^200[[:space:]]+middleend$' /etc/iproute2/rt_tables || \
echo "200 middleend" >> /etc/iproute2/rt_tables

grep -qE '^300[[:space:]]+backend$' /etc/iproute2/rt_tables || \
echo "300 backend" >> /etc/iproute2/rt_tables

grep -qE '^400[[:space:]]+cluster$' /etc/iproute2/rt_tables || \
echo "400 cluster" >> /etc/iproute2/rt_tables

# --------------------------------------------------
# CONFIGURE NETWORKMANAGER
# --------------------------------------------------

echo
echo "========================================="
echo " Configuring NetworkManager"
echo "========================================="

# --------------------------------------------------
# VLAN126 - FRONTEND
# --------------------------------------------------

echo "Configuring vlan126..."

nmcli connection modify vlan126 ipv4.never-default yes

nmcli connection modify vlan126 ipv4.routes \
"${FRONTEND_NET} table=100, \
0.0.0.0/0 ${FRONTEND_GW} table=100"

nmcli connection modify vlan126 ipv4.routing-rules \
"priority 100 from ${FRONTEND_IP}/32 table 100"

# --------------------------------------------------
# VLAN128 - MIDDLEEND
# --------------------------------------------------

echo "Configuring vlan128..."

nmcli connection modify vlan128 ipv4.never-default yes

nmcli connection modify vlan128 ipv4.routes \
"${MIDDLEEND_NET} table=200, \
0.0.0.0/0 ${MIDDLEEND_GW} table=200"

nmcli connection modify vlan128 ipv4.routing-rules \
"priority 200 from ${MIDDLEEND_IP}/32 table 200, \
priority 501 to 10.130.2.0/23 table 200, \
priority 502 to 10.130.4.0/23 table 200, \
priority 503 to 10.130.6.0/23 table 200, \
priority 504 to 10.130.8.0/23 table 200, \
priority 505 to 10.130.12.0/23 table 200, \
priority 506 to 10.130.26.0/23 table 200"

# --------------------------------------------------
# VLAN144 - CLUSTER
# --------------------------------------------------

echo "Configuring vlan144..."

nmcli connection modify vlan144 ipv4.never-default yes

nmcli connection modify vlan144 ipv4.routes \
"${CLUSTER_NET} table=400"

nmcli connection modify vlan144 ipv4.routing-rules \
"priority 210 from ${CLUSTER_IP}/32 table 400"

# --------------------------------------------------
# BOND2 - BACKEND
# --------------------------------------------------

echo "Configuring bond2..."

nmcli connection modify bond2 ipv4.never-default yes

nmcli connection modify bond2 ipv4.routes \
"${BACKEND_NET} table=300, \
0.0.0.0/0 ${BACKEND_GW} table=300"

nmcli connection modify bond2 ipv4.routing-rules \
"priority 300 from ${BACKEND_IP}/32 table 300, \
priority 601 to 10.101.0.0/23 table 300, \
priority 602 to 10.101.2.0/23 table 300, \
priority 603 to 10.101.4.0/23 table 300, \
priority 604 to 10.101.6.0/23 table 300, \
priority 605 to 10.120.0.0/23 table 300, \
priority 606 to 10.102.2.0/23 table 300, \
priority 607 to 10.102.4.0/23 table 300, \
priority 608 to 10.102.6.0/23 table 300"

# --------------------------------------------------
# REMOVE BAD RUNTIME RULES
# --------------------------------------------------

echo
echo "========================================="
echo " Cleaning Runtime Policy Rules"
echo "========================================="

# Remove old rules completely.
# NetworkManager will recreate the correct rules.

for PRIORITY in \
9999 \
100 \
200 \
210 \
300 \
501 502 503 504 505 506 \
601 602 603 604 605 606 607 608
do

    while ip rule show | grep -q "^${PRIORITY}:"; do
        ip rule del priority "$PRIORITY" 2>/dev/null || break
    done

done

# --------------------------------------------------
# REMOVE OLD POLICY TABLE ROUTES
# --------------------------------------------------

echo
echo "Flushing old policy routing tables..."

ip route flush table 100 2>/dev/null || true
ip route flush table 200 2>/dev/null || true
ip route flush table 300 2>/dev/null || true
ip route flush table 400 2>/dev/null || true

ip route flush cache

# --------------------------------------------------
# RELOAD NETWORKMANAGER
# --------------------------------------------------

echo
echo "========================================="
echo " Reloading NetworkManager Configuration"
echo "========================================="

nmcli connection reload

# Reapply the connections

nmcli device reapply vlan126 || true
nmcli device reapply vlan128 || true
nmcli device reapply vlan144 || true
nmcli device reapply bond2 || true

sleep 5

ip route flush cache

# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

echo
echo "========================================="
echo " FINAL POLICY RULES"
echo "========================================="

ip rule show

echo
echo "========================================="
echo " FRONTEND TABLE (100)"
echo "========================================="

ip route show table 100

echo
echo "========================================="
echo " MIDDLEEND TABLE (200)"
echo "========================================="

ip route show table 200

echo
echo "========================================="
echo " BACKEND TABLE (300)"
echo "========================================="

ip route show table 300

echo
echo "========================================="
echo " CLUSTER TABLE (400)"
echo "========================================="

ip route show table 400

echo
echo "========================================="
echo " ROUTE TESTS"
echo "========================================="

echo
echo "10.101.18.27 (iLO network):"
ip route get 10.101.18.27

echo
echo "10.101.28.20 (Middleend):"
ip route get 10.101.28.20

echo
echo "10.101.44.20 (Cluster):"
ip route get 10.101.44.20

echo
echo "10.101.30.1 (Backend gateway):"
ip route get 10.101.30.1

echo
echo "10.101.2.161 (Backend/NFS):"
ip route get 10.101.2.161

echo
echo "========================================="
echo " Configuration Complete"
echo "========================================="
