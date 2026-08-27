# BUILD_MARKER: CLUSTER_CONFIG_CENTRAL_V2_MERGED_SCOPE_20260828

import os
import re
import sys

import pandas as pd

from functions import vars


# ============================================================================
# HELPERS
# ============================================================================

def normalize_text(value):
    """Return a lower-case normalized string for general comparisons."""
    if pd.isna(value):
        return ""

    return str(value).strip().lower()


def normalize_scope(value):
    """
    Return the canonical uppercase scope key.

    ILO_SCOPE_SETTINGS uses uppercase keys, so values such as 'sil', 'SIL',
    'Sil', ' mtr ' and 'rTr' all resolve to the same configuration.
    """
    if pd.isna(value):
        return ""

    return str(value).strip().upper()


def is_missing(value):
    """Use the project's global invalid-value rules."""
    if pd.isna(value):
        return True

    return (
        str(value).strip().upper()
        in vars.INVALID_VALUES
    )


def determine_cluster_name(row):
    """
    Determine the cluster name from logical_name and the scope prefix.

    Eight NVR nodes belong to one cluster. Cluster numbering advances by ten
    so the associated VIP aliases can occupy the following seven numbers.
    """
    logical_name_value = row[
        "logical_name"
    ]

    scope_value = normalize_scope(
        row[
            "scope"
        ]
    )

    cluster_prefix = (
        vars.ILO_SCOPE_SETTINGS
        .get(
            scope_value,
            {},
        )
        .get(
            "CLUSTER_PREFIX",
            "clnvr_unknown",
        )
    )

    match = re.search(
        r"\d+",
        str(
            logical_name_value
        ),
    )

    if not match:
        return "{}_unknown".format(
            cluster_prefix
        )

    node_number = int(
        match.group()
    )

    cluster_index = (
        (
            node_number
            - 1
        )
        // vars.CLUSTER_NODE_GROUP_SIZE
    ) * vars.CLUSTER_INDEX_STEP

    return "{}{:03d}".format(
        cluster_prefix,
        cluster_index,
    )


def get_scope_config(scope_name):
    """
    Return the merged centralized scope configuration.

    Scope matching is case-insensitive because the Excel value is normalized
    to the uppercase keys used by ILO_SCOPE_SETTINGS.
    """
    scope_key = normalize_scope(
        scope_name
    )

    if not scope_key:
        return None

    return (
        vars.ILO_SCOPE_SETTINGS
        .get(
            scope_key
        )
    )


def load_complete_resource_list():
    """
    Load the complete resource-list worksheet.

    This generator intentionally does not use START_ROW, END_ROW or
    EXCEL_EMPTY_ROW_STOP because cluster nodes and VIP rows may be located
    anywhere in the worksheet.
    """
    print(
        "Loading complete Excel worksheet: {} "
        "(Sheet: '{}')..."
        .format(
            vars.RESOURCE_LIST,
            vars.SHEET_NAME,
        )
    )

    dataframe = pd.read_excel(
        vars.RESOURCE_LIST,
        sheet_name=vars.SHEET_NAME,
        engine=vars.EXCEL_ENGINE,
    )

    dataframe.columns = (
        dataframe.columns
        .astype(
            str
        )
        .str.strip()
        .str.lower()
    )

    return dataframe


def validate_required_columns(dataframe):
    """Return any required columns missing from the workbook."""
    return [
        column
        for column
        in vars.CLUSTER_REQUIRED_COLUMNS
        if column not in dataframe.columns
    ]


def filter_blades(dataframe):
    """Return all NVR blade-server rows used for cluster generation."""
    equipment = (
        dataframe[
            "equipment_type"
        ]
        .astype(
            str
        )
        .str.strip()
        .str.lower()
    )

    enclosure = (
        dataframe[
            "enclosure_physical_name"
        ]
        .astype(
            str
        )
        .str.strip()
        .str.lower()
    )

    invalid_enclosure_values = {
        "",
        "n.a",
        "n/a",
        "nan",
        "none",
        "nodatafound",
    }

    return dataframe[
        (
            equipment
            == vars.CLUSTER_BLADE_EQUIPMENT_TYPE
        )
        & dataframe[
            "enclosure_physical_name"
        ].notna()
        & (
            ~enclosure.isin(
                invalid_enclosure_values
            )
        )
        & dataframe[
            "scope"
        ].notna()
    ].copy()


def filter_vips(dataframe):
    """Return all NVR VIP rows from the complete worksheet."""
    short_name = (
        dataframe[
            "component_short_name"
        ]
        .astype(
            str
        )
        .str.strip()
        .str.lower()
    )

    component = (
        dataframe[
            "component"
        ]
        .astype(
            str
        )
        .str.strip()
        .str.lower()
    )

    return dataframe[
        (
            short_name
            == vars.CLUSTER_VIP_COMPONENT_SHORT_NAME
        )
        & (
            component
            == vars.CLUSTER_VIP_COMPONENT_NAME
        )
        & dataframe[
            "alias"
        ].notna()
    ].copy()


def safe_enclosure_name(value):
    """Create a filesystem-safe enclosure name."""
    return (
        str(
            value
        )
        .replace(
            "/",
            "-",
        )
        .replace(
            "\\",
            "-",
        )
    )


def build_cluster_contents(
    cluster_name,
    group,
    vip_dataframe,
    scope_config,
):
    """Build the BEFORE and AFTER command-file contents for one cluster."""
    nas_basedir = scope_config[
        "NAS_BASEDIR"
    ]

    vip_nic = scope_config[
        "VIP_NIC"
    ]

    vip_mask = scope_config[
        "VIP_MASK"
    ]

    cluster_prefix = scope_config[
        "CLUSTER_PREFIX"
    ]

    auth_node_names = []
    setup_lines = []
    stonith_lines = []
    utilization_lines = []

    for _, row in group.iterrows():
        logical_hostname = str(
            row[
                "logical_name"
            ]
        ).strip()

        actual_hostname = str(
            row[
                "hostname"
            ]
        ).strip()

        cl_ip = str(
            row[
                "cl_ip_address"
            ]
        ).strip()

        me_ip = str(
            row[
                "me_ip_address"
            ]
        ).strip()

        ilo_ip = str(
            row[
                "ilo_ip"
            ]
        ).strip()

        if is_missing(
            row[
                "ilo_ip"
            ]
        ):
            print(
                "[WARNING] Blade {} is missing its ilo_ip!"
                .format(
                    actual_hostname
                )
            )

        if is_missing(
            row[
                "cl_ip_address"
            ]
        ):
            print(
                "[WARNING] Blade {} is missing its "
                "cl_ip_address!"
                .format(
                    actual_hostname
                )
            )

        auth_node_names.append(
            logical_hostname
        )

        setup_lines.append(
            "{} addr={} addr={} \\".format(
                actual_hostname,
                cl_ip,
                me_ip,
            )
        )

        stonith_lines.append(
            "pcs stonith create fence_{host} fence_ilo4 "
            "ip={ilo} username={user} password=\"{password}\" "
            "pcmk_host_list={host} op monitor interval=600s"
            .format(
                host=actual_hostname,
                ilo=ilo_ip,
                user=(
                    vars.CLUSTER_FENCE_USERNAME
                ),
                password=(
                    vars.CLUSTER_FENCE_PASSWORD
                ),
            )
        )

        utilization_lines.append(
            "pcs node utilization {} rcount={}"
            .format(
                actual_hostname,
                vars.CLUSTER_RESOURCE_COUNT,
            )
        )

    auth_nodes_string = " ".join(
        auth_node_names
    )

    setup_block = "\n".join(
        setup_lines
    )

    stonith_block = "\n".join(
        stonith_lines
    )

    utilization_block = "\n".join(
        utilization_lines
    )

    vip_fs_blocks = []
    app_blocks = []

    match = re.search(
        r"\d+",
        cluster_name,
    )

    if match:
        cluster_index = int(
            match.group()
        )

        expected_aliases = [
            "{}{:03d}".format(
                cluster_prefix,
                cluster_index + offset,
            )
            for offset
            in range(
                1,
                vars.CLUSTER_VIP_COUNT_PER_CLUSTER
                + 1,
            )
        ]

        cluster_name_lower = (
            cluster_name.lower()
        )

        vip_alias_series = (
            vip_dataframe[
                "alias"
            ]
            .astype(
                str
            )
            .str.strip()
            .str.lower()
        )

        cluster_vip_rows = (
            vip_dataframe[
                vip_alias_series.isin(
                    expected_aliases
                )
            ]
        )

        found_aliases = (
            cluster_vip_rows[
                "alias"
            ]
            .astype(
                str
            )
            .str.strip()
            .str.lower()
            .tolist()
        )

        missing_vips = [
            alias
            for alias
            in expected_aliases
            if alias not in found_aliases
        ]

        if missing_vips:
            print(
                "[WARNING] Cluster {}: Missing VIPs in Excel! "
                "Could not find: {}"
                .format(
                    cluster_name,
                    ", ".join(
                        missing_vips
                    ),
                )
            )

        for alias in expected_aliases:
            alias_matches = (
                cluster_vip_rows[
                    cluster_vip_rows[
                        "alias"
                    ]
                    .astype(
                        str
                    )
                    .str.strip()
                    .str.lower()
                    == alias
                ]
            )

            if alias_matches.empty:
                continue

            vip_row = (
                alias_matches.iloc[
                    0
                ]
            )

            fe_ip = str(
                vip_row[
                    "fe_ip_address"
                ]
            ).strip()

            if is_missing(
                vip_row[
                    "fe_ip_address"
                ]
            ):
                print(
                    "[WARNING] VIP {} is missing its "
                    "fe_ip_address in the Excel file!"
                    .format(
                        alias
                    )
                )

            vip_fs_blocks.append(
                """
# ---------------------------------------------------------
# Storage & VIP for {alias}
# ---------------------------------------------------------
pcs resource create {alias}-vip ocf:heartbeat:IPaddr2 ip={fe_ip} cidr_netmask={vip_mask} nic={vip_nic} op monitor interval=60s
pcs resource utilization {alias}-vip rcount=1

# Core Resource Group
pcs resource create {alias}-nfsapp01 ocf:heartbeat:Filesystem device='{nas_basedir}{cluster}/{alias}/app' directory='/app' fstype='nfs' options="rw,nfsvers=3,tcp,hard,rsize=1048576,wsize=1048576,noatime,nodiratime,nconnect=8,nolock" --group rg-{alias}-core op monitor interval=60s
pcs resource create {alias}-nfslog01 ocf:heartbeat:Filesystem device='{nas_basedir}{cluster}/{alias}/log' directory='/var/log/thales' fstype='nfs' options="rw,nfsvers=3,tcp,hard,rsize=1048576,wsize=1048576,noatime,nodiratime,nconnect=8,nolock" --group rg-{alias}-core op monitor interval=60s
pcs resource create {alias}-nfsdat01 ocf:heartbeat:Filesystem device='{nas_basedir}{cluster}/{alias}/data' directory='/data' fstype='nfs' options="rw,nfsvers=3,tcp,hard,rsize=1048576,wsize=1048576,noatime,nodiratime,nconnect=8,nolock" --group rg-{alias}-core op monitor interval=60s
pcs resource utilization rg-{alias}-core rcount=3
pcs constraint colocation add rg-{alias}-core with {alias}-vip score=INFINITY

# CCTV Recording Mounts
pcs resource create {alias}-nfsrec01 ocf:heartbeat:Filesystem device='{nas_basedir}{cluster}/{alias}/{alias}_p01' directory='/mnt/storage/{alias}_p01' fstype='nfs' options="rw,nfsvers=3,tcp,hard,rsize=1048576,wsize=1048576,noatime,nodiratime,nconnect=8,actimeo=3600,nocto,nolock" op monitor interval=60s
pcs resource utilization {alias}-nfsrec01 rcount=1
pcs constraint colocation add {alias}-nfsrec01 with {alias}-vip score=INFINITY

pcs resource create {alias}-nfsrec02 ocf:heartbeat:Filesystem device='{nas_basedir}{cluster}/{alias}/{alias}_p02' directory='/mnt/storage/{alias}_p02' fstype='nfs' options="rw,nfsvers=3,tcp,hard,rsize=1048576,wsize=1048576,noatime,nodiratime,nconnect=8,actimeo=3600,nocto,nolock" op monitor interval=60s
pcs resource utilization {alias}-nfsrec02 rcount=1
pcs constraint colocation add {alias}-nfsrec02 with {alias}-vip score=INFINITY

pcs resource create {alias}-nfsrec03 ocf:heartbeat:Filesystem device='{nas_basedir}{cluster}/{alias}/{alias}_p03' directory='/mnt/storage/{alias}_p03' fstype='nfs' options="rw,nfsvers=3,tcp,hard,rsize=1048576,wsize=1048576,noatime,nodiratime,nconnect=8,actimeo=3600,nocto,nolock" op monitor interval=60s
pcs resource utilization {alias}-nfsrec03 rcount=1
pcs constraint colocation add {alias}-nfsrec03 with {alias}-vip score=INFINITY

pcs resource create {alias}-nfsrec04 ocf:heartbeat:Filesystem device='{nas_basedir}{cluster}/{alias}/{alias}_p04' directory='/mnt/storage/{alias}_p04' fstype='nfs' options="rw,nfsvers=3,tcp,hard,rsize=1048576,wsize=1048576,noatime,nodiratime,nconnect=8,actimeo=3600,nocto,nolock" op monitor interval=60s
pcs resource utilization {alias}-nfsrec04 rcount=1
pcs constraint colocation add {alias}-nfsrec04 with {alias}-vip score=INFINITY

# Order constraints for Storage
pcs constraint order start rg-{alias}-core then set {alias}-nfsrec01 {alias}-nfsrec02 {alias}-nfsrec03 {alias}-nfsrec04 sequential=false
""".format(
                    alias=alias,
                    fe_ip=fe_ip,
                    vip_mask=vip_mask,
                    vip_nic=vip_nic,
                    nas_basedir=nas_basedir,
                    cluster=cluster_name_lower,
                )
            )

            app_blocks.append(
                """
# ---------------------------------------------------------
# Application Services for {alias}
# ---------------------------------------------------------
pcs resource create {alias}-pctcfg-updater {config_agent} op monitor interval=120s timeout=60s
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
""".format(
                    alias=alias,
                    config_agent=(
                        vars.CLUSTER_PICATA_CONFIG_UPDATE_AGENT
                    ),
                )
            )

    vip_fs_content = "".join(
        vip_fs_blocks
    )

    app_content = "".join(
        app_blocks
    )

    before_content = """systemctl enable pcsd.service --now

pcs host auth {nodes} -u {ha_user} -p "{ha_password}"

pcs cluster setup {cluster} --start \\
{setup}
transport knet \\
link linknumber=0 link_priority=1 link linknumber=1 link_priority=0 \\
totem token={token_timeout}

pcs cluster start --all
pcs cluster enable --all

pcs property set symmetric-cluster=true
pcs property set placement-strategy=balanced
pcs resource defaults update resource-stickiness=INFINITY migration-threshold=3 failure-timeout=1800s

# Fencing Configuration
{stonith}

# Node Utilization Limits
{utilization}
{vip_fs}
""".format(
        nodes=auth_nodes_string,
        ha_user=vars.CLUSTER_HA_USERNAME,
        ha_password=vars.CLUSTER_HA_PASSWORD,
        cluster=cluster_name.upper(),
        setup=setup_block,
        token_timeout=vars.CLUSTER_TOKEN_TIMEOUT,
        stonith=stonith_block,
        utilization=utilization_block,
        vip_fs=vip_fs_content,
    )

    after_content = """{applications}
# ---------------------------------------------------------
# Final Verification
# ---------------------------------------------------------
pcs resource cleanup
pcs resource refresh
""".format(
        applications=app_content
    )

    return (
        before_content,
        after_content,
    )


def write_cluster_files(
    enclosure_name,
    cluster_name,
    before_content,
    after_content,
):
    """Write/overwrite the generated command files for one cluster."""
    safe_name = safe_enclosure_name(
        enclosure_name
    )

    cluster_dir = os.path.join(
        vars.CLUSTER_OUTPUT_DIR,
        "{}_{}".format(
            cluster_name,
            safe_name,
        ),
    )

    if not os.path.isdir(
        cluster_dir
    ):
        os.makedirs(
            cluster_dir
        )

    before_filename = (
        "{}_before({}).txt"
        .format(
            cluster_name,
            safe_name,
        )
    )

    after_filename = (
        "{}_after({}).txt"
        .format(
            cluster_name,
            safe_name,
        )
    )

    before_path = os.path.join(
        cluster_dir,
        before_filename,
    )

    after_path = os.path.join(
        cluster_dir,
        after_filename,
    )

    before_exists = os.path.exists(
        before_path
    )

    with open(
        before_path,
        "w",
        encoding="utf-8",
    ) as handle:
        handle.write(
            before_content
        )

    if before_exists:
        print(
            "Overwritten: {}".format(
                before_filename
            )
        )
    else:
        print(
            "Generated: {}".format(
                before_filename
            )
        )

    after_exists = os.path.exists(
        after_path
    )

    with open(
        after_path,
        "w",
        encoding="utf-8",
    ) as handle:
        handle.write(
            after_content
        )

    if after_exists:
        print(
            "Overwritten: {}".format(
                after_filename
            )
        )
    else:
        print(
            "Generated: {}".format(
                after_filename
            )
        )


# ============================================================================
# MAIN
# ============================================================================

def main():
    if not os.path.isfile(
        vars.RESOURCE_LIST
    ):
        print(
            "[ERROR] Resource List not found: {}"
            .format(
                vars.RESOURCE_LIST
            )
        )

        return 1

    if not os.path.isdir(
        vars.CLUSTER_OUTPUT_DIR
    ):
        os.makedirs(
            vars.CLUSTER_OUTPUT_DIR
        )

    print(
        "=" * 100
    )
    print(
        "CLUSTER COMMAND GENERATOR"
    )
    print(
        "=" * 100
    )
    print(
        "Resource list       : {}"
        .format(
            vars.RESOURCE_LIST
        )
    )
    print(
        "Sheet               : {}"
        .format(
            vars.SHEET_NAME
        )
    )
    print(
        "Excel rows          : Complete worksheet"
    )
    print(
        "Output directory    : {}"
        .format(
            vars.CLUSTER_OUTPUT_DIR
        )
    )
    print(
        "=" * 100
    )

    try:
        dataframe = (
            load_complete_resource_list()
        )

    except Exception as exc:
        print(
            "[ERROR] Failed to read Excel workbook: {}"
            .format(
                exc
            )
        )

        return 1

    missing_columns = (
        validate_required_columns(
            dataframe
        )
    )

    if missing_columns:
        print(
            "\n[ERROR] Missing required columns in "
            "sheet '{}': {}"
            .format(
                vars.SHEET_NAME,
                missing_columns,
            )
        )

        return 1

    blade_dataframe = (
        filter_blades(
            dataframe
        )
    )

    vip_dataframe = (
        filter_vips(
            dataframe
        )
    )

    if blade_dataframe.empty:
        print(
            "\n[WARNING] 0 Blade Servers matched "
            "the cluster filters! No files will be generated."
        )

        print(
            "\n--- DIAGNOSTIC CHECK ---"
        )

        print(
            "Total rows loaded: {}".format(
                len(
                    dataframe
                )
            )
        )

        print(
            "Unique Equipment Types found:"
        )

        print(
            dataframe[
                "equipment_type"
            ]
            .dropna()
            .unique()
        )

        return 0

    blade_dataframe[
        "cluster_name"
    ] = blade_dataframe.apply(
        determine_cluster_name,
        axis=1,
    )

    grouped = (
        blade_dataframe.groupby(
            [
                "enclosure_physical_name",
                "cluster_name",
            ]
        )
    )

    generated_clusters = 0
    skipped_clusters = 0

    for (
        enclosure_name,
        cluster_name,
    ), group in grouped:
        group = group.sort_values(
            "logical_name"
        )

        current_scope = normalize_scope(
            group[
                "scope"
            ].iloc[
                0
            ]
        )

        scope_config = (
            get_scope_config(
                current_scope
            )
        )

        if not scope_config:
            print(
                "[WARNING] Scope '{}' not found in "
                "ILO_SCOPE_SETTINGS! Skipping cluster {}."
                .format(
                    current_scope,
                    cluster_name,
                )
            )

            skipped_clusters += 1

            continue

        required_scope_keys = [
            "NAS_BASEDIR",
            "VIP_NIC",
            "VIP_MASK",
            "CLUSTER_PREFIX",
        ]

        missing_scope_keys = [
            key
            for key
            in required_scope_keys
            if key not in scope_config
        ]

        if missing_scope_keys:
            print(
                "[WARNING] Scope '{}' is missing cluster "
                "settings {}. Skipping cluster {}."
                .format(
                    current_scope,
                    missing_scope_keys,
                    cluster_name,
                )
            )

            skipped_clusters += 1

            continue

        (
            before_content,
            after_content,
        ) = build_cluster_contents(
            cluster_name,
            group,
            vip_dataframe,
            scope_config,
        )

        write_cluster_files(
            enclosure_name,
            cluster_name,
            before_content,
            after_content,
        )

        generated_clusters += 1

    print(
        "\nScript generation complete. "
        "Generated cluster directories: {} | Skipped: {}"
        .format(
            generated_clusters,
            skipped_clusters,
        )
    )

    print(
        "Files are located under: {}"
        .format(
            vars.CLUSTER_OUTPUT_DIR
        )
    )

    return 0


if __name__ == "__main__":
    sys.exit(
        main()
    )
