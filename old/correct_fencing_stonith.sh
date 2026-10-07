#!/bin/bash

# ============================================================
# Update all fence_ilo4 STONITH resources to use:
#
#     privlvl=operator
#
# instead of:
#
#     privlvl=user
#
# Existing resource configuration is preserved.
# ============================================================

set -u

LOG="/var/log/update-stonith-privlvl.log"

exec > >(tee -a "$LOG") 2>&1

echo
echo "============================================================"
echo "STONITH privilege-level update"
echo "Date: $(date)"
echo "Node: $(hostname -f)"
echo "============================================================"
echo

# ------------------------------------------------------------
# Check cluster
# ------------------------------------------------------------

if ! pcs status >/dev/null 2>&1; then
    echo "ERROR: pcs is not available or cluster is not accessible."
    exit 1
fi

# ------------------------------------------------------------
# Get all STONITH resources
# ------------------------------------------------------------

echo "Getting STONITH resources..."
echo

mapfile -t STONITH_RESOURCES < <(
    pcs stonith config |
    awk '/^Resource:/ {
        gsub(/:/, "", $2);
        print $2
    }'
)

if [ "${#STONITH_RESOURCES[@]}" -eq 0 ]; then
    echo "No STONITH resources found."
    exit 0
fi

echo "Found ${#STONITH_RESOURCES[@]} STONITH resource(s):"
printf '  %s\n' "${STONITH_RESOURCES[@]}"
echo

# ------------------------------------------------------------
# Process each resource
# ------------------------------------------------------------

UPDATED=0
SKIPPED=0
FAILED=0

for STONITH in "${STONITH_RESOURCES[@]}"; do

    echo "------------------------------------------------------------"
    echo "Resource: $STONITH"
    echo "------------------------------------------------------------"

    # Get complete resource configuration.
    CONFIG=$(pcs stonith config "$STONITH" 2>/dev/null)

    if [ $? -ne 0 ]; then
        echo "ERROR: Cannot read configuration for $STONITH"
        ((FAILED++))
        continue
    fi

    echo "$CONFIG"

    # --------------------------------------------------------
    # Determine STONITH type
    # --------------------------------------------------------

    TYPE=$(echo "$CONFIG" |
        awk '/Resource:/ {
            for (i=1; i<=NF; i++) {
                if ($i ~ /^type=/) {
                    sub(/^type=/, "", $i)
                    print $i
                }
            }
        }')

    echo
    echo "Type: ${TYPE:-UNKNOWN}"

    # We only want fence_ilo4.
    if [ "$TYPE" != "fence_ilo4" ]; then
        echo "Skipping: not a fence_ilo4 resource."
        ((SKIPPED++))
        continue
    fi

    # --------------------------------------------------------
    # Get current privilege
    # --------------------------------------------------------

    PRIVLVL=$(echo "$CONFIG" |
        awk '
        /Attributes:/ { inattr=1; next }
        inattr && /privlvl=/ {
            match($0, /privlvl=[^ ]+/)
            value=substr($0, RSTART+8, RLENGTH-8)
            print value
            exit
        }')

    echo "Current privlvl: ${PRIVLVL:-NOT SET}"

    # --------------------------------------------------------
    # Already correct
    # --------------------------------------------------------

    if [ "$PRIVLVL" = "operator" ]; then
        echo "Already configured as operator."
        ((SKIPPED++))
        continue
    fi

    # --------------------------------------------------------
    # Update
    # --------------------------------------------------------

    echo
    echo "Updating $STONITH:"
    echo "    privlvl=$PRIVLVL"
    echo " -> privlvl=operator"
    echo

    if pcs stonith update "$STONITH" privlvl=operator; then

        echo "SUCCESS: $STONITH updated."
        ((UPDATED++))

    else

        echo "ERROR: Failed to update $STONITH."
        ((FAILED++))
        continue

    fi

    # --------------------------------------------------------
    # Verify
    # --------------------------------------------------------

    echo
    echo "Verifying configuration..."

    VERIFY=$(pcs stonith config "$STONITH" 2>/dev/null)

    if echo "$VERIFY" | grep -q 'privlvl=operator'; then

        echo "VERIFIED: privlvl=operator"

    else

        echo "ERROR: Verification failed!"
        ((FAILED++))
    fi

done

# ------------------------------------------------------------
# Final summary
# ------------------------------------------------------------

echo
echo "============================================================"
echo "SUMMARY"
echo "============================================================"

echo "STONITH resources found : ${#STONITH_RESOURCES[@]}"
echo "Updated                 : $UPDATED"
echo "Already correct/skipped : $SKIPPED"
echo "Failed                  : $FAILED"

echo "============================================================"
echo

if [ "$FAILED" -gt 0 ]; then
    exit 1
fi

exit 0