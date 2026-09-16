#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pacemaker 1+1 Landscape Resource Report

Designed for:
  - 2-node Pacemaker cluster
  - 1 resource group
  - 1 active node
  - 1 passive/standby/failover node
  - typically 62 resources:
      5 core group members
      28 NFSREC resources
      28 Picata services
      1 configuration updater

Python compatibility:
  - Python 3.6+
  - Pillow required

The report uses actual crm_mon/CIB data. It does NOT duplicate
resources on the passive node.
"""

import os
import sys
import subprocess
import tempfile
import shutil
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("ERROR: Pillow is not installed.")
    print('Install with: python -m pip install "Pillow==8.4.0"')
    sys.exit(1)


# ============================================================
# CONFIGURATION
# ============================================================

CLUSTER_IP = "10.101.26.91"
SSH_USER = "root"
SSH_PORT = 22

SSH_PASSWORD = os.environ.get("PACEMAKER_SSH_PASSWORD")
if not SSH_PASSWORD:
    import getpass
    SSH_PASSWORD = getpass.getpass("SSH password: ")

OUTPUT_DIR = Path.cwd() / "cluster-diagrams"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Fixed landscape report.
WIDTH = 1600
HEIGHT = 1050

MARGIN = 22
GAP = 14

TITLE_H = 72
NODE_H = 620
SUMMARY_H = 245

NODE_W = (WIDTH - 2 * MARGIN - GAP) // 2

NODE_HEADER_H = 78
GROUP_HEADER_H = 40

RESOURCE_H = 20
RESOURCE_GAP = 2

CORE_H = 62
SERVICE_HEADER_H = 27
SERVICE_ROWS = 14
SERVICE_GRID_H = (
    SERVICE_HEADER_H
    + SERVICE_ROWS * (RESOURCE_H + RESOURCE_GAP)
    + 8
)
OTHER_H = 48


# ============================================================
# COLORS
# ============================================================

WHITE = "#FFFFFF"
BLACK = "#111111"
DARK = "#25344D"
BLUE = "#1769AA"
GREEN = "#16883A"
DARK_GREEN = "#0D6B2D"
PURPLE = "#7130A5"
ORANGE = "#D98200"
RED = "#C90000"

LIGHT_BLUE = "#EDF5FC"
LIGHT_GREEN = "#EAF7ED"
LIGHT_PURPLE = "#F2EAF9"
LIGHT_ORANGE = "#FFF3DE"
LIGHT_RED = "#FDEAEA"
LIGHT_GRAY = "#F4F6F8"
MID_GRAY = "#8A939E"
BORDER = "#B8C1CB"


# ============================================================
# FONTS
# ============================================================

def font(size, bold=False):
    if bold:
        candidates = [
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/segoeuib.ttf",
            "C:/Windows/Fonts/calibrib.ttf",
        ]
    else:
        candidates = [
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/segoeui.ttf",
            "C:/Windows/Fonts/calibri.ttf",
        ]

    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p, size)

    return ImageFont.load_default()


F_TITLE = font(30, True)
F_SUBTITLE = font(13)
F_NODE = font(20, True)
F_NODE_STATUS = font(13, True)
F_GROUP = font(13, True)
F_SECTION = font(11, True)
F_RESOURCE = font(10)
F_RESOURCE_SMALL = font(9)
F_RESOURCE_BOLD = font(9, True)
F_PANEL = font(14, True)
F_PANEL_LABEL = font(10)
F_PANEL_VALUE = font(10, True)
F_SMALL = font(9)
F_SMALL_BOLD = font(9, True)


# ============================================================
# DRAWING HELPERS
# ============================================================

def txt_size(draw, text, f):
    box = draw.textbbox((0, 0), text, font=f)
    return box[2] - box[0], box[3] - box[1]


def center(draw, box, text, f, fill):
    x1, y1, x2, y2 = box
    w, h = txt_size(draw, text, f)
    draw.text(
        (
            (x1 + x2 - w) / 2,
            (y1 + y2 - h) / 2,
        ),
        text,
        font=f,
        fill=fill,
    )


def truncate(draw, text, f, max_width):
    if txt_size(draw, text, f)[0] <= max_width:
        return text

    value = text
    while value and txt_size(
        draw,
        value + "...",
        f,
    )[0] > max_width:
        value = value[:-1]

    return value + "..."


def round_rect(draw, box, radius=7, fill=WHITE,
               outline=BORDER, width=1):
    draw.rounded_rectangle(
        box,
        radius=radius,
        fill=fill,
        outline=outline,
        width=width,
    )


def bool_value(value):
    return str(value).lower() in (
        "true",
        "yes",
        "on",
        "1",
    )


# ============================================================
# SSH
# ============================================================

def make_askpass(password):
    tmp = tempfile.mkdtemp(prefix="pcs_report_")
    askpass = os.path.join(tmp, "askpass.cmd")

    with open(askpass, "w") as f:
        f.write("@echo off\n")
        f.write("echo " + password + "\n")

    return tmp, askpass


def ssh(command):
    tmp = None

    try:
        tmp, askpass = make_askpass(SSH_PASSWORD)

        env = os.environ.copy()
        env["SSH_ASKPASS"] = askpass
        env["SSH_ASKPASS_REQUIRE"] = "force"
        env["DISPLAY"] = "none:0"

        cmd = [
            "ssh",
            "-p",
            str(SSH_PORT),
            "-T",
            "-o",
            "StrictHostKeyChecking=no",
            "-o",
            "UserKnownHostsFile=NUL",
            "-o",
            "ConnectTimeout=15",
            "-o",
            "ConnectionAttempts=1",
            "-o",
            "PreferredAuthentications=password,keyboard-interactive",
            "-o",
            "PubkeyAuthentication=no",
            SSH_USER + "@" + CLUSTER_IP,
            command,
        ]

        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            env=env,
        )

        if result.returncode != 0:
            print()
            print("=" * 80)
            print("SSH COMMAND FAILED")
            print("=" * 80)
            print("Target :", SSH_USER + "@" + CLUSTER_IP)
            print("Command:", command)
            print()
            print(result.stderr)
            sys.exit(1)

        return result.stdout

    finally:
        if tmp:
            shutil.rmtree(tmp, ignore_errors=True)


# ============================================================
# PACEMAKER DATA
# ============================================================

print()
print("=" * 80)
print("PACEMAKER 1+1 LANDSCAPE REPORT")
print("=" * 80)
print()
print(
    "Connecting to "
    + SSH_USER
    + "@"
    + CLUSTER_IP
    + "..."
)

if "SSH_OK" not in ssh("echo SSH_OK"):
    print("ERROR: SSH connection test failed.")
    sys.exit(1)

print("SSH connection successful.")

crm_xml = ssh("crm_mon -1 -X")
cib_xml = ssh("cibadmin -Q")
pcs_status = ssh("pcs status --full")


try:
    crm = ET.fromstring(crm_xml)
except Exception as exc:
    print("ERROR parsing crm_mon XML:", exc)
    sys.exit(1)

try:
    cib = ET.fromstring(cib_xml)
except Exception as exc:
    print("ERROR parsing CIB XML:", exc)
    sys.exit(1)


# ============================================================
# CLUSTER NAME
# ============================================================

cluster_name = "Pacemaker Cluster"

for elem in cib.iter():
    if elem.tag == "nvpair":
        if elem.get("name") == "cluster-name":
            cluster_name = elem.get(
                "value",
                cluster_name,
            )
            break


# ============================================================
# NODES
# ============================================================

nodes = {}

for elem in crm.findall(".//nodes/node"):
    name = (
        elem.get("uname")
        or elem.get("name")
        or elem.get("id")
    )

    if not name:
        continue

    nodes[name] = {
        "name": name,
        "online": bool_value(
            elem.get("online", "false")
        ),
        "standby": bool_value(
            elem.get("standby", "false")
        ),
        "maintenance": bool_value(
            elem.get("maintenance", "false")
        ),
    }


# ============================================================
# RESOURCES
# ============================================================

resources = {}


def add_resource(resource_id, active, failed,
                  managed, node, role):
    if not resource_id:
        return

    resources[resource_id] = {
        "id": resource_id,
        "active": active,
        "failed": failed,
        "managed": managed,
        "node": node,
        "role": role,
        "disabled": False,
    }


for elem in crm.iter():
    if elem.tag not in (
        "resource",
        "primitive",
    ):
        continue

    rid = elem.get("id")

    if not rid:
        continue

    active = bool_value(
        elem.get("active", "false")
    )

    failed = bool_value(
        elem.get("failed", "false")
    )

    managed = not (
        elem.get("managed", "true").lower()
        == "false"
    )

    role = elem.get(
        "role",
        "Stopped",
    )

    node = None

    for child in elem:
        if child.tag == "node":
            node = (
                child.get("uname")
                or child.get("name")
            )
            if node:
                break

    add_resource(
        rid,
        active,
        failed,
        managed,
        node,
        role,
    )


# ============================================================
# RESOURCE GROUP
# ============================================================

groups = {}
resources_element = None

for elem in cib.iter():
    if elem.tag == "resources":
        resources_element = elem
        break


def target_role_stopped(element):
    for child in element.iter():
        if child.tag == "nvpair":
            if child.get("name") == "target-role":
                if str(
                    child.get("value", "")
                ).lower() == "stopped":
                    return True
    return False


if resources_element is not None:
    for group in resources_element.findall("group"):
        gid = group.get("id")

        if not gid:
            continue

        members = []

        for primitive in group.findall("primitive"):
            rid = primitive.get("id")
            if rid:
                members.append(rid)

        groups[gid] = {
            "id": gid,
            "members": members,
            "disabled": target_role_stopped(group),
        }


if groups:
    group_id = next(iter(groups))
    group_members = groups[group_id]["members"]
else:
    group_id = "RESOURCE GROUP"
    group_members = []


# ============================================================
# ADMIN-DISABLED RESOURCES
# ============================================================

if resources_element is not None:
    for primitive in resources_element.iter("primitive"):
        rid = primitive.get("id")

        if rid and target_role_stopped(primitive):
            if rid in resources:
                resources[rid]["disabled"] = True


# ============================================================
# FAILED ACTIONS
# ============================================================

failed_actions = []
in_failed = False

resource_names = sorted(
    resources.keys(),
    key=len,
    reverse=True,
)

for raw in pcs_status.splitlines():
    line = raw.strip()

    if line.lower() == "failed resource actions:":
        in_failed = True
        continue

    if not in_failed:
        continue

    if line.startswith("Daemon Status:"):
        break

    if not line.startswith("*"):
        continue

    value = line[1:].strip()

    if not value:
        continue

    rid = None

    for candidate in resource_names:
        if value.startswith(candidate + "_"):
            rid = candidate
            break

    failed_actions.append(
        rid if rid else value
    )


# ============================================================
# CONSTRAINT COUNTS
# ============================================================

constraint_counts = {
    "order": 0,
    "colocation": 0,
    "anti_colocation": 0,
    "location": 0,
    "ticket": 0,
}

constraints_element = None

for elem in cib.iter():
    if elem.tag == "constraints":
        constraints_element = elem
        break

if constraints_element is not None:
    for elem in constraints_element:
        tag = elem.tag.lower()

        if tag == "rsc_order":
            constraint_counts["order"] += 1

        elif tag == "rsc_colocation":
            constraint_counts["colocation"] += 1

            score = elem.get(
                "score",
                "",
            ).upper()

            if (
                score == "-INFINITY"
                or score.startswith("-INFINITY")
            ):
                constraint_counts[
                    "anti_colocation"
                ] += 1

        elif tag == "rsc_location":
            constraint_counts["location"] += 1

        elif tag == "rsc_ticket":
            constraint_counts["ticket"] += 1


# ============================================================
# QUORUM
# ============================================================

quorum = True

if "without quorum" in pcs_status.lower():
    quorum = False

if "partition with quorum" in pcs_status.lower():
    quorum = True


# ============================================================
# RESOURCE CLASSIFICATION
# ============================================================

core_ids = [
    rid for rid in group_members
]

nfsrec_ids = sorted(
    [
        rid for rid in resources
        if re.search(
            r"-nfsrec\d+$",
            rid.lower(),
        )
    ],
    key=lambda x: int(
        re.search(
            r"(\d+)$",
            x,
        ).group(1)
    )
    if re.search(
        r"(\d+)$",
        x,
    )
    else 999,
)

picata_ids = sorted(
    [
        rid for rid in resources
        if re.search(
            r"-picata\d+$",
            rid.lower(),
        )
    ],
    key=lambda x: int(
        re.search(
            r"(\d+)$",
            x,
        ).group(1)
    )
    if re.search(
        r"(\d+)$",
        x,
    )
    else 999,
)

other_ids = [
    rid for rid in resources
    if rid not in core_ids
    and rid not in nfsrec_ids
    and rid not in picata_ids
]


# ============================================================
# ACTIVE / PASSIVE HOST
# ============================================================

active_hosts = set()

for resource in resources.values():
    if resource["active"] and resource["node"]:
        active_hosts.add(resource["node"])

if len(active_hosts) == 1:
    active_host = next(iter(active_hosts))
else:
    active_host = None

passive_hosts = [
    name for name in nodes
    if name != active_host
]


# ============================================================
# HEALTH
# ============================================================

failed_resources = [
    rid for rid, r in resources.items()
    if r["failed"]
]

unmanaged_resources = [
    rid for rid, r in resources.items()
    if not r["managed"]
]

all_nodes_online = (
    len(nodes) == 2
    and all(
        n["online"]
        for n in nodes.values()
    )
)

one_active_host = (
    len(active_hosts) == 1
)

health_ok = (
    len(nodes) == 2
    and len(groups) == 1
    and all_nodes_online
    and quorum
    and one_active_host
    and len(failed_resources) == 0
    and len(failed_actions) == 0
    and len(unmanaged_resources) == 0
)

health_text = (
    "CLUSTER HEALTH: HEALTHY"
    if health_ok
    else "CLUSTER HEALTH: ATTENTION"
)

health_color = GREEN if health_ok else RED
health_fill = (
    LIGHT_GREEN
    if health_ok
    else LIGHT_RED
)


# ============================================================
# CREATE CANVAS
# ============================================================

img = Image.new(
    "RGB",
    (WIDTH, HEIGHT),
    WHITE,
)

draw = ImageDraw.Draw(img)


# ============================================================
# TITLE
# ============================================================

center(
    draw,
    (
        0,
        5,
        WIDTH,
        42,
    ),
    cluster_name
    + " - 1+1 Pacemaker Resource Map",
    F_TITLE,
    DARK,
)

center(
    draw,
    (
        0,
        42,
        WIDTH,
        62,
    ),
    "Connected through "
    + CLUSTER_IP
    + "   |   Generated "
    + datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    ),
    F_SUBTITLE,
    MID_GRAY,
)

# Health badge.
badge_w = 300
badge_h = 42
bx = WIDTH - MARGIN - badge_w
by = 25

round_rect(
    draw,
    (
        bx,
        by,
        bx + badge_w,
        by + badge_h,
    ),
    radius=7,
    fill=health_fill,
    outline=health_color,
    width=2,
)

center(
    draw,
    (
        bx,
        by,
        bx + badge_w,
        by + badge_h,
    ),
    health_text,
    F_SMALL_BOLD,
    health_color,
)


# ============================================================
# NODE PANELS
# ============================================================

node_top = TITLE_H
node_bottom = node_top + NODE_H

node_boxes = {}

node_names = sorted(nodes.keys())

# Ensure two columns if two nodes exist.
if len(node_names) < 2:
    node_names = node_names + [
        "UNAVAILABLE NODE"
    ]

for index, node_name in enumerate(
    node_names[:2]
):

    x1 = (
        MARGIN
        + index * (NODE_W + GAP)
    )

    x2 = x1 + NODE_W

    node = nodes.get(
        node_name,
        {
            "online": False,
            "standby": False,
            "maintenance": False,
        },
    )

    is_active = (
        node_name == active_host
    )

    if not node["online"]:
        header_fill = RED
        status = "OFFLINE"
    elif node["standby"]:
        header_fill = ORANGE
        status = "ONLINE (STANDBY)"
    elif is_active:
        header_fill = GREEN
        status = "ONLINE (ACTIVE NODE)"
    else:
        header_fill = GREEN
        status = "ONLINE"

    node_resources = [
        rid for rid, r in resources.items()
        if r["active"]
        and r["node"] == node_name
    ]

    # Outer node panel.
    round_rect(
        draw,
        (
            x1,
            node_top,
            x2,
            node_bottom,
        ),
        radius=8,
        fill=WHITE,
        outline=BORDER,
        width=1,
    )

    # Header.
    draw.rounded_rectangle(
        (
            x1,
            node_top,
            x2,
            node_top + NODE_HEADER_H,
        ),
        radius=8,
        fill=header_fill,
    )

    draw.rectangle(
        (
            x1,
            node_top + NODE_HEADER_H - 10,
            x2,
            node_top + NODE_HEADER_H,
        ),
        fill=header_fill,
    )

    center(
        draw,
        (
            x1,
            node_top + 6,
            x2,
            node_top + 34,
        ),
        node_name,
        F_NODE,
        WHITE,
    )

    center(
        draw,
        (
            x1,
            node_top + 35,
            x2,
            node_top + 57,
        ),
        status,
        F_NODE_STATUS,
        WHITE,
    )

    center(
        draw,
        (
            x1,
            node_top + 58,
            x2,
            node_top + NODE_HEADER_H,
        ),
        "Resources running: "
        + str(len(node_resources))
        + " / "
        + str(len(resources)),
        F_SMALL,
        WHITE,
    )

    # --------------------------------------------------------
    # Group box
    # --------------------------------------------------------

    gx1 = x1 + 10
    gy1 = node_top + NODE_HEADER_H + 10
    gx2 = x2 - 10
    gy2 = node_bottom - 10

    group_running = (
        is_active
        and len(node_resources) > 0
    )

    group_outline = (
        GREEN
        if group_running
        else BLUE
    )

    round_rect(
        draw,
        (
            gx1,
            gy1,
            gx2,
            gy2,
        ),
        radius=7,
        fill=LIGHT_GRAY,
        outline=group_outline,
        width=2,
    )

    # Group header.
    draw.rectangle(
        (
            gx1,
            gy1,
            gx2,
            gy1 + GROUP_HEADER_H,
        ),
        fill=LIGHT_PURPLE,
    )

    draw.text(
        (
            gx1 + 10,
            gy1 + 11,
        ),
        "Resource Group: "
        + truncate(
            draw,
            group_id,
            F_GROUP,
            560,
        )
        + "  ("
        + str(len(group_members))
        + " core resources)",
        font=F_GROUP,
        fill=PURPLE,
    )

    group_state = (
        "RUNNING"
        if group_running
        else "PASSIVE / EMPTY"
        if not node_resources
        else "NOT RUNNING"
    )

    state_w, _ = txt_size(
        draw,
        group_state,
        F_SMALL_BOLD,
    )

    draw.text(
        (
            gx2 - state_w - 12,
            gy1 + 13,
        ),
        group_state,
        font=F_SMALL_BOLD,
        fill=(
            GREEN
            if group_running
            else ORANGE
            if not node_resources
            else RED
        ),
    )

    # --------------------------------------------------------
    # PASSIVE NODE: absolutely no resources
    # --------------------------------------------------------

    if not node_resources:

        center(
            draw,
            (
                gx1 + 20,
                gy1 + 120,
                gx2 - 20,
                gy1 + 160,
            ),
            "NO RESOURCES RUNNING",
            F_PANEL,
            MID_GRAY,
        )

        center(
            draw,
            (
                gx1 + 20,
                gy1 + 160,
                gx2 - 20,
                gy1 + 195,
            ),
            "1+1 FAILOVER TARGET",
            F_PANEL,
            BLUE,
        )

        center(
            draw,
            (
                gx1 + 20,
                gy1 + 195,
                gx2 - 20,
                gy1 + 225,
            ),
            "Empty by design",
            F_SMALL,
            DARK,
        )

        continue

    # --------------------------------------------------------
    # ACTIVE NODE CONTENT
    # --------------------------------------------------------

    content_x1 = gx1 + 10
    content_x2 = gx2 - 10
    content_w = content_x2 - content_x1

    cy = gy1 + GROUP_HEADER_H + 8

    # CORE
    core_present = [
        rid for rid in core_ids
        if rid in node_resources
    ]

    if core_present:

        round_rect(
            draw,
            (
                content_x1,
                cy,
                content_x2,
                cy + CORE_H,
            ),
            radius=5,
            fill=LIGHT_PURPLE,
            outline=PURPLE,
            width=1,
        )

        draw.text(
            (
                content_x1 + 8,
                cy + 6,
            ),
            "CORE ("
            + str(len(core_present))
            + ")",
            font=F_SECTION,
            fill=PURPLE,
        )

        cell_w = content_w / max(
            len(core_present),
            1,
        )

        for i, rid in enumerate(
            core_present
        ):

            rx1 = (
                content_x1
                + i * cell_w
                + 4
            )
            rx2 = (
                content_x1
                + (i + 1) * cell_w
                - 4
            )

            ry1 = cy + 26
            ry2 = cy + CORE_H - 6

            failed = (
                rid in failed_resources
            )

            fill = (
                LIGHT_RED
                if failed
                else LIGHT_GREEN
            )

            outline = (
                RED
                if failed
                else GREEN
            )

            round_rect(
                draw,
                (
                    rx1,
                    ry1,
                    rx2,
                    ry2,
                ),
                radius=4,
                fill=fill,
                outline=outline,
                width=1,
            )

            label = truncate(
                draw,
                rid,
                F_RESOURCE_SMALL,
                rx2 - rx1 - 8,
            )

            center(
                draw,
                (
                    rx1 + 4,
                    ry1,
                    rx2 - 4,
                    ry2,
                ),
                label,
                F_RESOURCE_SMALL,
                BLACK,
            )

        cy += CORE_H + 8

    # --------------------------------------------------------
    # NFSREC + PICATA SIDE BY SIDE
    # --------------------------------------------------------

    col_gap = 10
    col_w = (
        content_w - col_gap
    ) / 2

    service_defs = [
        (
            "NAS Recorders",
            nfsrec_ids,
        ),
        (
            "Picata Services",
            picata_ids,
        ),
    ]

    for col_index, (
        title,
        ids,
    ) in enumerate(service_defs):

        px1 = (
            content_x1
            + col_index
            * (col_w + col_gap)
        )

        px2 = px1 + col_w

        round_rect(
            draw,
            (
                px1,
                cy,
                px2,
                cy + SERVICE_GRID_H,
            ),
            radius=5,
            fill=LIGHT_BLUE,
            outline=BLUE,
            width=1,
        )

        draw.text(
            (
                px1 + 8,
                cy + 6,
            ),
            title
            + " ("
            + str(len(ids))
            + ")",
            font=F_SECTION,
            fill=BLUE,
        )

        # 2 columns x 14 rows.
        inner_gap = 5
        cell_w = (
            col_w - 10 - inner_gap
        ) / 2

        start_y = (
            cy
            + SERVICE_HEADER_H
        )

        for i, rid in enumerate(ids):

            col = i % 2
            row = i // 2

            rx1 = (
                px1
                + 5
                + col
                * (cell_w + inner_gap)
            )

            rx2 = (
                rx1 + cell_w
            )

            ry1 = (
                start_y
                + row
                * (RESOURCE_H + RESOURCE_GAP)
            )

            ry2 = ry1 + RESOURCE_H

            failed = (
                rid in failed_resources
            )

            fill = (
                LIGHT_RED
                if failed
                else LIGHT_GREEN
            )

            outline = (
                RED
                if failed
                else GREEN
            )

            round_rect(
                draw,
                (
                    rx1,
                    ry1,
                    rx2,
                    ry2,
                ),
                radius=3,
                fill=fill,
                outline=outline,
                width=1,
            )

            label = truncate(
                draw,
                rid,
                F_RESOURCE_SMALL,
                rx2 - rx1 - 8,
            )

            draw.text(
                (
                    rx1 + 4,
                    ry1 + 7,
                ),
                label,
                font=F_RESOURCE_SMALL,
                fill=BLACK,
            )

        # No vertical overlap: both service panels share exactly
        # the same cy and fixed SERVICE_GRID_H.
    cy += SERVICE_GRID_H + 8

    # --------------------------------------------------------
    # OTHER
    # --------------------------------------------------------

    if other_ids:

        round_rect(
            draw,
            (
                content_x1,
                cy,
                content_x2,
                cy + OTHER_H,
            ),
            radius=5,
            fill=LIGHT_BLUE,
            outline=BLUE,
            width=1,
        )

        draw.text(
            (
                content_x1 + 8,
                cy + 6,
            ),
            "Configuration Updater ("
            + str(len(other_ids))
            + ")",
            font=F_SECTION,
            fill=BLUE,
        )

        label = truncate(
            draw,
            ", ".join(other_ids),
            F_RESOURCE_SMALL,
            content_w - 16,
        )

        draw.text(
            (
                content_x1 + 8,
                cy + 25,
            ),
            label,
            font=F_RESOURCE_SMALL,
            fill=BLACK,
        )


# ============================================================
# BOTTOM SUMMARY AREA
# ============================================================

summary_top = node_bottom + GAP
summary_bottom = HEIGHT - MARGIN

# Layout safety check: bottom summary must never overlap the node panels.
if summary_top >= summary_bottom:
    raise RuntimeError(
        "Invalid layout: bottom summary has no available vertical space."
    )

summary_w = (
    WIDTH
    - 2 * MARGIN
    - 4 * GAP
) / 5


def panel(x, title, color):
    round_rect(
        draw,
        (
            x,
            summary_top,
            x + summary_w,
            summary_bottom,
        ),
        radius=7,
        fill=WHITE,
        outline=color,
        width=2,
    )

    draw.rectangle(
        (
            x,
            summary_top,
            x + summary_w,
            summary_top + 35,
        ),
        fill=color,
    )

    draw.text(
        (
            x + 10,
            summary_top + 9,
        ),
        title,
        font=F_PANEL,
        fill=WHITE,
    )


# ============================================================
# PANEL 1: CLUSTER SUMMARY
# ============================================================

x = MARGIN

panel(
    x,
    "CLUSTER SUMMARY",
    BLUE,
)

summary_items = [
    ("Cluster name", cluster_name),
    ("Nodes configured", str(len(nodes))),
    ("Resource groups", str(len(groups))),
    ("Total resources", str(len(resources))),
    (
        "Running resources",
        str(sum(
            1 for r in resources.values()
            if r["active"]
        )),
    ),
    (
        "Failed resources",
        str(len(failed_resources)),
    ),
    (
        "Failed actions",
        str(len(failed_actions)),
    ),
    (
        "Quorum",
        "Present" if quorum else "NOT PRESENT",
    ),
]

py = summary_top + 52

for label, value in summary_items:

    draw.text(
        (x + 10, py),
        label,
        font=F_PANEL_LABEL,
        fill=DARK,
    )

    value = truncate(
        draw,
        value,
        F_PANEL_VALUE,
        summary_w - 120,
    )

    vw, _ = txt_size(
        draw,
        value,
        F_PANEL_VALUE,
    )

    draw.text(
        (
            x + summary_w - 10 - vw,
            py,
        ),
        value,
        font=F_PANEL_VALUE,
        fill=(
            GREEN
            if label == "Quorum"
            and quorum
            else RED
            if (
                "Failed" in label
                and value != "0"
            )
            else DARK
        ),
    )

    py += 25


# ============================================================
# PANEL 2: RESOURCE DISTRIBUTION
# ============================================================

x = MARGIN + (summary_w + GAP)

panel(
    x,
    "RESOURCE DISTRIBUTION",
    GREEN,
)

draw.text(
    (x + 10, summary_top + 48),
    "Node",
    font=F_PANEL_VALUE,
    fill=DARK,
)

draw.text(
    (x + summary_w - 80, summary_top + 48),
    "Count",
    font=F_PANEL_VALUE,
    fill=DARK,
)

py = summary_top + 76

for node_name in node_names[:2]:

    count = sum(
        1 for r in resources.values()
        if r["active"]
        and r["node"] == node_name
    )

    draw.text(
        (
            x + 10,
            py,
        ),
        truncate(
            draw,
            node_name,
            F_PANEL_LABEL,
            summary_w - 100,
        ),
        font=F_PANEL_LABEL,
        fill=DARK,
    )

    draw.text(
        (
            x + summary_w - 70,
            py,
        ),
        str(count),
        font=F_PANEL_VALUE,
        fill=GREEN if count else MID_GRAY,
    )

    py += 25

draw.line(
    (
        x + 10,
        py + 4,
        x + summary_w - 10,
        py + 4,
    ),
    fill=BORDER,
)

py += 18

draw.text(
    (x + 10, py),
    "Active host",
    font=F_PANEL_LABEL,
    fill=DARK,
)

draw.text(
    (
        x + 10,
        py + 22,
    ),
    truncate(
        draw,
        active_host or "NONE",
        F_PANEL_VALUE,
        summary_w - 20,
    ),
    font=F_PANEL_VALUE,
    fill=GREEN if active_host else RED,
)


# ============================================================
# PANEL 3: RESOURCE BREAKDOWN
# ============================================================

x = MARGIN + 2 * (summary_w + GAP)

panel(
    x,
    "RESOURCE BREAKDOWN",
    BLUE,
)

breakdown = [
    ("Core group members", len(core_ids)),
    ("NFSREC services", len(nfsrec_ids)),
    ("Picata services", len(picata_ids)),
    ("Configuration updater", sum(
        1 for rid in other_ids
        if "pctcfg-updater" in rid.lower()
    )),
    (
        "Other resources",
        len([
            rid for rid in other_ids
            if "pctcfg-updater" not in rid.lower()
        ]),
    ),
    ("Total", len(resources)),
]

py = summary_top + 54

for label, count in breakdown:

    draw.text(
        (
            x + 10,
            py,
        ),
        label,
        font=F_PANEL_LABEL,
        fill=DARK,
    )

    count_text = str(count)
    cw, _ = txt_size(
        draw,
        count_text,
        F_PANEL_VALUE,
    )

    draw.text(
        (
            x + summary_w - 10 - cw,
            py,
        ),
        count_text,
        font=F_PANEL_VALUE,
        fill=DARK,
    )

    py += 28


# ============================================================
# PANEL 4: CIB CONSTRAINTS
# ============================================================

x = MARGIN + 3 * (summary_w + GAP)

panel(
    x,
    "CIB CONSTRAINTS",
    PURPLE,
)

constraint_rows = [
    ("Order constraints", constraint_counts["order"]),
    ("Colocation constraints", constraint_counts["colocation"]),
    ("Anti-colocation", constraint_counts["anti_colocation"]),
    ("Location constraints", constraint_counts["location"]),
    ("Ticket constraints", constraint_counts["ticket"]),
]

py = summary_top + 54

for label, count in constraint_rows:

    draw.text(
        (
            x + 10,
            py,
        ),
        label,
        font=F_PANEL_LABEL,
        fill=DARK,
    )

    value = str(count)
    vw, _ = txt_size(
        draw,
        value,
        F_PANEL_VALUE,
    )

    draw.text(
        (
            x + summary_w - 10 - vw,
            py,
        ),
        value,
        font=F_PANEL_VALUE,
        fill=DARK,
    )

    py += 25

draw.line(
    (
        x + 10,
        py + 3,
        x + summary_w - 10,
        py + 3,
    ),
    fill=BORDER,
)

draw.text(
    (
        x + 10,
        py + 15,
    ),
    "Constraints are informational;",
    font=F_SMALL_BOLD,
    fill=PURPLE,
)

draw.text(
    (
        x + 10,
        py + 32,
    ),
    "they do not create a health alert.",
    font=F_SMALL,
    fill=DARK,
)


# ============================================================
# PANEL 5: CLUSTER HEALTH
# ============================================================

x = MARGIN + 4 * (summary_w + GAP)

panel(
    x,
    "CLUSTER HEALTH",
    GREEN if health_ok else RED,
)

health_rows = [
    (
        all_nodes_online,
        "2 nodes online",
    ),
    (
        one_active_host,
        "1 node active, 1 failover target",
    ),
    (
        quorum,
        "Quorum present",
    ),
    (
        len(failed_resources) == 0,
        "No failed resources",
    ),
    (
        len(failed_actions) == 0,
        "No failed actions",
    ),
    (
        len(unmanaged_resources) == 0,
        "No unmanaged resources",
    ),
]

py = summary_top + 54

for ok, label in health_rows:

    color = GREEN if ok else RED

    draw.ellipse(
        (
            x + 10,
            py + 1,
            x + 22,
            py + 13,
        ),
        fill=color,
    )

    draw.text(
        (
            x + 30,
            py,
        ),
        label,
        font=F_SMALL,
        fill=DARK if ok else RED,
    )

    py += 25

draw.line(
    (
        x + 10,
        py + 3,
        x + summary_w - 10,
        py + 3,
    ),
    fill=BORDER,
)

py += 14

if health_ok:
    draw.text(
        (
            x + 10,
            py,
        ),
        "1+1 standby node with 0 resources",
        font=F_SMALL_BOLD,
        fill=GREEN,
    )

    draw.text(
        (
            x + 10,
            py + 18,
        ),
        "is an expected healthy state.",
        font=F_SMALL,
        fill=DARK,
    )
else:
    draw.text(
        (
            x + 10,
            py,
        ),
        "Review failed resources/actions",
        font=F_SMALL_BOLD,
        fill=RED,
    )


# ============================================================
# FOOTER
# ============================================================

draw.text(
    (
        MARGIN,
        HEIGHT - 14,
    ),
    "Legend: ",
    font=F_SMALL_BOLD,
    fill=DARK,
)

legend_items = [
    ("RUNNING / ACTIVE", GREEN),
    ("PASSIVE / EMPTY", ORANGE),
    ("FAILED", RED),
    ("RESOURCE GROUP", PURPLE),
]

lx = MARGIN + 55

for label, color in legend_items:

    draw.ellipse(
        (
            lx,
            HEIGHT - 15,
            lx + 10,
            HEIGHT - 5,
        ),
        fill=color,
    )

    draw.text(
        (
            lx + 15,
            HEIGHT - 17,
        ),
        label,
        font=F_SMALL,
        fill=DARK,
    )

    lw, _ = txt_size(
        draw,
        label,
        F_SMALL,
    )

    lx += lw + 40


# ============================================================
# SAVE
# ============================================================

timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
)

output_file = (
    OUTPUT_DIR
    / (
        cluster_name.replace(" ", "_")
        + "_1plus1_landscape_"
        + timestamp
        + ".png"
    )
)

img.save(
    output_file,
    "PNG",
)

# ============================================================
# CONSOLE SUMMARY
# ============================================================

print()
print("=" * 80)
print("REPORT GENERATED")
print("=" * 80)
print()
print("Cluster          :", cluster_name)
print("Nodes            :", len(nodes))
print("Resource groups  :", len(groups))
print("Total resources  :", len(resources))
print("Core members     :", len(core_ids))
print("NFSREC           :", len(nfsrec_ids))
print("Picata           :", len(picata_ids))
print("Other            :", len(other_ids))
print("Active host      :", active_host or "NONE")
print("Passive target   :", ", ".join(passive_hosts) or "NONE")
print("Failed resources :", len(failed_resources))
print("Failed actions   :", len(failed_actions))
print("Quorum           :", "Present" if quorum else "NOT PRESENT")
print("Health           :", "HEALTHY" if health_ok else "ATTENTION")
print()
print("Output:")
print(str(output_file))
print()
print("=" * 80)
