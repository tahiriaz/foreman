#!/bin/bash
#
# ============================================================================
# Pacemaker NVR VIP + NFS Constraint Rebuild Script
# ============================================================================
#
# Run BEFORE Picata/configuration-updater deployment.
#
# Manages ONLY:
#   - CORE group <-> VIP colocation
#   - NFSREC <-> VIP colocation
#   - CORE -> NFSREC ordering
#   - VIP <-> VIP anti-colocation
#
# Picata and configuration-updater resources do NOT need to exist.
#
# Existing constraints are identified by their RESOURCE RELATIONSHIP,
# not by their Pacemaker-generated constraint ID.
#
# ============================================================================

set -Eeuo pipefail
umask 077

LOG_FILE="/var/log/constraints-vip-nfs-rebuild.log"
BACKUP_DIR="/root/cib-backups"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP_FILE="${BACKUP_DIR}/cib-before-vip-nfs-constraints-${TIMESTAMP}.xml"
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

# ---------------------------------------------------------------------------
# 0. Validate required commands
# ---------------------------------------------------------------------------

for cmd in pcs cibadmin python3; do
    command -v "$cmd" >/dev/null 2>&1 ||
        die "Required command not found: $cmd"
done

[[ $EUID -eq 0 ]] ||
    die "Run this script as root."

# ---------------------------------------------------------------------------
# 1. Start
# ---------------------------------------------------------------------------

log "============================================================"
log "Pacemaker NVR VIP + NFS constraint rebuild"
log "============================================================"
log "This script is intended to run BEFORE Picata deployment."

# ---------------------------------------------------------------------------
# 2. Temporary files
# ---------------------------------------------------------------------------

CIB_XML="$(mktemp /tmp/nvr-cib.XXXXXX.xml)"
DISCOVERY_FILE="$(mktemp /tmp/nvr-discovery.XXXXXX)"
CONSTRAINT_XML="$(mktemp /tmp/nvr-constraints.XXXXXX.xml)"

trap 'rm -f "$CIB_XML" "$DISCOVERY_FILE" "$CONSTRAINT_XML"' EXIT

# ---------------------------------------------------------------------------
# 3. Capture live CIB
# ---------------------------------------------------------------------------

cibadmin --query > "$CIB_XML" ||
    die "Could not retrieve the live CIB."

[[ -s "$CIB_XML" ]] ||
    die "The retrieved CIB is empty."

# ---------------------------------------------------------------------------
# 4. Discover VIP, CORE and NFS only
#
#    Picata and configuration-updater are deliberately ignored.
# ---------------------------------------------------------------------------

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
    sys.stderr.write(
        "Cannot parse CIB XML: %s\n" % exc
    )
    sys.exit(1)

resources_root = root.find("./configuration/resources")

if resources_root is None:
    sys.stderr.write(
        "CIB has no configuration/resources section.\n"
    )
    sys.exit(1)

primitives = {}
groups = {}


def walk(parent, parent_group=None):

    for child in list(parent):

        tag = child.tag.split("}")[-1]

        if tag == "group":

            gid = child.get("id")

            if gid:
                groups[gid] = child
                walk(child, gid)

        elif tag in ("clone", "master"):

            walk(child, parent_group)

        elif tag == "primitive":

            rid = child.get("id")

            if rid:
                primitives[rid] = {
                    "xml": child,
                    "group": parent_group
                }


walk(resources_root)


def agent(primitive):
    return (
        primitive.get("class", ""),
        primitive.get("provider", ""),
        primitive.get("type", "")
    )


# ---------------------------------------------------------------------------
# Discover clusters from VIP resources
# ---------------------------------------------------------------------------

clusters = set()

for rid, info in primitives.items():

    if not rid.endswith("-vip"):
        continue

    cls, provider, typ = agent(info["xml"])

    if (
        cls == "ocf"
        and provider == "heartbeat"
        and typ == "IPaddr2"
    ):

        cluster = rid[:-4]

        if re.match(r"^clnvrm[0-9]+$", cluster):
            clusters.add(cluster)


clusters = sorted(clusters)

if not clusters:

    sys.stderr.write(
        "No NVR VIP resources found matching the supplied naming pattern.\n"
    )

    sys.exit(1)


output = []


# ---------------------------------------------------------------------------
# Validate every cluster
# ---------------------------------------------------------------------------

for cluster in clusters:

    vip = cluster + "-vip"
    core = "rg-" + cluster + "-core"

    # -----------------------------------------------------------------------
    # Validate VIP
    # -----------------------------------------------------------------------

    if vip not in primitives:

        sys.stderr.write(
            "Missing VIP resource: %s\n" % vip
        )

        sys.exit(1)

    # -----------------------------------------------------------------------
    # Validate CORE group
    # -----------------------------------------------------------------------

    if core not in groups:

        sys.stderr.write(
            "Missing expected CORE group: %s\n" % core
        )

        sys.exit(1)

    core_members = [
        resource_id
        for resource_id, info in primitives.items()
        if info["group"] == core
    ]

    if not core_members:

        sys.stderr.write(
            "CORE group %s has no direct primitive members.\n"
            % core
        )

        sys.exit(1)

    # -----------------------------------------------------------------------
    # Discover NFSREC resources
    # -----------------------------------------------------------------------

    nfs_pattern = re.compile(
        r"^" + re.escape(cluster) + r"-nfsrec([0-9]+)$"
    )

    nfs = []

    for rid, info in primitives.items():

        match = nfs_pattern.match(rid)

        if not match:
            continue

        cls, provider, typ = agent(info["xml"])

        if (
            cls == "ocf"
            and provider == "heartbeat"
            and typ == "Filesystem"
        ):

            nfs.append(
                (
                    int(match.group(1)),
                    rid
                )
            )

    nfs.sort()

    # -----------------------------------------------------------------------
    # Exactly four NFS resources are required
    # -----------------------------------------------------------------------

    if len(nfs) != 4:

        sys.stderr.write(
            "%s: expected exactly 4 NFSREC Filesystem resources; "
            "found %d.\n"
            % (
                cluster,
                len(nfs)
            )
        )

        sys.exit(1)

    numbers = [
        number
        for number, rid in nfs
    ]

    if numbers != [1, 2, 3, 4]:

        sys.stderr.write(
            "%s: NFSREC numbering must be 01, 02, 03, 04; "
            "found %s.\n"
            % (
                cluster,
                numbers
            )
        )

        sys.exit(1)

    nfs_ids = [
        rid
        for number, rid in nfs
    ]

    output.append(
        "|".join(
            [
                cluster,
                vip,
                core,
                ",".join(nfs_ids)
            ]
        )
    )


# ---------------------------------------------------------------------------
# Write discovery file
# ---------------------------------------------------------------------------

with open(output_path, "w") as handle:

    handle.write(
        "\n".join(output) + "\n"
    )


print(
    "Discovered and validated %d NVR clusters."
    % len(output)
)


for line in output:

    fields = line.split("|")

    print(
        "%s: VIP=%s CORE=%s NFSREC=%d"
        % (
            fields[0],
            fields[1],
            fields[2],
            len(fields[3].split(","))
        )
    )

PYTHON

[[ -s "$DISCOVERY_FILE" ]] ||
    die "Resource discovery returned no results."

# ---------------------------------------------------------------------------
# 5. Display discovery results
# ---------------------------------------------------------------------------

log "This script will rebuild ONLY VIP + CORE + NFS constraints."
log "Picata/configuration-updater resources are NOT required."
log "Picata/configuration-updater constraints will NOT be modified."

log "Discovered NVR clusters:"

cat "$DISCOVERY_FILE"

# ---------------------------------------------------------------------------
# 6. Confirmation
# ---------------------------------------------------------------------------

if [[ "$AUTO_CONFIRM" != "YES" ]]; then

    echo

    read -r -p \
        "Type YES to back up the CIB and rebuild VIP/CORE/NFS constraints: " \
        ANSWER

    [[ "$ANSWER" == "YES" ]] ||
        die "Cancelled by operator."

fi

# ---------------------------------------------------------------------------
# 7. Back up CIB
# ---------------------------------------------------------------------------

log "Creating CIB backup: $BACKUP_FILE"

pcs cluster cib "$BACKUP_FILE" ||
    die "Failed to create CIB backup."

[[ -s "$BACKUP_FILE" ]] ||
    die "CIB backup file is empty."

chmod 600 "$BACKUP_FILE"

log "CIB backup completed."

# ---------------------------------------------------------------------------
# 8. Delete existing VIP/NFS constraints
#
#    IMPORTANT:
#    We identify constraints by RESOURCE RELATIONSHIP rather than ID.
#
#    This handles both:
#
#      col-clnvrm071-core-vip
#
#    and Pacemaker-generated IDs such as:
#
#      colocation-rg-clnvrm071-core-clnvrm071-vip-INFINITY
#
# ---------------------------------------------------------------------------

log "Deleting only VIP + NFS constraints managed by this script..."

cibadmin --query --scope constraints > "$CONSTRAINT_XML" ||
    die "Could not retrieve current constraints."

mapfile -t CONSTRAINT_IDS < <(
    python3 - "$CONSTRAINT_XML" "$DISCOVERY_FILE" <<'PYTHON'
from __future__ import print_function

import sys
import xml.etree.ElementTree as ET


constraints_path = sys.argv[1]
discovery_path = sys.argv[2]


root = ET.parse(constraints_path).getroot()


# ---------------------------------------------------------------------------
# Read resources belonging to this script
# ---------------------------------------------------------------------------

clusters = []
vips = set()
cores = set()
nfs_by_cluster = {}


with open(discovery_path) as handle:

    for line in handle:

        line = line.strip()

        if not line:
            continue

        cluster, vip, core, nfs_csv = line.split("|")

        clusters.append(cluster)
        vips.add(vip)
        cores.add(core)

        nfs_by_cluster[cluster] = set(
            nfs_csv.split(",")
        )


# ---------------------------------------------------------------------------
# Helper: determine whether this is a colocation relationship
# ---------------------------------------------------------------------------

def is_colocation(element, resource_a, resource_b):

    if element.tag.split("}")[-1] != "rsc_colocation":
        return False

    rsc = element.get("rsc")
    with_rsc = element.get("with-rsc")

    return (
        (rsc == resource_a and with_rsc == resource_b)
        or
        (rsc == resource_b and with_rsc == resource_a)
    )


# ---------------------------------------------------------------------------
# Helper: determine whether this is a normal ordering relationship
# ---------------------------------------------------------------------------

def is_order(element, first, then):

    if element.tag.split("}")[-1] != "rsc_order":
        return False

    return (
        element.get("first") == first
        and
        element.get("then") == then
    )


# ---------------------------------------------------------------------------
# Helper: VIP anti-colocation
#
# We only remove a negative colocation where BOTH resources are NVR VIPs.
# ---------------------------------------------------------------------------

def is_vip_anti_colocation(element):

    if element.tag.split("}")[-1] != "rsc_colocation":
        return False

    if element.get("score") != "-INFINITY":
        return False

    rsc = element.get("rsc")
    with_rsc = element.get("with-rsc")

    return (
        rsc in vips
        and
        with_rsc in vips
    )


# ---------------------------------------------------------------------------
# Identify constraints to remove
# ---------------------------------------------------------------------------

for element in list(root):

    constraint_id = element.get("id")

    if not constraint_id:
        continue

    remove = False

    for cluster in clusters:

        vip = cluster + "-vip"
        core = "rg-" + cluster + "-core"

        # ---------------------------------------------------------------
        # CORE <-> VIP
        # ---------------------------------------------------------------

        if is_colocation(
            element,
            core,
            vip
        ):
            remove = True

        # ---------------------------------------------------------------
        # NFSREC <-> VIP
        # ---------------------------------------------------------------

        for nfs in nfs_by_cluster[cluster]:

            if is_colocation(
                element,
                nfs,
                vip
            ):
                remove = True

            # -----------------------------------------------------------
            # CORE -> NFSREC
            # -----------------------------------------------------------

            if is_order(
                element,
                core,
                nfs
            ):
                remove = True

    # -------------------------------------------------------------------
    # VIP <-> VIP anti-colocation
    # -------------------------------------------------------------------

    if is_vip_anti_colocation(element):

        remove = True

    if remove:

        print(constraint_id)

PYTHON
)

# ---------------------------------------------------------------------------
# 9. Delete identified constraints
# ---------------------------------------------------------------------------

for cid in "${CONSTRAINT_IDS[@]}"; do

    log "Deleting VIP/NFS constraint: $cid"

    pcs constraint delete "$cid" ||
        die "Failed to delete constraint $cid"

done

log "VIP/NFS constraints deleted: ${#CONSTRAINT_IDS[@]}"

# ---------------------------------------------------------------------------
# 10. Rebuild VIP + CORE + NFS constraints
# ---------------------------------------------------------------------------

declare -a CLUSTERS=()
declare -A VIPS=()


while IFS='|' read -r cluster vip core nfs_csv; do

    [[ -n "$cluster" ]] ||
        continue

    CLUSTERS+=("$cluster")

    VIPS["$cluster"]="$vip"

    log "------------------------------------------------------------"
    log "Building VIP/NFS constraints for $cluster"
    log "VIP: $vip"
    log "CORE: $core"
    log "NFSREC: $nfs_csv"
    log "------------------------------------------------------------"

    # -----------------------------------------------------------------------
    # CORE <-> VIP
    # -----------------------------------------------------------------------

    pcs constraint colocation add \
        "$core" \
        with "$vip" \
        INFINITY \
        id="col-${cluster}-core-vip" ||
        die "Failed CORE/VIP colocation for $cluster"

    # -----------------------------------------------------------------------
    # NFSREC <-> VIP
    # CORE -> NFSREC
    # -----------------------------------------------------------------------

    IFS=',' read -r -a nfs_array <<< "$nfs_csv"

    for nfs in "${nfs_array[@]}"; do

        pcs constraint colocation add \
            "$nfs" \
            with "$vip" \
            INFINITY \
            id="col-${cluster}-${nfs}-vip" ||
            die "Failed NFSREC/VIP colocation for $nfs"

        pcs constraint order \
            start "$core" \
            then start "$nfs" \
            kind=Mandatory \
            id="ord-${cluster}-core-${nfs}" ||
            die "Failed CORE/NFSREC ordering for $nfs"

    done

done < "$DISCOVERY_FILE"

# ---------------------------------------------------------------------------
# 11. Pairwise VIP anti-colocation
#
# IMPORTANT:
#   "--" tells pcs that -INFINITY is an argument/value, not an option.
# ---------------------------------------------------------------------------

log "Creating pairwise anti-colocation constraints between NVR VIPs..."

for ((i = 0; i < ${#CLUSTERS[@]}; i++)); do

    for ((j = i + 1; j < ${#CLUSTERS[@]}; j++)); do

        cluster_a="${CLUSTERS[$i]}"
        cluster_b="${CLUSTERS[$j]}"

        vip_a="${VIPS[$cluster_a]}"
        vip_b="${VIPS[$cluster_b]}"

        log "Anti-colocating $vip_a and $vip_b"

        pcs constraint colocation add \
            "$vip_a" \
            with "$vip_b" \
            -- \
            -INFINITY \
            id="anti-${cluster_a}-${cluster_b}" ||
            die "Failed anti-colocation between $cluster_a and $cluster_b"

    done

done

# ---------------------------------------------------------------------------
# 12. Final verification
# ---------------------------------------------------------------------------

log "VIP + NFS constraint rebuild completed."

log "Displaying current constraints..."

pcs constraint config ||
    die "Unable to display rebuilt constraints."

log "============================================================"
log "NVR VIP + NFS constraint rebuild completed successfully."
log "CIB backup: $BACKUP_FILE"
log "Log file: $LOG_FILE"
log "============================================================"