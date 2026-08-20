import os
import pandas as pd
import re

# ==========================================
# 1. User Defined Variables & Dictionaries
# ==========================================
dc_resource_list = "Resource List-v7.6.xlsx"
SHEET_NAME = "General Resource List"
token_timeout = 10000
ha_pass = "Th@les01"
resource_count = 13        
ilo_username = "hpilofence"
ilo_password = "Th@les01"

# Systemd Variables
sv_picata_config_update = "systemd:configuration-updater"

# Scope-based Configuration Dictionary
scope_config = {
    'mtr': {
        'nas_basedir': "ssip.mtr-rec.infstonas001mp.mak.iss:/ifs/infstonas001mp/mtr-rec/",
        'vip_nic': "vlan126",
        'vip_mask': 23,
        'cluster_prefix': "clnvrm"
    },
    'rtr': {
        'nas_basedir': "ssip.rtr-rec.infstonas001rp.mak.iss:/ifs/infstonas001rp/rtr-rec/",
        'vip_nic': "vlan226", 
        'vip_mask': 23,
        'cluster_prefix': "clnvrr"
    }
}

# ==========================================
# 2. Path Setup
# ==========================================
base_dir = os.getcwd()
template_dir = os.path.join(base_dir, "Templates")
excel_path = os.path.join(template_dir, dc_resource_list)
output_dir = os.path.join(base_dir, "cluster_scripts")

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# ==========================================
# 3. Read and Filter Data
# ==========================================
df = pd.read_excel(excel_path, sheet_name=SHEET_NAME, engine='openpyxl')
df.columns = df.columns.astype(str).str.strip().str.lower()

# DIAGNOSTIC CHECK
required_columns = [
    'scope', 'hostname', 'logical_name', 'ilo_ip', 'cl_ip_address', 
    'me_ip_address', 'component_short_name', 'component', 'alias', 'fe_ip_address'
]
missing_cols = [col for col in required_columns if col not in df.columns]

if missing_cols:
    print(f"\n[ERROR] Missing required columns in sheet '{SHEET_NAME}': {missing_cols}")
    exit()

# Filter Blade Servers
df_blades = df[
    (df['equipment_type'].astype(str).str.strip().str.lower() == "nvr blade server") & 
    (df['enclosure_physical_name'].notna()) & 
    (~df['enclosure_physical_name'].astype(str).str.strip().str.lower().isin(['n.a', 'n/a', 'nan', ''])) &
    (df['scope'].notna())
].copy()

# Filter VIPs
df_vips = df[
    (df['component_short_name'].astype(str).str.strip().str.lower() == "vip") & 
    (df['component'].astype(str).str.strip().str.lower() == "network video recorder") &
    (df['alias'].notna())
].copy()

if df_blades.empty:
    print("\n[WARNING] 0 Blade Servers matched your filters! No files will be generated.")
    exit()

# ==========================================
# 4. Determine Cluster Names Dynamically
# ==========================================
def determine_cluster_name(row):
    logical_name_val = row['logical_name']
    scope_val = str(row['scope']).strip().lower()
    
    # Retrieve cluster_prefix from dictionary, default to unknown if not found
    cluster_prefix = scope_config.get(scope_val, {}).get('cluster_prefix', 'clnvr_unknown')
    
    match = re.search(r'\d+', str(logical_name_val))
    if match:
        node_num = int(match.group())
        cluster_index = ((node_num - 1) // 8) * 10
        return f"{cluster_prefix}{cluster_index:03d}"
    return f"{cluster_prefix}_unknown"

df_blades['cluster_name'] = df_blades.apply(determine_cluster_name, axis=1)

# ==========================================
# 5. Generate Cluster Scripts (Line by Line)
# ==========================================
grouped = df_blades.groupby(['enclosure_physical_name', 'cluster_name'])

for (enclosure_name, cluster_name), group in grouped:
    group = group.sort_values('logical_name')
    
    # Extract the scope for this specific group to pull from dictionary
    current_scope = str(group['scope'].iloc[0]).strip().lower()
    
    if current_scope not in scope_config:
        print(f"[WARNING] Scope '{current_scope}' not found in dictionary! Skipping cluster {cluster_name}.")
        continue
        
    nas_basedir = scope_config[current_scope]['nas_basedir']
    vip_nic = scope_config[current_scope]['vip_nic']
    vip_mask = scope_config[current_scope]['vip_mask']
    cluster_prefix = scope_config[current_scope]['cluster_prefix']
    
    safe_enclosure_name = str(enclosure_name).replace("/", "-").replace("\\", "-")
    cluster_dir = os.path.join(output_dir, f"{cluster_name}_{safe_enclosure_name}")
    os.makedirs(cluster_dir, exist_ok=True)
    
    auth_node_names, setup_lines, stonith_lines, utilization_lines = [], [], [], []
    
    # 5a. Build Core Infrastructure Commands (Blade Servers)
    for _, row in group.iterrows():
        logical_hostname = str(row['logical_name']).strip()
        actual_hostname = str(row['hostname']).strip()
        cl_ip = str(row['cl_ip_address']).strip()
        me_ip = str(row['me_ip_address']).strip()
        ilo_ip = str(row['ilo_ip']).strip()
        
        # IP Warnings for Blades
        if pd.isna(row['ilo_ip']) or ilo_ip in ['', 'nan']:
            print(f"[WARNING] Blade {actual_hostname} is missing its ilo_ip!")
        if pd.isna(row['cl_ip_address']) or cl_ip in ['', 'nan']:
            print(f"[WARNING] Blade {actual_hostname} is missing its cl_ip_address!")
            
        auth_node_names.append(logical_hostname)
        setup_lines.append(f"{actual_hostname} addr={cl_ip} addr={me_ip} \\")
        stonith_lines.append(f"pcs stonith create fence_{actual_hostname} fence_ilo4 ip={ilo_ip} username={ilo_username} password=\"{ilo_password}\" pcmk_host_list={actual_hostname} op monitor interval=600s")
        utilization_lines.append(f"pcs node utilization {actual_hostname} rcount={resource_count}")
        
    auth_nodes_str = " ".join(auth_node_names)
    setup_block = "\n".join(setup_lines)
    stonith_block = "\n".join(stonith_lines)
    utilization_block = "\n".join(utilization_lines)
    
    # 5b. Build VIP, Filesystem, and Application Blocks via Python Iteration
    vip_fs_blocks = []
    app_blocks = []
    
    match = re.search(r'\d+', cluster_name)
    if match:
        c_idx = int(match.group())
        expected_aliases = [f"{cluster_prefix}{c_idx + i:03d}" for i in range(1, 8)]
        
        c_name_lower = cluster_name.lower()
        
        # Get VIPs for this specific cluster
        cluster_vip_rows = df_vips[df_vips['alias'].astype(str).str.strip().str.lower().isin(expected_aliases)]
        found_aliases = cluster_vip_rows['alias'].astype(str).str.strip().str.lower().tolist()
        
        missing_vips = [alias for alias in expected_aliases if alias not in found_aliases]
        if missing_vips:
            print(f"[WARNING] Cluster {cluster_name}: Missing VIPs in Excel! Could not find: {', '.join(missing_vips)}")
        
        for alias in expected_aliases:
            v_row_df = cluster_vip_rows[cluster_vip_rows['alias'].astype(str).str.strip().str.lower() == alias]
            
            if v_row_df.empty:
                continue
                
            v_row = v_row_df.iloc[0]
            fe_ip = str(v_row['fe_ip_address']).strip()
            
            if pd.isna(v_row['fe_ip_address']) or fe_ip in ['', 'nan']:
                print(f"[WARNING] VIP {alias} is missing its fe_ip_address in the Excel file!")
            
            # -----------------------------------------------------
            # BEFORE.TXT (VIPs, Mounts, Storage Colocation & Order)
            # -----------------------------------------------------
            vip_fs_blocks.append(f"""
# ---------------------------------------------------------
# Storage & VIP for {alias}
# ---------------------------------------------------------
pcs resource create {alias}-vip ocf:heartbeat:IPaddr2 ip={fe_ip} cidr_netmask={vip_mask} nic={vip_nic} op monitor interval=60s
pcs resource utilization {alias}-vip rcount=1

# Core Resource Group
pcs resource create {alias}-nfsapp01 ocf:heartbeat:Filesystem device='{nas_basedir}{c_name_lower}/{alias}/app' directory='/app' fstype='nfs' options="rw,nfsvers=3,tcp,hard,rsize=1048576,wsize=1048576,noatime,nodiratime,nconnect=8,nolock" --group rg-{alias}-core op monitor interval=60s
pcs resource create {alias}-nfslog01 ocf:heartbeat:Filesystem device='{nas_basedir}{c_name_lower}/{alias}/log' directory='/var/log/thales' fstype='nfs' options="rw,nfsvers=3,tcp,hard,rsize=1048576,wsize=1048576,noatime,nodiratime,nconnect=8,nolock" --group rg-{alias}-core op monitor interval=60s
pcs resource create {alias}-nfsdat01 ocf:heartbeat:Filesystem device='{nas_basedir}{c_name_lower}/{alias}/data' directory='/data' fstype='nfs' options="rw,nfsvers=3,tcp,hard,rsize=1048576,wsize=1048576,noatime,nodiratime,nconnect=8,nolock" --group rg-{alias}-core op monitor interval=60s
pcs resource utilization rg-{alias}-core rcount=3
pcs constraint colocation add rg-{alias}-core with {alias}-vip score=INFINITY

# CCTV Recording Mounts
pcs resource create {alias}-nfsrec01 ocf:heartbeat:Filesystem device='{nas_basedir}{c_name_lower}/{alias}/{alias}_p01' directory='/mnt/storage/{alias}_p01' fstype='nfs' options="rw,nfsvers=3,tcp,hard,rsize=1048576,wsize=1048576,noatime,nodiratime,nconnect=8,actimeo=3600,nocto,nolock" op monitor interval=60s
pcs resource utilization {alias}-nfsrec01 rcount=1
pcs constraint colocation add {alias}-nfsrec01 with {alias}-vip score=INFINITY

pcs resource create {alias}-nfsrec02 ocf:heartbeat:Filesystem device='{nas_basedir}{c_name_lower}/{alias}/{alias}_p02' directory='/mnt/storage/{alias}_p02' fstype='nfs' options="rw,nfsvers=3,tcp,hard,rsize=1048576,wsize=1048576,noatime,nodiratime,nconnect=8,actimeo=3600,nocto,nolock" op monitor interval=60s
pcs resource utilization {alias}-nfsrec02 rcount=1
pcs constraint colocation add {alias}-nfsrec02 with {alias}-vip score=INFINITY

pcs resource create {alias}-nfsrec03 ocf:heartbeat:Filesystem device='{nas_basedir}{c_name_lower}/{alias}/{alias}_p03' directory='/mnt/storage/{alias}_p03' fstype='nfs' options="rw,nfsvers=3,tcp,hard,rsize=1048576,wsize=1048576,noatime,nodiratime,nconnect=8,actimeo=3600,nocto,nolock" op monitor interval=60s
pcs resource utilization {alias}-nfsrec03 rcount=1
pcs constraint colocation add {alias}-nfsrec03 with {alias}-vip score=INFINITY

pcs resource create {alias}-nfsrec04 ocf:heartbeat:Filesystem device='{nas_basedir}{c_name_lower}/{alias}/{alias}_p04' directory='/mnt/storage/{alias}_p04' fstype='nfs' options="rw,nfsvers=3,tcp,hard,rsize=1048576,wsize=1048576,noatime,nodiratime,nconnect=8,actimeo=3600,nocto,nolock" op monitor interval=60s
pcs resource utilization {alias}-nfsrec04 rcount=1
pcs constraint colocation add {alias}-nfsrec04 with {alias}-vip score=INFINITY

# Order constraints for Storage
pcs constraint order start rg-{alias}-core then set {alias}-nfsrec01 {alias}-nfsrec02 {alias}-nfsrec03 {alias}-nfsrec04 sequential=false
""")

            # -----------------------------------------------------
            # AFTER.TXT (Services, Colocation & Order)
            # -----------------------------------------------------
            app_blocks.append(f"""
# ---------------------------------------------------------
# Application Services for {alias}
# ---------------------------------------------------------
pcs resource create {alias}-pctcfg-updater {sv_picata_config_update} op monitor interval=120s timeout=60s
pcs resource utilization {alias}-pctcfg-updater rcount=1
pcs constraint colocation add {alias}-pctcfg-updater with {alias}-vip score=INFINITY

pcs resource create {alias}-picata01 systemd:picata-{alias}_p01 op monitor interval=120s timeout=60s
pcs resource utilization {alias}-picata01 rcount=1
pcs constraint colocation add {alias}-picata01 with {alias}-vip score=INFINITY

pcs resource create {alias}-picata02 systemd:picata-{alias}_p02 op monitor interval=120s timeout=60s
pcs resource utilization {alias}-picata02 rcount=1
pcs constraint colocation add {alias}-picata02 with {alias}-vip score=INFINITY

pcs resource create {alias}-picata03 systemd:picata-{alias}_p03 op monitor interval=120s timeout=60s
pcs resource utilization {alias}-picata03 rcount=1
pcs constraint colocation add {alias}-picata03 with {alias}-vip score=INFINITY

pcs resource create {alias}-picata04 systemd:picata-{alias}_p04 op monitor interval=120s timeout=60s
pcs resource utilization {alias}-picata04 rcount=1
pcs constraint colocation add {alias}-picata04 with {alias}-vip score=INFINITY

# Order constraints for Applications
pcs constraint order start rg-{alias}-core then set {alias}-pctcfg-updater {alias}-picata01 {alias}-picata02 {alias}-picata03 {alias}-picata04 sequential=false
pcs constraint order {alias}-nfsrec01 then {alias}-picata01
pcs constraint order {alias}-nfsrec02 then {alias}-picata02
pcs constraint order {alias}-nfsrec03 then {alias}-picata03
pcs constraint order {alias}-nfsrec04 then {alias}-picata04
""")

    # Combine blocks
    vip_fs_content = "".join(vip_fs_blocks)
    app_content = "".join(app_blocks)

    # 5c. Assemble BEFORE.txt
    before_content = f"""systemctl enable pcsd.service --now

pcs host auth {auth_nodes_str} -u hacluster -p "{ha_pass}"

pcs cluster setup {cluster_name.upper()} --start \\
{setup_block}
transport knet \\
link linknumber=0 link_priority=1 link linknumber=1 link_priority=0 \\
totem token={token_timeout}

pcs cluster start --all
pcs cluster enable --all

pcs property set symmetric-cluster=true
pcs property set placement-strategy=balanced
pcs resource defaults update resource-stickiness=INFINITY migration-threshold=3 failure-timeout=1800s

# Fencing Configuration
{stonith_block}

# Node Utilization Limits
{utilization_block}
{vip_fs_content}
"""

    # 5d. Assemble AFTER.txt
    final_app_content = f"""{app_content}
# ---------------------------------------------------------
# Final Verification
# ---------------------------------------------------------
pcs resource cleanup
pcs resource refresh
"""

    # 5e. Write Files
    before_filepath = os.path.join(cluster_dir, f"{cluster_name}_before({safe_enclosure_name}).txt")
    after_filepath = os.path.join(cluster_dir, f"{cluster_name}_after({safe_enclosure_name}).txt")
    
    # Write BEFORE
    before_exists = os.path.exists(before_filepath)
    with open(before_filepath, "w") as f:
        f.write(before_content)
    if before_exists:
        print(f"Overwritten: {cluster_name}_before({safe_enclosure_name}).txt")
    else:
        print(f"Generated: {cluster_name}_before({safe_enclosure_name}).txt")
        
    # Write AFTER
    after_exists = os.path.exists(after_filepath)
    with open(after_filepath, "w") as f:
        f.write(final_app_content)
    if after_exists:
        print(f"Overwritten: {cluster_name}_after({safe_enclosure_name}).txt")
    else:
        print(f"Generated: {cluster_name}_after({safe_enclosure_name}).txt")

print("\nScript generation complete. Files are located in the 'cluster_scripts' subdirectories.")