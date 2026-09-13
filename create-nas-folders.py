#!/usr/bin/env python3

import sys
from pathlib import Path

import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

SCRIPT_DIR = Path(__file__).resolve().parent

EXCEL_FILE = SCRIPT_DIR / "templates" / "nvr.xlsx"

# Change this if your worksheet has a different name
SHEET_NAME = "NVR_Clusters"

OUTPUT_FILE = SCRIPT_DIR / "nas-output" / "create_nas_folders.sh"

OWNER = "recorder:recorder"


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clean(value):
    """
    Convert Excel values into clean strings.
    Empty cells become empty strings.
    """

    if pd.isna(value):
        return ""

    return str(value).strip()


def get_storage_folder(dc):
    """
    Determine the storage folder from DC.

    MP -> mtr-rec
    RP -> rtr-rec
    """

    dc = clean(dc).lower()

    if dc == "mp":
        return "mtr-rec"

    elif dc == "rp":
        return "rtr-rec"

    else:
        raise ValueError(
            "Unsupported DC value '{}'. Expected MP or RP.".format(dc)
        )


def normalize_cluster_type(cluster_type):
    """
    Normalize cluster type.
    """

    value = clean(cluster_type).lower()
    value = value.replace(" ", "")

    if value in ["7+1", "7plus1", "7-1"]:
        return "7+1"

    elif value in ["1+1", "1plus1", "1-1"]:
        return "1+1"

    else:
        raise ValueError(
            "Unsupported cluster type '{}'".format(cluster_type)
        )


def generate_resource_group_name(cluster_alias, number):
    """
    Generate the Resource Group name.

    IMPORTANT NAMING RULE:

    clnvrm000 + 1 -> clnvrm001
    clnvrm000 + 2 -> clnvrm002
    ...
    clnvrm000 + 7 -> clnvrm007

    We replace the LAST digit of cluster_alias.
    We do NOT append the number.
    """

    cluster_alias = clean(cluster_alias)

    if not cluster_alias:
        raise ValueError("cluster_alias is empty")

    # Remove the final digit
    base_name = cluster_alias[:-1]

    # Add the RG number
    resource_group = "{}{}".format(
        base_name,
        number
    )

    return resource_group


def get_resource_groups(cluster_alias, cluster_type):
    """
    Generate Resource Groups automatically.

    7+1:
        clnvrm001
        clnvrm002
        ...
        clnvrm007

    1+1:
        clnvrm001
    """

    resource_groups = []

    if cluster_type == "7+1":

        for number in range(1, 8):

            resource_group = generate_resource_group_name(
                cluster_alias,
                number
            )

            resource_groups.append(resource_group)

    elif cluster_type == "1+1":

        resource_group = generate_resource_group_name(
            cluster_alias,
            1
        )

        resource_groups.append(resource_group)

    else:

        raise ValueError(
            "Unsupported cluster type '{}'".format(cluster_type)
        )

    return resource_groups


def get_service_count(cluster_type):
    """
    7+1 = 4 Picata services per Resource Group
    1+1 = 28 Picata services
    """

    if cluster_type == "7+1":
        return 4

    elif cluster_type == "1+1":
        return 28

    else:
        raise ValueError(
            "Unsupported cluster type '{}'".format(cluster_type)
        )


# ============================================================
# START
# ============================================================

print("")
print("============================================================")
print("READING NVR RESOURCE LIST")
print("============================================================")
print("")


# ============================================================
# READ EXCEL FILE
# ============================================================

try:

    df = pd.read_excel(
        EXCEL_FILE,
        sheet_name=SHEET_NAME,
        dtype=object,
        engine="openpyxl"
    )

except FileNotFoundError:

    print("")
    print("ERROR: Excel file was not found:")
    print(EXCEL_FILE)
    sys.exit(1)


except Exception as e:

    print("")
    print("ERROR reading Excel file:")
    print(e)
    sys.exit(1)


# ============================================================
# CLEAN COLUMN NAMES
# ============================================================

df.columns = [

    str(column).strip()

    for column in df.columns

]


# ============================================================
# REQUIRED COLUMNS
# ============================================================

required_columns = [

    "dc",
    "cluster_alias",
    "cluster_type",
    "nas_cluster"

]


missing_columns = []


for column in required_columns:

    if column not in df.columns:

        missing_columns.append(column)


if missing_columns:

    print("")
    print("ERROR: Missing required columns:")

    for column in missing_columns:

        print("  - {}".format(column))

    print("")
    print("Available columns:")

    for column in df.columns:

        print("  - {}".format(column))

    sys.exit(1)


# ============================================================
# CREATE OUTPUT DIRECTORY
# ============================================================

output_path = Path(OUTPUT_FILE)

output_path.parent.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# INITIALIZE OUTPUT SCRIPT
# ============================================================

lines = []


lines.append("#!/bin/bash")
lines.append("")
lines.append("set -e")
lines.append("")
lines.append("############################################################")
lines.append("# NVR NAS FOLDER CREATION SCRIPT")
lines.append("# Generated automatically from nvr.xlsx")
lines.append("############################################################")
lines.append("")


# ============================================================
# TRACK PROCESSED CLUSTERS
# ============================================================

processed_clusters = set()

clusters_generated = 0
resource_groups_generated = 0
service_folders_generated = 0


# ============================================================
# PROCESS EXCEL ROWS
# ============================================================

for index, row in df.iterrows():

    excel_row = index + 2


    # --------------------------------------------------------
    # READ VALUES
    # --------------------------------------------------------

    dc = clean(row["dc"])

    cluster_alias = clean(
        row["cluster_alias"]
    )

    cluster_type_value = clean(
        row["cluster_type"]
    )

    nas_cluster = clean(
        row["nas_cluster"]
    )


    # --------------------------------------------------------
    # SKIP EMPTY ROWS
    # --------------------------------------------------------

    if not cluster_alias:

        continue


    # --------------------------------------------------------
    # PROCESS EACH CLUSTER ONLY ONCE
    #
    # A 7+1 cluster has multiple server rows.
    # --------------------------------------------------------

    cluster_key = cluster_alias.lower()


    if cluster_key in processed_clusters:

        continue


    # --------------------------------------------------------
    # VALIDATE DATA
    # --------------------------------------------------------

    if not dc:

        print(
            "WARNING: Row {} skipped. DC is empty for '{}'.".format(
                excel_row,
                cluster_alias
            )
        )

        continue


    if not cluster_type_value:

        print(
            "WARNING: Row {} skipped. cluster_type is empty for '{}'.".format(
                excel_row,
                cluster_alias
            )
        )

        continue


    if not nas_cluster:

        print(
            "WARNING: Row {} skipped. nas_cluster is empty for '{}'.".format(
                excel_row,
                cluster_alias
            )
        )

        continue


    # --------------------------------------------------------
    # NORMALIZE CLUSTER TYPE
    # --------------------------------------------------------

    try:

        cluster_type = normalize_cluster_type(
            cluster_type_value
        )

    except ValueError as e:

        print(
            "WARNING: Row {} skipped: {}".format(
                excel_row,
                e
            )
        )

        continue


    # --------------------------------------------------------
    # DETERMINE STORAGE FOLDER
    # --------------------------------------------------------

    try:

        storage_folder = get_storage_folder(dc)

    except ValueError as e:

        print(
            "WARNING: Row {} skipped: {}".format(
                excel_row,
                e
            )
        )

        continue


    # --------------------------------------------------------
    # DETERMINE RESOURCE GROUPS
    # --------------------------------------------------------

    try:

        resource_groups = get_resource_groups(
            cluster_alias,
            cluster_type
        )

        service_count = get_service_count(
            cluster_type
        )

    except ValueError as e:

        print(
            "WARNING: Row {} skipped: {}".format(
                excel_row,
                e
            )
        )

        continue


    # --------------------------------------------------------
    # MARK AS PROCESSED
    # --------------------------------------------------------

    processed_clusters.add(cluster_key)

    clusters_generated += 1


    # ========================================================
    # CLUSTER ROOT
    #
    # Example:
    #
    # /ifs/infstonas001mp/mtr-rec/clnvrm000
    # ========================================================

    cluster_root = "/ifs/{}/{}/{}".format(
        nas_cluster,
        storage_folder,
        cluster_alias
    )


    # ========================================================
    # CLUSTER HEADER
    # ========================================================

    lines.append("")
    lines.append("############################################################")
    lines.append("# CLUSTER      : {}".format(cluster_alias))
    lines.append("# CLUSTER TYPE : {}".format(cluster_type))
    lines.append("# NAS ROOT     : {}".format(cluster_root))
    lines.append("############################################################")
    lines.append("")


    # ========================================================
    # CREATE CLUSTER ROOT
    # ========================================================

    lines.append(
        "mkdir -p '{}'".format(cluster_root)
    )

    lines.append(
        "chown {} '{}'".format(
            OWNER,
            cluster_root
        )
    )

    lines.append("")


    # ========================================================
    # PROCESS RESOURCE GROUPS
    # ========================================================

    for resource_group in resource_groups:


        resource_groups_generated += 1


        # ----------------------------------------------------
        # RESOURCE GROUP ROOT
        #
        # Example:
        #
        # /ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm001
        # ----------------------------------------------------

        rg_root = "{}/{}".format(
            cluster_root,
            resource_group
        )


        lines.append("")
        lines.append("############################################################")
        lines.append("# RESOURCE GROUP : {}".format(resource_group))
        lines.append("# PATH           : {}".format(rg_root))
        lines.append("############################################################")
        lines.append("")


        # ====================================================
        # CREATE RESOURCE GROUP ROOT
        # ====================================================

        lines.append(
            "mkdir -p '{}'".format(rg_root)
        )

        lines.append(
            "chown {} '{}'".format(
                OWNER,
                rg_root
            )
        )

        lines.append("")


        # ====================================================
        # CREATE CORE FOLDERS
        # ====================================================

        lines.append("# Core mount point folders")
        lines.append("")


        core_folders = [

            "{}/app".format(rg_root),

            "{}/data".format(rg_root),

            "{}/log".format(rg_root),

            "{}/etc/picata".format(rg_root)

        ]


        for folder in core_folders:

            lines.append(
                "mkdir -p '{}'".format(folder)
            )

            lines.append(
                "chown -R {} '{}'".format(
                    OWNER,
                    folder
                )
            )

            lines.append("")


        # ====================================================
        # CREATE PICATA SERVICE FOLDERS
        #
        # Example:
        #
        # clnvrm001_p01
        # clnvrm001_p02
        # clnvrm001_p03
        # clnvrm001_p04
        # ====================================================

        lines.append("# Picata service folders")
        lines.append("")


        for service_number in range(
            1,
            service_count + 1
        ):


            service_name = "{}_p{:02d}".format(
                resource_group,
                service_number
            )


            service_path = "{}/{}".format(
                rg_root,
                service_name
            )


            lines.append(
                "mkdir -p '{}'".format(
                    service_path
                )
            )


            lines.append(
                "chown -R {} '{}'".format(
                    OWNER,
                    service_path
                )
            )


            lines.append("")


            service_folders_generated += 1


# ============================================================
# SCRIPT COMPLETE
# ============================================================

lines.append("")
lines.append("############################################################")
lines.append("# NAS FOLDER CREATION COMPLETE")
lines.append("############################################################")
lines.append("")


# ============================================================
# WRITE OUTPUT FILE
# ============================================================

try:

    with open(
        str(output_path),
        "w",
        encoding="utf-8",
        newline="\n"
    ) as output_file:

        output_file.write(
            "\n".join(lines)
        )

        output_file.write("\n")


except Exception as e:

    print("")
    print("ERROR writing output file:")
    print(e)

    sys.exit(1)


# ============================================================
# SUMMARY
# ============================================================

print("")
print("============================================================")
print("NAS SCRIPT GENERATED SUCCESSFULLY")
print("============================================================")
print("")

print("Input Excel:")
print(EXCEL_FILE)

print("")

print("Output:")
print(OUTPUT_FILE)

print("")

print("Clusters generated: {}".format(
    clusters_generated
))

print("Resource groups generated: {}".format(
    resource_groups_generated
))

print("Service folders generated: {}".format(
    service_folders_generated
))

print("")
print("Naming example:")
print("")
print("Cluster Alias: clnvrm000")
print("Resource Groups:")
print("  clnvrm001")
print("  clnvrm002")
print("  ...")
print("  clnvrm007")
print("")
print("Service example:")
print("  clnvrm001_p01")
print("  clnvrm001_p02")
print("  clnvrm001_p03")
print("  clnvrm001_p04")
print("")
print("============================================================")