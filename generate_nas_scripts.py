#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generate Dell PowerScale / OneFS NVR NAS scripts.

Purpose
-------
Read the NVR_Clusters sheet from the Excel workbook and generate one
idempotent OneFS shell script per cluster.

Supported architectures
------------------------
7+1:
    CLNVRM050
        clnvrm051
        clnvrm052
        ...
        clnvrm057
    Each RG has P01-P04.

1+1:
    CLNVRM100
        clnvrm101
    The RG has P01-P28.

Directory layout
----------------
Cluster root:
    /ifs/infstonas001mp/mtr-rec/clnvrm050

Resource group:
    /ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm051

RG directories:
    app/
    etc/
    data/
    log/

Picata service directories:
    clnvrm051_p01/
    clnvrm051_p02/
    ...

NFS
---
Only the cluster ROOT is exported.

Example:
    /ifs/infstonas001mp/mtr-rec/clnvrm050

The RG and Picata directories are NOT exported individually.

The generated scripts are intentionally idempotent:
    - Existing directories are NOT deleted.
    - Existing directories are NOT recreated destructively.
    - Existing directories are checked.
    - Ownership/mode are corrected only when necessary.
    - Missing directories are created with the required ownership/mode.
    - Existing NFS exports are checked and modified only when necessary.
    - Quotas are checked before creation.

IMPORTANT
---------
This script generates shell scripts. It does NOT directly modify OneFS.
Review the generated scripts before executing them.
"""

import sys
import shlex
from pathlib import Path

import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

EXCEL_FILE = Path(r"Templates\nvr.xlsx")
OUTPUT_DIR = Path("nas-output")

# CLNVRM050 - CLNVRM090 plus CLNVRM100.
TARGET_CLUSTER_NUMBERS = set(list(range(50, 91)) + [100])


# ============================================================
# OWNERSHIP / PERMISSIONS
# ============================================================

RECORDER_OWNER = "recorder:recorder"

# Cluster and RG roots are private to recorder.
CLUSTER_MODE = "700"
RG_MODE = "700"

APP_MODE = "755"
DATA_MODE = "700"
ETC_MODE = "755"

# Keep the existing log convention from the original generator.
LOG_OWNER = "root:wheel"
LOG_MODE = "755"

# Picata service directories must be writable by recorder.
SERVICE_OWNER = "recorder:recorder"
SERVICE_MODE = "700"


# ============================================================
# PICATA
# ============================================================

SEVEN_PLUS_ONE_SERVICES = 4
ONE_PLUS_ONE_SERVICES = 28


# ============================================================
# QUOTA
# ============================================================

ENABLE_QUOTA = True
SERVICE_QUOTA = "16TB"
QUOTA_MODE = "hard"


# ============================================================
# NFS EXPORT
# ============================================================

NFS_ZONE = "mtr-rec"
NFS_RW_CLIENTS = "10.101.30.0/23"
NFS_ROOT_CLIENTS = "10.101.30.0/23"


# ============================================================
# HELPERS
# ============================================================

def shell_quote(value):
    return shlex.quote(str(value))


def is_nan_value(value):
    if pd.isna(value):
        return True
    return str(value).strip().lower() == "nan"


def cluster_number(cluster_alias):
    """
    Accept:
        clnvrm050
        clnvrr050

    Return:
        50
    """
    value = str(cluster_alias).strip().upper()

    if value.startswith("CLNVRM"):
        suffix = value[6:]
    elif value.startswith("CLNVRR"):
        suffix = value[6:]
    else:
        return None

    if not suffix.isdigit():
        return None

    return int(suffix)


def is_target_cluster(cluster_alias):
    number = cluster_number(cluster_alias)

    if number is None:
        return False

    return number in TARGET_CLUSTER_NUMBERS


def normalize_cluster_alias(cluster_alias):
    """
    Normalize:
        clnvrr050 -> clnvrm050
        clnvrm050 -> clnvrm050
    """
    number = cluster_number(cluster_alias)

    if number is None:
        raise ValueError(
            "Invalid cluster_alias: {}".format(cluster_alias)
        )

    return "clnvrm{:03d}".format(number)


def resource_group_name(picata_rg):
    """
    Convert:
        tvsnvrpic051mp -> clnvrm051
        tvsnvrpic101mp -> clnvrm101
    """
    value = str(picata_rg).strip().lower()
    prefix = "tvsnvrpic"

    if not value.startswith(prefix):
        raise ValueError(
            "Unsupported picata_rg_instances value '{}'. "
            "Expected format like tvsnvrpic051mp.".format(picata_rg)
        )

    remainder = value[len(prefix):]

    if len(remainder) < 3 or not remainder[:3].isdigit():
        raise ValueError(
            "Cannot extract RG number from '{}'.".format(picata_rg)
        )

    return "clnvrm{}".format(remainder[:3])


def service_count(cluster_type):
    value = str(cluster_type).strip()

    if value == "7+1":
        return SEVEN_PLUS_ONE_SERVICES

    if value == "1+1":
        return ONE_PLUS_ONE_SERVICES

    return None


def add_header(lines, title):
    lines.extend([
        "#!/bin/bash",
        "#",
        "# {}".format(title),
        "#",
        "# Generated by generate_nas_scripts.py",
        "#",
        "set -e",
        "",
        "# This script is idempotent.",
        "# Existing directories are preserved.",
        "# Ownership/mode are corrected only when required.",
        "",
    ])


# ============================================================
# IDEMPOTENT DIRECTORY HELPERS
# ============================================================

def add_directory_check_fix(lines, path, owner, mode, description):
    """
    Generate an idempotent directory operation.

    If the directory exists:
        - do NOT recreate it
        - check owner
        - check group
        - check mode
        - correct only what is wrong

    If it does not exist:
        - create it
        - set ownership
        - set mode
    """

    qpath = shell_quote(path)

    lines.extend([
        "# {}".format(description),
        "if [[ -d {} ]]; then".format(qpath),
        "    echo \"Directory exists: {}\"".format(path),
        "",
        "    CURRENT_OWNER=$(stat -c '%U' {} 2>/dev/null || true)".format(qpath),
        "    CURRENT_GROUP=$(stat -c '%G' {} 2>/dev/null || true)".format(qpath),
        "    CURRENT_MODE=$(stat -c '%a' {} 2>/dev/null || true)".format(qpath),
        "",
        "    if [[ \"$CURRENT_OWNER:$CURRENT_GROUP\" != \"{}\" ]]; then".format(owner),
        "        echo \"  Fixing owner/group: $CURRENT_OWNER:$CURRENT_GROUP -> {}\"".format(owner),
        "        chown {} {}".format(owner, qpath),
        "    else",
        "        echo \"  Owner/group OK: $CURRENT_OWNER:$CURRENT_GROUP\"",
        "    fi",
        "",
        "    if [[ \"$CURRENT_MODE\" != \"{}\" ]]; then".format(mode),
        "        echo \"  Fixing mode: $CURRENT_MODE -> {}\"".format(mode),
        "        chmod {} {}".format(mode, qpath),
        "    else",
        "        echo \"  Mode OK: $CURRENT_MODE\"",
        "    fi",
        "else",
        "    echo \"Directory does not exist. Creating: {}\"".format(path),
        "    mkdir -p {}".format(qpath),
        "    chown {} {}".format(owner, qpath),
        "    chmod {} {}".format(mode, qpath),
        "fi",
        "",
    ])


# ============================================================
# RESOURCE GROUP BASE DIRECTORIES
# ============================================================

def add_rg_base_structure(lines, rg_root):
    """
    Create/check:
        app
        etc
        data
        log
    """

    app_dir = "{}/app".format(rg_root)
    etc_dir = "{}/etc".format(rg_root)
    data_dir = "{}/data".format(rg_root)
    log_dir = "{}/log".format(rg_root)

    lines.extend([
        "# --------------------------------------------------------",
        "# RESOURCE GROUP BASE DIRECTORIES",
        "# --------------------------------------------------------",
        "",
    ])

    add_directory_check_fix(
        lines,
        app_dir,
        RECORDER_OWNER,
        APP_MODE,
        "APP directory"
    )

    add_directory_check_fix(
        lines,
        etc_dir,
        RECORDER_OWNER,
        ETC_MODE,
        "ETC directory"
    )

    add_directory_check_fix(
        lines,
        data_dir,
        RECORDER_OWNER,
        DATA_MODE,
        "DATA directory"
    )

    add_directory_check_fix(
        lines,
        log_dir,
        LOG_OWNER,
        LOG_MODE,
        "LOG directory"
    )


# ============================================================
# PICATA SERVICE DIRECTORIES
# ============================================================

def add_service_directories(lines, rg_root, rg_name, count):
    """
    Create/check:
        P01-P04 for 7+1
        P01-P28 for 1+1

    Each service directory is:
        recorder:recorder
        mode 700
    """

    lines.extend([
        "# --------------------------------------------------------",
        "# PICATA SERVICE DIRECTORIES",
        "# --------------------------------------------------------",
        "",
    ])

    for number in range(1, count + 1):

        service_name = "{}_p{:02d}".format(
            rg_name,
            number
        )

        service_root = "{}/{}".format(
            rg_root,
            service_name
        )

        add_directory_check_fix(
            lines,
            service_root,
            SERVICE_OWNER,
            SERVICE_MODE,
            "PICATA service directory {}".format(service_name)
        )


# ============================================================
# PICATA ETC STRUCTURE
# ============================================================

def add_picata_structure(lines, rg_root):
    """
    Create/check:

        etc/picata/area-LQ/alarms
        etc/picata/area-LQ/records

    The existing content is preserved.
    """

    picata_root = "{}/etc/picata".format(rg_root)
    area_lq = "{}/area-LQ".format(picata_root)
    alarms = "{}/alarms".format(area_lq)
    records = "{}/records".format(area_lq)

    lines.extend([
        "# --------------------------------------------------------",
        "# PICATA ETC STRUCTURE",
        "# --------------------------------------------------------",
        "",
    ])

    add_directory_check_fix(
        lines,
        picata_root,
        RECORDER_OWNER,
        ETC_MODE,
        "PICATA configuration root"
    )

    add_directory_check_fix(
        lines,
        area_lq,
        RECORDER_OWNER,
        ETC_MODE,
        "PICATA area-LQ directory"
    )

    add_directory_check_fix(
        lines,
        alarms,
        RECORDER_OWNER,
        ETC_MODE,
        "PICATA alarms directory"
    )

    add_directory_check_fix(
        lines,
        records,
        RECORDER_OWNER,
        ETC_MODE,
        "PICATA records directory"
    )


# ============================================================
# QUOTA
# ============================================================

def add_quota(lines, rg_root, rg_name):
    """
    Create a directory quota only if one does not already exist.
    """

    if not ENABLE_QUOTA:
        return

    qpath = shell_quote(rg_root)

    lines.extend([
        "# --------------------------------------------------------",
        "# QUOTA: {}".format(rg_name),
        "# --------------------------------------------------------",
        "",
        "QUOTA_PATH={}".format(qpath),
        "",
        "echo \"Checking quota for $QUOTA_PATH\"",
        "",
        "if isi quota quotas list --path \"$QUOTA_PATH\" >/dev/null 2>&1; then",
        "    echo \"Quota already exists: $QUOTA_PATH\"",
        "else",
        "    echo \"Creating quota: $QUOTA_PATH\"",
        "    isi quota quotas create \"$QUOTA_PATH\" --type=directory",
        "fi",
        "",
    ])

    if QUOTA_MODE == "hard":
        lines.extend([
            "isi quota quotas modify \"$QUOTA_PATH\" "
            "--hard-threshold {}".format(SERVICE_QUOTA),
            "",
        ])

    elif QUOTA_MODE == "advisory":
        lines.extend([
            "isi quota quotas modify \"$QUOTA_PATH\" "
            "--advisory-threshold {}".format(SERVICE_QUOTA),
            "",
        ])

    else:
        raise ValueError(
            "QUOTA_MODE must be 'hard' or 'advisory'."
        )


# ============================================================
# NFS EXPORT
# ============================================================

def add_nfs_export(lines, cluster_root):
    """
    Export ONLY the cluster root.

    If the export exists:
        modify its required parameters.

    If it does not exist:
        create it.

    IMPORTANT:
        The AWK braces are escaped because this Python function
        uses str.format().
    """

    qroot = shell_quote(cluster_root)
    qzone = shell_quote(NFS_ZONE)
    qrw = shell_quote(NFS_RW_CLIENTS)
    qrootclients = shell_quote(NFS_ROOT_CLIENTS)

    lines.extend([
        "# --------------------------------------------------------",
        "# NFS EXPORT - CLUSTER ROOT ONLY",
        "# --------------------------------------------------------",
        "",
        "EXPORT_PATH={}".format(qroot),
        "",
        "echo \"Checking NFS export: $EXPORT_PATH\"",
        "",
        "# Find an existing export for this exact path.",
        "EXPORT_ID=$(isi nfs exports list "
        "--zone={} --format=csv | "
        "awk -F, -v p=\"$EXPORT_PATH\" "
        "'$2 == p {{print $1; exit}}')".format(qzone),
        "",
        "if [[ -z \"$EXPORT_ID\" ]]; then",
        "    echo \"NFS export does not exist. Creating: $EXPORT_PATH\"",
        "",
        "    isi nfs exports create \"$EXPORT_PATH\" \\",
        "        --zone={} \\".format(qzone),
        "        --read-write-clients={} \\".format(qrw),
        "        --root-clients={} \\".format(qrootclients),
        "        --all-dirs=yes",
        "",
        "    echo \"NFS export created: $EXPORT_PATH\"",
        "else",
        "    echo \"NFS export already exists: $EXPORT_PATH (ID $EXPORT_ID)\"",
        "    echo \"Checking/updating required NFS parameters...\"",
        "",
        "    isi nfs exports modify \"$EXPORT_ID\" \\",
        "        --zone={} \\".format(qzone),
        "        --read-write-clients={} \\".format(qrw),
        "        --root-clients={} \\".format(qrootclients),
        "        --all-dirs=yes",
        "",
        "    echo \"NFS export updated: $EXPORT_PATH (ID $EXPORT_ID)\"",
        "fi",
        "",
    ])


# ============================================================
# MAIN
# ============================================================

def main():

    print("")
    print("============================================================")
    print(" ONEFS NVR NAS SCRIPT GENERATOR - IDEMPOTENT")
    print("============================================================")
    print("")
    print("Excel:")
    print("  {}".format(EXCEL_FILE))
    print("")
    print("Target clusters:")
    print("  CLNVRM050 - CLNVRM090")
    print("  CLNVRM100")
    print("")
    print("Existing directories will NOT be deleted.")
    print("Existing directories will be checked and corrected only")
    print("when owner/group/mode do not match the required values.")
    print("")

    # --------------------------------------------------------
    # Validate Excel
    # --------------------------------------------------------

    if not EXCEL_FILE.exists():
        print("ERROR: Excel file does not exist:")
        print("  {}".format(EXCEL_FILE))
        print("")
        print("Current working directory:")
        print("  {}".format(Path.cwd()))
        return 1

    # --------------------------------------------------------
    # Check openpyxl
    # --------------------------------------------------------

    try:
        import openpyxl  # noqa: F401
    except ImportError:
        print("ERROR: openpyxl is not installed.")
        print("")
        print('Install with: python -m pip install "openpyxl==3.0.10"')
        return 1

    # --------------------------------------------------------
    # Create output directory
    # --------------------------------------------------------

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------------
    # Read Excel
    # --------------------------------------------------------

    try:
        data = pd.read_excel(
            str(EXCEL_FILE),
            sheet_name="NVR_Clusters",
            engine="openpyxl"
        )
    except Exception as exc:
        print("ERROR: Failed to read Excel file:")
        print("  {}".format(exc))
        return 1

    # --------------------------------------------------------
    # Required columns
    # --------------------------------------------------------

    required_columns = {
        "cluster_type",
        "cluster_name",
        "cluster_alias",
        "picata_rg_instances",
        "nas_root",
    }

    missing_columns = required_columns - set(data.columns)

    if missing_columns:
        print("ERROR: Missing required Excel columns:")

        for column in sorted(missing_columns):
            print("  {}".format(column))

        print("")
        print("Available columns:")

        for column in data.columns:
            print("  {}".format(column))

        return 1

    # --------------------------------------------------------
    # Output tracking
    # --------------------------------------------------------

    processed_rg = set()

    cluster_folder_scripts = {}
    cluster_quota_scripts = {}

    cluster_root_paths = {}
    cluster_types = {}
    cluster_rg_counts = {}

    # ========================================================
    # PROCESS EXCEL
    # ========================================================

    for index, row in data.iterrows():

        if is_nan_value(row["cluster_alias"]):
            continue

        if is_nan_value(row["cluster_type"]):
            continue

        if is_nan_value(row["picata_rg_instances"]):
            continue

        if is_nan_value(row["nas_root"]):
            continue

        raw_cluster_alias = str(
            row["cluster_alias"]
        ).strip()

        cluster_alias = normalize_cluster_alias(
            raw_cluster_alias
        )

        # Only requested target clusters.
        if not is_target_cluster(raw_cluster_alias):
            continue

        cluster_type = str(
            row["cluster_type"]
        ).strip()

        cluster_name = str(
            row["cluster_name"]
        ).strip().upper()

        picata_rg = str(
            row["picata_rg_instances"]
        ).strip()

        nas_root = str(
            row["nas_root"]
        ).strip().rstrip("/")

        # ----------------------------------------------------
        # Validate architecture
        # ----------------------------------------------------

        count = service_count(cluster_type)

        if count is None:
            print(
                "WARNING: Unsupported cluster_type '{}' "
                "for {}. Skipping row {}.".format(
                    cluster_type,
                    cluster_alias,
                    index + 2
                )
            )
            continue

        # ----------------------------------------------------
        # Convert Excel Picata RG to filesystem RG
        # ----------------------------------------------------

        try:
            rg_name = resource_group_name(picata_rg)
        except ValueError as exc:
            print(
                "WARNING: {} Skipping row {}.".format(
                    exc,
                    index + 2
                )
            )
            continue

        # ----------------------------------------------------
        # Cluster root comes directly from Excel nas_root.
        # ----------------------------------------------------

        cluster_root = nas_root

        # ----------------------------------------------------
        # Prevent duplicate RG processing.
        # ----------------------------------------------------

        rg_key = (
            cluster_alias,
            rg_name
        )

        if rg_key in processed_rg:
            continue

        processed_rg.add(rg_key)

        # ----------------------------------------------------
        # Validate cluster architecture consistency
        # ----------------------------------------------------

        if cluster_alias in cluster_types:

            if cluster_types[cluster_alias] != cluster_type:

                print(
                    "ERROR: Cluster {} has conflicting "
                    "cluster_type values: '{}' and '{}'.".format(
                        cluster_alias,
                        cluster_types[cluster_alias],
                        cluster_type
                    )
                )

                return 1

        else:
            cluster_types[cluster_alias] = cluster_type

        # ----------------------------------------------------
        # Initialize cluster files
        # ----------------------------------------------------

        if cluster_alias not in cluster_folder_scripts:

            cluster_folder_scripts[cluster_alias] = []
            cluster_quota_scripts[cluster_alias] = []

            cluster_root_paths[cluster_alias] = cluster_root

            cluster_rg_counts[cluster_alias] = 0

            add_header(
                cluster_folder_scripts[cluster_alias],
                "NAS FOLDERS / PERMISSIONS / NFS - {}".format(
                    cluster_alias
                )
            )

            add_header(
                cluster_quota_scripts[cluster_alias],
                "NAS QUOTAS - {}".format(
                    cluster_alias
                )
            )

        folder_lines = cluster_folder_scripts[cluster_alias]
        quota_lines = cluster_quota_scripts[cluster_alias]

        cluster_rg_counts[cluster_alias] += 1

        # ====================================================
        # CLUSTER ROOT
        # ====================================================

        if cluster_rg_counts[cluster_alias] == 1:

            folder_lines.extend([
                "",
                "################################################",
                "# CLUSTER ROOT",
                "################################################",
                "",
            ])

            add_directory_check_fix(
                folder_lines,
                cluster_root,
                RECORDER_OWNER,
                CLUSTER_MODE,
                "CLUSTER ROOT"
            )

        # ====================================================
        # RESOURCE GROUP
        # ====================================================

        rg_root = "{}/{}".format(
            cluster_root,
            rg_name
        )

        folder_lines.extend([
            "",
            "################################################",
            "# CLUSTER: {}".format(cluster_alias),
            "# CLUSTER NAME: {}".format(cluster_name),
            "# TYPE: {}".format(cluster_type),
            "# PICATA RG: {}".format(picata_rg),
            "# RESOURCE GROUP: {}".format(rg_name),
            "################################################",
            "",
        ])

        add_directory_check_fix(
            folder_lines,
            rg_root,
            RECORDER_OWNER,
            RG_MODE,
            "RESOURCE GROUP ROOT"
        )

        # ----------------------------------------------------
        # RG app/etc/data/log
        # ----------------------------------------------------

        add_rg_base_structure(
            folder_lines,
            rg_root
        )

        # ----------------------------------------------------
        # RG etc/picata/...
        # ----------------------------------------------------

        add_picata_structure(
            folder_lines,
            rg_root
        )

        # ----------------------------------------------------
        # P01-P04 or P01-P28
        # ----------------------------------------------------

        add_service_directories(
            folder_lines,
            rg_root,
            rg_name,
            count
        )

        # ----------------------------------------------------
        # Quota on RG root
        # ----------------------------------------------------

        add_quota(
            quota_lines,
            rg_root,
            rg_name
        )

    # ========================================================
    # VALIDATE 7+1 / 1+1 RG COUNTS
    # ========================================================

    for cluster_alias in sorted(
        cluster_folder_scripts.keys(),
        key=lambda name: cluster_number(name)
    ):

        cluster_type = cluster_types[cluster_alias]
        actual_count = cluster_rg_counts[cluster_alias]

        if cluster_type == "7+1":

            if actual_count != 7:

                print(
                    "ERROR: {} is 7+1 but {} resource groups "
                    "were found. Expected 7.".format(
                        cluster_alias,
                        actual_count
                    )
                )

                return 1

        elif cluster_type == "1+1":

            if actual_count != 1:

                print(
                    "ERROR: {} is 1+1 but {} resource groups "
                    "were found. Expected 1.".format(
                        cluster_alias,
                        actual_count
                    )
                )

                return 1

    # ========================================================
    # ONE NFS EXPORT PER CLUSTER
    # ========================================================

    for cluster_alias in sorted(
        cluster_folder_scripts.keys(),
        key=lambda name: cluster_number(name)
    ):

        cluster_root = cluster_root_paths[cluster_alias]

        folder_lines = cluster_folder_scripts[cluster_alias]

        folder_lines.extend([
            "",
            "################################################",
            "# CLUSTER ROOT NFS EXPORT",
            "################################################",
            "",
        ])

        add_nfs_export(
            folder_lines,
            cluster_root
        )

    # ========================================================
    # WRITE OUTPUT FILES
    # ========================================================

    print("")
    print("Generating files...")
    print("")

    sorted_clusters = sorted(
        cluster_folder_scripts.keys(),
        key=lambda name: cluster_number(name)
    )

    for cluster_alias in sorted_clusters:

        folder_file = (
            OUTPUT_DIR /
            "{}_folders.sh".format(cluster_alias)
        )

        quota_file = (
            OUTPUT_DIR /
            "{}_quotas.sh".format(cluster_alias)
        )

        cluster_folder_scripts[cluster_alias].extend([
            "",
            'echo ""',
            'echo "Completed NAS folders, permissions and NFS export for {}"'.format(
                cluster_alias
            ),
            "",
        ])

        cluster_quota_scripts[cluster_alias].extend([
            "",
            'echo ""',
            'echo "Completed quotas for {}"'.format(
                cluster_alias
            ),
            "",
        ])

        with open(
            str(folder_file),
            "w",
            encoding="utf-8",
            newline="\n"
        ) as file_handle:

            file_handle.write(
                "\n".join(
                    cluster_folder_scripts[cluster_alias]
                )
            )

        with open(
            str(quota_file),
            "w",
            encoding="utf-8",
            newline="\n"
        ) as file_handle:

            file_handle.write(
                "\n".join(
                    cluster_quota_scripts[cluster_alias]
                )
            )

        # Make generated scripts executable on Linux.
        try:
            folder_file.chmod(0o750)
            quota_file.chmod(0o750)
        except OSError:
            pass

        cluster_type = cluster_types[cluster_alias]

        print(
            "{}: type={} RGs={} P01-P{:02d}".format(
                cluster_alias,
                cluster_type,
                cluster_rg_counts[cluster_alias],
                service_count(cluster_type)
            )
        )

        print("  {}".format(folder_file))
        print("  {}".format(quota_file))
        print("")

    # ========================================================
    # SUMMARY
    # ========================================================

    print("============================================================")
    print(" COMPLETED")
    print("============================================================")
    print("")
    print(
        "Generated {} cluster(s).".format(
            len(sorted_clusters)
        )
    )
    print("")

    for cluster_alias in sorted_clusters:

        cluster_type = cluster_types[cluster_alias]
        rg_count = cluster_rg_counts[cluster_alias]
        p_count = service_count(cluster_type)

        print(
            "{} | {} | {} RG(s) | P01-P{:02d}".format(
                cluster_alias,
                cluster_type,
                rg_count,
                p_count
            )
        )

    print("")
    print("NFS:")
    print("  One cluster-root export per cluster")
    print("  all-dirs=yes")
    print("  RW/root clients: {}".format(NFS_RW_CLIENTS))
    print("")
    print("Existing directories are preserved and checked.")
    print("Only incorrect ownership/mode values are changed.")
    print("")

    return 0


if __name__ == "__main__":
    sys.exit(main())
