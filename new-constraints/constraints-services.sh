#!/bin/bash
#
# Pacemaker NVR Picata + Configuration-Updater Constraint Rebuild Script
#
# Run AFTER Picata and configuration-updater are deployed.
# Manages ONLY:
#   - Picata <-> VIP colocation
#   - NFSREC -> matching Picata ordering
#   - configuration-updater <-> VIP colocation
#   - nfsetc01 -> configuration-updater ordering
#
# Existing VIP/NFS constraints are never modified.
# Existing service constraints are identified by RESOURCE RELATIONSHIP,
# not by Pacemaker-generated constraint ID.
#
set -Eeuo pipefail
umask 077

LOG_FILE="/var/log/constraints-services-rebuild.log"
BACKUP_DIR="/root/cib-backups"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP_FILE="${BACKUP_DIR}/cib-before-services-constraints-${TIMESTAMP}.xml"
AUTO_CONFIRM="${AUTO_CONFIRM:-NO}"

mkdir -p "$BACKUP_DIR"
touch "$LOG_FILE"
chmod 600 "$LOG_FILE"
exec > >(tee -a "$LOG_FILE") 2>&1

log() { printf '[%s] %s\n' "$(date '+%F %T')" "$*"; }
die() { log "ERROR: $*"; exit 1; }
for cmd in pcs cibadmin python3; do command -v "$cmd" >/dev/null 2>&1 || die "Required command not found: $cmd"; done
[[ $EUID -eq 0 ]] || die "Run this script as root."

log "============================================================"
log "Pacemaker NVR Picata + configuration-updater constraint rebuild"
log "============================================================"
log "This script is intended to run AFTER Picata deployment."

CIB_XML="$(mktemp /tmp/nvr-cib.XXXXXX.xml)"
DISCOVERY_FILE="$(mktemp /tmp/nvr-discovery.XXXXXX)"
CONSTRAINT_XML="$(mktemp /tmp/nvr-constraints.XXXXXX.xml)"
trap 'rm -f "$CIB_XML" "$DISCOVERY_FILE" "$CONSTRAINT_XML"' EXIT

cibadmin --query > "$CIB_XML" || die "Could not retrieve the live CIB."
[[ -s "$CIB_XML" ]] || die "The retrieved CIB is empty."

python3 - "$CIB_XML" "$DISCOVERY_FILE" <<'PYTHON'
from __future__ import print_function
import re, sys
import xml.etree.ElementTree as ET

cib_path, output_path = sys.argv[1], sys.argv[2]
root=ET.parse(cib_path).getroot()
resources_root=root.find("./configuration/resources")
if resources_root is None:
    sys.stderr.write("CIB has no configuration/resources section.\n"); sys.exit(1)

primitives={}
def walk(parent, parent_group=None):
    for child in list(parent):
        tag=child.tag.split("}")[-1]
        if tag in ("group","clone","master"):
            walk(child, child.get("id") if tag=="group" else parent_group)
        elif tag=="primitive":
            rid=child.get("id")
            if rid: primitives[rid]=child
walk(resources_root)

def agent(p): return p.get("class",""),p.get("provider",""),p.get("type","")

clusters=set()
for rid,p in primitives.items():
    if rid.endswith("-vip"):
        cls,prov,typ=agent(p)
        if cls=="ocf" and prov=="heartbeat" and typ=="IPaddr2":
            c=rid[:-4]
            if re.match(r"^clnvrm[0-9]+$",c): clusters.add(c)
clusters=sorted(clusters)
if not clusters:
    sys.stderr.write("No NVR VIP resources found matching the supplied naming pattern.\n"); sys.exit(1)

output=[]
for c in clusters:
    vip=c+"-vip"; updater=c+"-pctcfg-updater"; etc=c+"-nfsetc01"
    if vip not in primitives: sys.stderr.write("Missing VIP resource: %s\n"%vip); sys.exit(1)
    if updater not in primitives:
        sys.stderr.write("%s: missing updater resource %s. Picata/services are not deployed yet.\n"%(c,updater)); sys.exit(1)
    cls,prov,typ=agent(primitives[updater])
    if cls!="systemd" or typ!="configuration-updater":
        sys.stderr.write("%s: updater has unexpected resource agent.\n"%c); sys.exit(1)
    if etc not in primitives:
        sys.stderr.write("%s: missing required /etc resource %s.\n"%(c,etc)); sys.exit(1)

    nfs=[]
    npat=re.compile(r"^"+re.escape(c)+r"-nfsrec([0-9]+)$")
    for rid,p in primitives.items():
        m=npat.match(rid)
        if m:
            cls,prov,typ=agent(p)
            if cls=="ocf" and prov=="heartbeat" and typ=="Filesystem": nfs.append((int(m.group(1)),rid))
    nfs.sort()
    if [n for n,r in nfs] != [1,2,3,4]:
        sys.stderr.write("%s: expected NFSREC01-04. Found %s.\n"%(c,[n for n,r in nfs])); sys.exit(1)

    pp=re.compile(r"^"+re.escape(c)+r"-picata([0-9]+)$")
    picata=[]
    for rid,p in primitives.items():
        m=pp.match(rid)
        if m:
            cls,prov,typ=agent(p)
            if cls=="systemd" and typ.startswith("picata-"): picata.append((int(m.group(1)),rid))
    picata.sort()
    if not picata:
        sys.stderr.write("%s: no Picata systemd resources discovered.\n"%c); sys.exit(1)

    nfs_ids=[r for n,r in nfs]
    nfs_set=set(nfs_ids)
    for number,pid in picata:
        expected="%s-nfsrec%02d"%(c,number)
        if expected not in nfs_set:
            sys.stderr.write("%s: Picata %s has no matching NFSREC %s.\n"%(c,pid,expected)); sys.exit(1)

    output.append("|".join([c,vip,",".join(nfs_ids),",".join(r for n,r in picata),updater,etc]))

with open(output_path,"w") as f: f.write("\n".join(output)+"\n")
print("Discovered and validated %d NVR clusters."%len(output))
for line in output:
    f=line.split("|")
    print("%s: VIP=%s NFSREC=%d Picata=%d updater=%s etc=%s"%(f[0],f[1],len(f[2].split(",")),len(f[3].split(",")),f[4],f[5]))
PYTHON

[[ -s "$DISCOVERY_FILE" ]] || die "Resource discovery returned no results."
log "This script will rebuild ONLY Picata + configuration-updater constraints."
log "VIP/NFS constraints will NOT be deleted or modified."
log "Discovered NVR clusters:"
cat "$DISCOVERY_FILE"

if [[ "$AUTO_CONFIRM" != "YES" ]]; then
    echo
    read -r -p "Type YES to back up the CIB and rebuild service constraints: " ANSWER
    [[ "$ANSWER" == "YES" ]] || die "Cancelled by operator."
fi

log "Creating CIB backup: $BACKUP_FILE"
pcs cluster cib "$BACKUP_FILE" || die "Failed to create CIB backup."
[[ -s "$BACKUP_FILE" ]] || die "CIB backup file is empty."
chmod 600 "$BACKUP_FILE"
log "CIB backup completed."

# Delete existing service constraints by relationship, not ID.
log "Deleting only Picata/updater constraints managed by this script..."
cibadmin --query --scope constraints > "$CONSTRAINT_XML" || die "Could not retrieve current constraints."

mapfile -t CONSTRAINT_IDS < <(python3 - "$CONSTRAINT_XML" "$DISCOVERY_FILE" <<'PYTHON'
from __future__ import print_function
import sys
import xml.etree.ElementTree as ET

constraints_path, discovery_path=sys.argv[1],sys.argv[2]
root=ET.parse(constraints_path).getroot()

vips=set(); picata=set(); nfs=set(); updaters=set(); etcs=set(); pairs=set()
for line in open(discovery_path):
    line=line.strip()
    if not line: continue
    c,v,nfs_csv,picata_csv,updater,etc=line.split("|")
    vips.add(v); nfs.update(nfs_csv.split(",")); picata.update(picata_csv.split(",")); updaters.add(updater); etcs.add(etc)
    for p in picata_csv.split(","): pairs.add((p,v))

def is_coloc(e,a,b):
    if e.tag.split("}")[-1] != "rsc_colocation": return False
    r=e.get("rsc"); w=e.get("with-rsc")
    return (r==a and w==b) or (r==b and w==a)

def is_order(e,a,b):
    return e.tag.split("}")[-1] == "rsc_order" and e.get("first")==a and e.get("then")==b

for e in list(root):
    cid=e.get("id")
    if not cid: continue
    remove=False
    for p,v in pairs:
        if is_coloc(e,p,v): remove=True
    for p in picata:
        # Find its matching NFS from the resource suffix.
        # Picata01 -> NFSREC01, etc.
        marker="-picata"
        if marker in p:
            prefix,suffix=p.rsplit(marker,1)
            n=prefix+"-nfsrec"+suffix.zfill(2)
            if is_order(e,n,p): remove=True
    for u in updaters:
        for v in vips:
            if is_coloc(e,u,v): remove=True
        for etc in etcs:
            if is_order(e,etc,u): remove=True
    if remove: print(cid)
PYTHON
)

for cid in "${CONSTRAINT_IDS[@]}"; do
    log "Deleting service constraint: $cid"
    pcs constraint delete "$cid" || die "Failed to delete constraint $cid"
done
log "Service constraints deleted: ${#CONSTRAINT_IDS[@]}"

while IFS='|' read -r cluster vip nfs_csv picata_csv updater etc_resource; do
    [[ -n "$cluster" ]] || continue
    log "------------------------------------------------------------"
    log "Building service constraints for $cluster"
    log "VIP: $vip"; log "NFSREC: $nfs_csv"; log "Picata: $picata_csv"; log "Updater: $updater"; log "/etc resource: $etc_resource"
    log "------------------------------------------------------------"

    IFS=',' read -r -a picata_array <<< "$picata_csv"
    for picata in "${picata_array[@]}"; do
        suffix="${picata##*picata}"
        nfs="$(printf '%s-nfsrec%02d' "$cluster" "$((10#$suffix))")"
        pcs constraint colocation add "$picata" with "$vip" INFINITY id="col-${cluster}-${picata}-vip" || die "Failed Picata/VIP colocation for $picata"
        pcs constraint order start "$nfs" then start "$picata" kind=Mandatory id="ord-${cluster}-${nfs}-${picata}" || die "Failed NFSREC/Picata ordering for $picata"
    done

    pcs constraint colocation add "$updater" with "$vip" INFINITY id="col-${cluster}-updater-vip" || die "Failed updater/VIP colocation for $cluster"
    pcs constraint order start "$etc_resource" then start "$updater" kind=Mandatory id="ord-${cluster}-etc-${updater}" || die "Failed /etc/picata/updater ordering for $cluster"
done < "$DISCOVERY_FILE"

log "Picata + configuration-updater constraint rebuild completed."
pcs constraint config || die "Unable to display rebuilt constraints."
log "============================================================"
log "NVR Picata + configuration-updater constraint rebuild completed successfully."
log "CIB backup: $BACKUP_FILE"
log "Log file: $LOG_FILE"
log "============================================================"
