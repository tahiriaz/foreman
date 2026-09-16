#!/bin/bash
#
# ============================================================================
# Pacemaker Constraint Rebuild Script
# ============================================================================
#
# Purpose:
#   1. Delete ALL existing Pacemaker constraints
#   2. Recreate the required constraints for a group of NVR services
#   3. Ensure each service CORE group runs on a different node
#   4. Ensure each service VIP runs on the same node as its CORE group
#   5. Ensure all NFSREC resources run on the same node as their CORE group
#   6. Verify the final number of constraints
#
# Supported site naming:
#   SITE="M"  -> CLNVRMxxx
#   SITE="R"  -> CLNVRRxxx
#
# ============================================================================
# Constraint architecture
# ============================================================================
#
# For each service:
#
#                  CORE
#                   |
#          +--------+--------+
#          |        |        |
#       NFSREC01 NFSREC02 NFSREC03 NFSREC04
#                   |
#                  VIP
#
# 1. Ordering:
#
#      CORE -> NFSREC01
#      CORE -> NFSREC02
#      CORE -> NFSREC03
#      CORE -> NFSREC04
#
# 2. Colocation:
#
#      NFSREC01 with CORE
#      NFSREC02 with CORE
#      NFSREC03 with CORE
#      NFSREC04 with CORE
#      VIP     with CORE
#
# 3. CORE anti-colocation:
#
#      CORE011 != CORE012
#      CORE011 != CORE013
#      ...
#      CORE016 != CORE017
#
#    This guarantees that two different services cannot run their CORE
#    resource groups on the same node.
#
# 4. VIP anti-colocation:
#
#      VIP011 != VIP012
#      VIP011 != VIP013
#      ...
#
#    This explicitly guarantees that two VIPs cannot run on the same node.
#
# ============================================================================
# Constraint count for N services
# ============================================================================
#
# Per service:
#
#      4 ordering
#      4 NFSREC -> CORE colocation
#      1 VIP -> CORE colocation
#
#      = 9 per service
#
# CORE anti-colocation:
#
#      N * (N - 1) / 2
#
# VIP anti-colocation:
#
#      N * (N - 1) / 2
#
# Total:
#
#      N*9 + 2*(N*(N-1)/2)
#
#      = N*9 + N*(N-1)
#
#      = N*(N+8)
#
# For 7 services:
#
#      7 * 15 = 105 constraints
#
# ============================================================================


# ============================================================================
# USER CONFIGURATION
# ============================================================================

SITE="M"

CLUSTER_BASE="010"

START=1
END=7


# ============================================================================
# BASIC VALIDATION
# ============================================================================

echo
echo "============================================================"
echo " Pacemaker Constraint Rebuild"
echo "============================================================"
echo

if [[ "$SITE" != "M" && "$SITE" != "R" ]]; then
    echo "ERROR: SITE must be either M or R."
    echo "Current value: $SITE"
    exit 1
fi

if ! [[ "$CLUSTER_BASE" =~ ^[0-9]{3}$ ]]; then
    echo "ERROR: CLUSTER_BASE must contain exactly 3 digits."
    echo "Example: 000, 010, 020, 030"
    echo "Current value: $CLUSTER_BASE"
    exit 1
fi

if ! [[ "$START" =~ ^[0-9]+$ ]]; then
    echo "ERROR: START must be a positive integer."
    exit 1
fi

if ! [[ "$END" =~ ^[0-9]+$ ]]; then
    echo "ERROR: END must be a positive integer."
    exit 1
fi

if (( START > END )); then
    echo "ERROR: START cannot be greater than END."
    exit 1
fi


# ============================================================================
# CONVERT CLUSTER_BASE TO DECIMAL
# ============================================================================

BASE_NUMBER=$((10#$CLUSTER_BASE))

CLUSTER_COUNT=$((END - START + 1))


# ============================================================================
# DISPLAY CONFIGURATION
# ============================================================================

echo "Site              : $SITE"
echo "Cluster base      : $CLUSTER_BASE"
echo "Base number       : $BASE_NUMBER"
echo "Resource range    : $START - $END"
echo "Number of services: $CLUSTER_COUNT"
echo

echo "Resources that will be configured:"
echo

for i in $(seq "$START" "$END"); do

    RESOURCE_NUMBER=$((BASE_NUMBER + i))

    ID=$(printf "%03d" "$RESOURCE_NUMBER")

    RESOURCE="clnvr${SITE,,}${ID}"
    CORE="rg-${RESOURCE}-core"
    VIP="${RESOURCE}-vip"

    echo "  $RESOURCE"
    echo "      CORE : $CORE"
    echo "      VIP  : $VIP"

done

echo


# ============================================================================
# CONFIRM CONFIGURATION
# ============================================================================

echo "WARNING:"
echo "This script will DELETE ALL existing Pacemaker constraints."
echo
echo "The following constraints will then be created:"
echo
echo "  - CORE -> NFSREC ordering"
echo "  - NFSREC with CORE colocation"
echo "  - VIP with CORE colocation"
echo "  - CORE anti-colocation between services"
echo "  - VIP anti-colocation between services"
echo

read -r -p "Continue and rebuild ALL constraints? [yes/no]: " CONFIRM

if [[ "$CONFIRM" != "yes" ]]; then
    echo
    echo "Aborted."
    exit 0
fi

echo


# ============================================================================
# CHECK PCS
# ============================================================================

if ! command -v pcs >/dev/null 2>&1; then
    echo "ERROR: pcs command not found."
    exit 1
fi


# ============================================================================
# STEP 1 - DISPLAY CURRENT CONSTRAINTS
# ============================================================================

echo
echo "============================================================"
echo " STEP 1 - Current Constraints"
echo "============================================================"
echo

pcs constraint config --full

echo


# ============================================================================
# STEP 2 - EXTRACT ALL CONSTRAINT IDs
# ============================================================================

echo
echo "============================================================"
echo " STEP 2 - Extract Existing Constraint IDs"
echo "============================================================"
echo

CONSTRAINT_IDS=$(pcs constraint config --full \
    | sed -nE 's/.*\(id:[[:space:]]*([^)]*)\).*/\1/p' \
    | sort -u)

if [[ -z "$CONSTRAINT_IDS" ]]; then

    echo "No existing constraints found."

else

    echo "Existing constraint IDs:"
    echo
    echo "$CONSTRAINT_IDS"

fi

echo


# ============================================================================
# STEP 3 - DELETE ALL EXISTING CONSTRAINTS
# ============================================================================

echo
echo "============================================================"
echo " STEP 3 - Delete Existing Constraints"
echo "============================================================"
echo

if [[ -z "$CONSTRAINT_IDS" ]]; then

    echo "Nothing to delete."

else

    DELETE_COUNT=0

    while IFS= read -r CONSTRAINT_ID; do

        [[ -z "$CONSTRAINT_ID" ]] && continue

        echo "Deleting constraint:"
        echo "  $CONSTRAINT_ID"

        if pcs constraint delete "$CONSTRAINT_ID"; then

            DELETE_COUNT=$((DELETE_COUNT + 1))

        else

            echo
            echo "ERROR: Failed to delete constraint:"
            echo "  $CONSTRAINT_ID"
            exit 1

        fi

    done <<< "$CONSTRAINT_IDS"

    echo
    echo "Deleted constraints: $DELETE_COUNT"

fi

echo


# ============================================================================
# STEP 4 - VERIFY THAT NO CONSTRAINTS REMAIN
# ============================================================================

echo
echo "============================================================"
echo " STEP 4 - Verify Constraint Cleanup"
echo "============================================================"
echo

REMAINING_IDS=$(pcs constraint config --full \
    | sed -nE 's/.*\(id:[[:space:]]*([^)]*)\).*/\1/p' \
    | sort -u)

if [[ -n "$REMAINING_IDS" ]]; then

    echo "ERROR: Some constraints still exist:"
    echo
    echo "$REMAINING_IDS"
    echo
    exit 1

fi

echo "Constraint cleanup verified."
echo "No existing constraints remain."
echo


# ============================================================================
# STEP 5 - CREATE SERVICE ORDERING AND COLOCATION
# ============================================================================

echo
echo "============================================================"
echo " STEP 5 - Create Service Constraints"
echo "============================================================"
echo


for i in $(seq "$START" "$END"); do

    RESOURCE_NUMBER=$((BASE_NUMBER + i))

    ID=$(printf "%03d" "$RESOURCE_NUMBER")

    RESOURCE="clnvr${SITE,,}${ID}"

    CORE="rg-${RESOURCE}-core"

    VIP="${RESOURCE}-vip"


    echo
    echo "------------------------------------------------------------"
    echo "Service: ${RESOURCE^^}"
    echo "CORE   : $CORE"
    echo "VIP    : $VIP"
    echo "------------------------------------------------------------"
    echo


    # ========================================================================
    # ORDERING
    # ========================================================================

    for r in 01 02 03 04; do

        NFSREC="${RESOURCE}-nfsrec${r}"

        echo "Creating order:"
        echo "  $CORE -> $NFSREC"

        if ! pcs constraint order \
            start "$CORE" \
            then "$NFSREC"; then

            echo
            echo "ERROR creating ordering constraint:"
            echo "  $CORE -> $NFSREC"
            exit 1

        fi

    done


    # ========================================================================
    # NFSREC -> CORE COLOCATION
    # ========================================================================

    for r in 01 02 03 04; do

        NFSREC="${RESOURCE}-nfsrec${r}"

        echo "Creating colocation:"
        echo "  $NFSREC with $CORE"

        if ! pcs constraint colocation add \
            "$NFSREC" \
            with "$CORE" \
            INFINITY; then

            echo
            echo "ERROR creating NFSREC colocation:"
            echo "  $NFSREC with $CORE"
            exit 1

        fi

    done


    # ========================================================================
    # VIP -> CORE COLOCATION
    # ========================================================================

    echo "Creating VIP colocation:"
    echo "  $VIP with $CORE"

    if ! pcs constraint colocation add \
        "$VIP" \
        with "$CORE" \
        INFINITY; then

        echo
        echo "ERROR creating VIP colocation:"
        echo "  $VIP with $CORE"
        exit 1

    fi

done


# ============================================================================
# STEP 6 - CORE ANTI-COLOCATION
# ============================================================================
#
# This is the important addition.
#
# Every CORE group must be on a different node.
#
# Example:
#
#   rg-clnvrm011-core != rg-clnvrm012-core
#
#   rg-clnvrm011-core != rg-clnvrm013-core
#
# etc.
#
# ============================================================================

echo
echo "============================================================"
echo " STEP 6 - Create CORE Anti-Colocation Constraints"
echo "============================================================"
echo


for i in $(seq "$START" "$END"); do

    RESOURCE_NUMBER1=$((BASE_NUMBER + i))

    ID1=$(printf "%03d" "$RESOURCE_NUMBER1")

    RESOURCE1="clnvr${SITE,,}${ID1}"

    CORE1="rg-${RESOURCE1}-core"


    for j in $(seq $((i + 1)) "$END"); do

        RESOURCE_NUMBER2=$((BASE_NUMBER + j))

        ID2=$(printf "%03d" "$RESOURCE_NUMBER2")

        RESOURCE2="clnvr${SITE,,}${ID2}"

        CORE2="rg-${RESOURCE2}-core"


        echo "Creating CORE anti-colocation:"
        echo "  $CORE1 != $CORE2"

        if ! pcs constraint colocation add \
            "$CORE1" \
            with "$CORE2" \
            -INFINITY; then

            echo
            echo "ERROR creating CORE anti-colocation:"
            echo "  $CORE1 != $CORE2"
            exit 1

        fi

    done

done


# ============================================================================
# STEP 7 - VIP ANTI-COLOCATION
# ============================================================================

echo
echo "============================================================"
echo " STEP 7 - Create VIP Anti-Colocation Constraints"
echo "============================================================"
echo


for i in $(seq "$START" "$END"); do

    RESOURCE_NUMBER1=$((BASE_NUMBER + i))

    ID1=$(printf "%03d" "$RESOURCE_NUMBER1")

    RESOURCE1="clnvr${SITE,,}${ID1}"

    VIP1="${RESOURCE1}-vip"


    for j in $(seq $((i + 1)) "$END"); do

        RESOURCE_NUMBER2=$((BASE_NUMBER + j))

        ID2=$(printf "%03d" "$RESOURCE_NUMBER2")

        RESOURCE2="clnvr${SITE,,}${ID2}"

        VIP2="${RESOURCE2}-vip"


        echo "Creating VIP anti-colocation:"
        echo "  $VIP1 != $VIP2"

        if ! pcs constraint colocation add \
            "$VIP1" \
            with "$VIP2" \
            -INFINITY; then

            echo
            echo "ERROR creating VIP anti-colocation:"
            echo "  $VIP1 != $VIP2"
            exit 1

        fi

    done

done


# ============================================================================
# STEP 8 - DISPLAY FINAL CONSTRAINT CONFIGURATION
# ============================================================================

echo
echo "============================================================"
echo " STEP 8 - Final Constraint Configuration"
echo "============================================================"
echo

pcs constraint config --full

echo


# ============================================================================
# STEP 9 - CALCULATE EXPECTED CONSTRAINT COUNT
# ============================================================================

ORDER_COUNT=$((CLUSTER_COUNT * 4))

NFSREC_COUNT=$((CLUSTER_COUNT * 4))

VIP_CORE_COUNT=$CLUSTER_COUNT

CORE_ANTI_COUNT=$((CLUSTER_COUNT * (CLUSTER_COUNT - 1) / 2))

VIP_ANTI_COUNT=$((CLUSTER_COUNT * (CLUSTER_COUNT - 1) / 2))

EXPECTED_TOTAL=$(( \
    ORDER_COUNT \
    + NFSREC_COUNT \
    + VIP_CORE_COUNT \
    + CORE_ANTI_COUNT \
    + VIP_ANTI_COUNT \
))


# ============================================================================
# STEP 10 - COUNT ACTUAL CONSTRAINTS
# ============================================================================

echo
echo "============================================================"
echo " STEP 10 - Constraint Count Verification"
echo "============================================================"
echo

FINAL_CONSTRAINT_IDS=$(pcs constraint config --full \
    | sed -nE 's/.*\(id:[[:space:]]*([^)]*)\).*/\1/p' \
    | sort -u)

if [[ -z "$FINAL_CONSTRAINT_IDS" ]]; then

    ACTUAL_TOTAL=0

else

    ACTUAL_TOTAL=$(printf '%s\n' "$FINAL_CONSTRAINT_IDS" | grep -c '.')

fi


# ============================================================================
# DISPLAY COUNT BREAKDOWN
# ============================================================================

echo "Expected constraint breakdown:"
echo

echo "  Services                  : $CLUSTER_COUNT"
echo
echo "  Ordering constraints      : $ORDER_COUNT"
echo "  NFSREC colocations        : $NFSREC_COUNT"
echo "  VIP -> CORE colocations   : $VIP_CORE_COUNT"
echo "  CORE anti-colocations     : $CORE_ANTI_COUNT"
echo "  VIP anti-colocations      : $VIP_ANTI_COUNT"
echo
echo "  Expected total            : $EXPECTED_TOTAL"
echo "  Actual total              : $ACTUAL_TOTAL"
echo


# ============================================================================
# STEP 11 - FINAL VALIDATION
# ============================================================================

if [[ "$ACTUAL_TOTAL" -eq "$EXPECTED_TOTAL" ]]; then

    echo "============================================================"
    echo " SUCCESS"
    echo "============================================================"
    echo
    echo "Constraint count is correct."
    echo
    echo "Site              : $SITE"
    echo "Cluster base      : $CLUSTER_BASE"
    echo "Resources         : $CLUSTER_COUNT"
    echo "Expected          : $EXPECTED_TOTAL"
    echo "Actual            : $ACTUAL_TOTAL"
    echo
    echo "Pacemaker constraints were rebuilt successfully."
    echo

else

    echo "============================================================"
    echo " ERROR"
    echo "============================================================"
    echo
    echo "Constraint count does NOT match."
    echo
    echo "Expected: $EXPECTED_TOTAL"
    echo "Actual  : $ACTUAL_TOTAL"
    echo
    echo "Review the final constraint configuration above."
    echo

    exit 1

fi


# ============================================================================
# END
# ============================================================================

echo "Script completed."
echo
