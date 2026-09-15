#!/usr/bin/env python3

import os
import sys
import subprocess
import tempfile
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
from collections import defaultdict

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("ERROR: Pillow is not installed.")
    print()
    print('Install with:')
    print('    python -m pip install "Pillow==8.4.0"')
    sys.exit(1)


# ============================================================
# CONFIGURATION
# ============================================================

# ------------------------------------------------------------
# Cluster node IP, hostname or VIP
# ------------------------------------------------------------

CLUSTER_IP = "10.101.28.27"

# ------------------------------------------------------------
# SSH credentials
# ------------------------------------------------------------

ssh_user = "root"

ssh_password = "Th@les01"

ssh_port = 22

# ------------------------------------------------------------
# Output directory
# ------------------------------------------------------------

OUTPUT_DIR = Path.cwd() / "cluster-diagrams"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# IMAGE CONFIGURATION
# ============================================================

SIDE_MARGIN = 35

TOP_MARGIN = 130

BOTTOM_MARGIN = 65

NODE_WIDTH = 300

NODE_GAP = 18

NODE_HEADER_HEIGHT = 105

NODE_RESOURCE_HEIGHT = 34

NODE_RESOURCE_GAP = 5

SERVICE_HEADER_HEIGHT = 34

SERVICE_RESOURCE_HEIGHT = 28

SERVICE_GAP = 5

PANEL_GAP = 12

PANEL_HEADER_HEIGHT = 38

PANEL_PADDING = 12

FONT_TITLE = 30
FONT_SUBTITLE = 15

FONT_NODE = 17
FONT_NODE_STATUS = 15

FONT_COUNT = 13

FONT_SERVICE = 15
FONT_RESOURCE = 12

FONT_PANEL = 15
FONT_PANEL_TEXT = 12

FONT_SMALL = 11

FONT_LEGEND = 11


# ============================================================
# COLORS
# ============================================================

WHITE = "#FFFFFF"

BLACK = "#111111"

DARK_BLUE = "#173A75"

BLUE = "#1565C0"
LIGHT_BLUE = "#EAF3FF"

GREEN = "#1B8E3E"
LIGHT_GREEN = "#E7F5E9"

DARK_GREEN = "#0B6B2D"

ORANGE = "#E68A00"
LIGHT_ORANGE = "#FFF1D6"

RED = "#C40000"
LIGHT_RED = "#FCE7E7"

PURPLE = "#7026A0"
LIGHT_PURPLE = "#F0E7F7"

GRAY = "#777777"
DARK_GRAY = "#444444"
LIGHT_GRAY = "#F2F3F5"

BORDER = "#AAB2BD"

CYAN = "#087E8B"
LIGHT_CYAN = "#E4F6F8"


# ============================================================
# FONTS
# ============================================================

def get_font(size, bold=False):

    if bold:

        candidates = [
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/segoeuib.ttf",
            "C:/Windows/Fonts/calibrib.ttf"
        ]

    else:

        candidates = [
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/segoeui.ttf",
            "C:/Windows/Fonts/calibri.ttf"
        ]

    for path in candidates:

        if Path(path).exists():

            return ImageFont.truetype(
                path,
                size
            )

    return ImageFont.load_default()


TITLE_FONT = get_font(FONT_TITLE, True)

SUBTITLE_FONT = get_font(
    FONT_SUBTITLE,
    False
)

NODE_FONT = get_font(
    FONT_NODE,
    True
)

NODE_STATUS_FONT = get_font(
    FONT_NODE_STATUS,
    True
)

COUNT_FONT = get_font(
    FONT_COUNT,
    False
)

SERVICE_FONT = get_font(
    FONT_SERVICE,
    True
)

RESOURCE_FONT = get_font(
    FONT_RESOURCE,
    False
)

PANEL_FONT = get_font(
    FONT_PANEL,
    True
)

PANEL_TEXT_FONT = get_font(
    FONT_PANEL_TEXT,
    False
)

PANEL_TEXT_BOLD = get_font(
    FONT_PANEL_TEXT,
    True
)

SMALL_FONT = get_font(
    FONT_SMALL,
    False
)

LEGEND_FONT = get_font(
    FONT_LEGEND,
    False
)


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def shorten(text, length):

    if text is None:
        return ""

    if len(text) <= length:
        return text

    return text[:length - 3] + "..."


def text_size(draw, text, font):

    bbox = draw.textbbox(
        (0, 0),
        text,
        font=font
    )

    return (
        bbox[2] - bbox[0],
        bbox[3] - bbox[1]
    )


def centered_text(
    draw,
    x,
    y,
    text,
    font,
    fill
):

    width, height = text_size(
        draw,
        text,
        font
    )

    draw.text(
        (
            x - width / 2,
            y - height / 2
        ),
        text,
        font=font,
        fill=fill
    )


def safe_name(text):

    return (
        text
        .replace("/", "_")
        .replace("\\", "_")
        .replace(" ", "_")
        .replace(":", "_")
    )


# ============================================================
# SSH ASKPASS
# ============================================================

def create_askpass_script(password):

    temp_dir = tempfile.mkdtemp(
        prefix="cluster_diagram_"
    )

    askpass_file = os.path.join(
        temp_dir,
        "askpass.cmd"
    )

    # The password is returned to OpenSSH when it invokes
    # SSH_ASKPASS.
    #
    # NOTE:
    # Avoid CMD-special characters such as &, |, <, >,
    # ^, %, ! in the password if possible.

    with open(
        askpass_file,
        "w"
    ) as f:

        f.write("@echo off\n")
        f.write(
            "echo "
            + password
            + "\n"
        )

    return temp_dir, askpass_file


# ============================================================
# SSH COMMAND
# ============================================================

def ssh_command(command):

    temp_dir = None

    try:

        temp_dir, askpass_file = (
            create_askpass_script(
                ssh_password
            )
        )

        environment = os.environ.copy()

        environment[
            "SSH_ASKPASS"
        ] = askpass_file

        environment[
            "SSH_ASKPASS_REQUIRE"
        ] = "force"

        environment[
            "DISPLAY"
        ] = "none:0"

        command_line = [

            "ssh",

            "-p",
            str(ssh_port),

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

            ssh_user
            + "@"
            + CLUSTER_IP,

            command
        ]

        result = subprocess.run(

            command_line,

            stdout=subprocess.PIPE,

            stderr=subprocess.PIPE,

            universal_newlines=True,

            env=environment
        )

        if result.returncode != 0:

            print()
            print("=" * 80)
            print("SSH COMMAND FAILED")
            print("=" * 80)
            print()
            print(
                "Target: "
                + ssh_user
                + "@"
                + CLUSTER_IP
            )
            print()
            print(
                "Command:"
            )
            print(command)
            print()
            print(
                "SSH error:"
            )
            print(result.stderr)

            sys.exit(1)

        return result.stdout

    finally:

        if temp_dir:

            shutil.rmtree(
                temp_dir,
                ignore_errors=True
            )


# ============================================================
# CONNECTIVITY TEST
# ============================================================

print()
print("=" * 80)
print("PACEMAKER CLUSTER RESOURCE MAP")
print("=" * 80)
print()

print(
    "Connecting to: "
    + ssh_user
    + "@"
    + CLUSTER_IP
)

print()

print("Testing SSH connection...")

ssh_result = ssh_command(
    "echo SSH_CONNECTION_OK"
)

if "SSH_CONNECTION_OK" not in ssh_result:

    print(
        "ERROR: SSH connection test failed."
    )

    sys.exit(1)

print("SSH connection successful.")


# ============================================================
# GET PACEMAKER XML
# ============================================================

print(
    "Getting Pacemaker status..."
)

crm_xml = ssh_command(
    "crm_mon -1 -X"
)

print(
    "Getting Pacemaker CIB..."
)

cib_xml = ssh_command(
    "cibadmin -Q"
)


# ============================================================
# PARSE XML
# ============================================================

try:

    crm_root = ET.fromstring(
        crm_xml
    )

except Exception as e:

    print()
    print(
        "ERROR parsing crm_mon XML:"
    )
    print(str(e))
    sys.exit(1)


try:

    cib_root = ET.fromstring(
        cib_xml
    )

except Exception as e:

    print()
    print(
        "ERROR parsing CIB XML:"
    )
    print(str(e))
    sys.exit(1)


# ============================================================
# CLUSTER NAME
# ============================================================

cluster_name = "Pacemaker Cluster"

for elem in cib_root.iter():

    if elem.tag == "nvpair":

        if elem.get("name") == "cluster-name":

            cluster_name = elem.get(
                "value",
                cluster_name
            )

            break


# ============================================================
# NODE INFORMATION
# ============================================================

nodes = {}


for node in crm_root.findall(
    ".//nodes/node"
):

    node_name = (

        node.get("uname")
        or node.get("name")
        or node.get("id")
    )

    if not node_name:
        continue

    online = (
        node.get(
            "online",
            "false"
        ).lower()
        == "true"
    )

    standby = (
        node.get(
            "standby",
            "false"
        ).lower()
        == "true"
    )

    maintenance = (
        node.get(
            "maintenance",
            "false"
        ).lower()
        == "true"
    )

    # Pacemaker can report standby in different forms.
    if node.get("standby") == "on":
        standby = True

    nodes[node_name] = {

        "name": node_name,

        "online": online,

        "standby": standby,

        "maintenance": maintenance,

        "resources": []
    }


# ============================================================
# RESOURCE INFORMATION
# ============================================================

resources = {}


def add_resource(
    resource_id,
    active=False,
    failed=False,
    managed=True,
    node=None,
    role="Stopped",
    resource_type="primitive"
):

    if not resource_id:
        return

    if resource_id not in resources:

        resources[resource_id] = {

            "id": resource_id,

            "active": active,

            "failed": failed,

            "managed": managed,

            "node": node,

            "role": role,

            "type": resource_type
        }

    else:

        resource = resources[
            resource_id
        ]

        if active:
            resource["active"] = True

        if failed:
            resource["failed"] = True

        if node:
            resource["node"] = node

        if role:
            resource["role"] = role

        if not managed:
            resource["managed"] = False


# ------------------------------------------------------------
# crm_mon resource parsing
# ------------------------------------------------------------

for elem in crm_root.iter():

    if elem.tag not in (
        "resource",
        "primitive"
    ):
        continue

    resource_id = elem.get("id")

    if not resource_id:
        continue

    active = (
        elem.get(
            "active",
            "false"
        ).lower()
        == "true"
    )

    failed = (
        elem.get(
            "failed",
            "false"
        ).lower()
        == "true"
    )

    managed = (
        elem.get(
            "managed",
            "true"
        ).lower()
        != "false"
    )

    role = elem.get(
        "role",
        "Stopped"
    )

    running_node = None

    for child in elem:

        if child.tag == "node":

            running_node = (

                child.get("uname")
                or child.get("name")
            )

            if running_node:
                break

    add_resource(

        resource_id,

        active,

        failed,

        managed,

        running_node,

        role
    )


# ============================================================
# FAILED RESOURCE DETECTION
# ============================================================

failed_resources = set()


for elem in crm_root.iter():

    resource_id = elem.get(
        "resource"
    )

    if not resource_id:
        continue

    if (
        elem.get(
            "failed",
            ""
        ).lower()
        == "true"
    ):

        failed_resources.add(
            resource_id
        )


for resource_id, resource in resources.items():

    if resource["failed"]:

        failed_resources.add(
            resource_id
        )


# ============================================================
# RESOURCE GROUPS
# ============================================================

groups = {}


resources_section = None


for elem in cib_root.iter():

    if elem.tag == "resources":

        resources_section = elem

        break


if resources_section is not None:

    for group in resources_section.findall(
        "group"
    ):

        group_id = group.get(
            "id"
        )

        if not group_id:
            continue

        members = []

        for primitive in group.findall(
            "primitive"
        ):

            resource_id = primitive.get(
                "id"
            )

            if resource_id:

                members.append(
                    resource_id
                )

        groups[group_id] = {

            "id": group_id,

            "members": members
        }


# ============================================================
# RESOURCE -> GROUP
# ============================================================

resource_to_group = {}


for group_id, group in groups.items():

    for resource_id in group["members"]:

        resource_to_group[
            resource_id
        ] = group_id


# ============================================================
# ADD RESOURCES TO NODES
# ============================================================

for resource_id, resource in resources.items():

    node_name = resource["node"]

    if not node_name:
        continue

    if node_name not in nodes:

        nodes[node_name] = {

            "name": node_name,

            "online": True,

            "standby": False,

            "maintenance": False,

            "resources": []
        }

    if resource_id not in nodes[
        node_name
    ]["resources"]:

        nodes[
            node_name
        ]["resources"].append(
            resource_id
        )


# ============================================================
# CONSTRAINT INFORMATION
# ============================================================

constraint_counts = {

    "order": 0,

    "colocation": 0,

    "location": 0,

    "ticket": 0,

    "anti_colocation": 0
}


constraints_section = None


for elem in cib_root.iter():

    if elem.tag == "constraints":

        constraints_section = elem

        break


if constraints_section is not None:

    for constraint in constraints_section:

        tag = constraint.tag.lower()

        if tag == "rsc_order":

            constraint_counts[
                "order"
            ] += 1

        elif tag == "rsc_colocation":

            constraint_counts[
                "colocation"
            ] += 1

            score = constraint.get(
                "score",
                ""
            ).upper()

            if (
                score == "-INFINITY"
                or score.startswith(
                    "-INFINITY"
                )
            ):

                constraint_counts[
                    "anti_colocation"
                ] += 1

        elif tag == "rsc_location":

            constraint_counts[
                "location"
            ] += 1

        elif tag == "rsc_ticket":

            constraint_counts[
                "ticket"
            ] += 1


# ============================================================
# QUORUM
# ============================================================

quorum_present = True

# Look for quorum-related status in crm_mon XML.
# Pacemaker 2.x generally exposes quorum through status/
# tickets/node information, but the exact XML layout can vary.

crm_text_lower = crm_xml.lower()

if "partition with quorum" in crm_text_lower:

    quorum_present = True

elif "without quorum" in crm_text_lower:

    quorum_present = False


# ============================================================
# GROUP HEALTH
# ============================================================

group_states = {}


for group_id, group in groups.items():

    running = []

    stopped = []

    failed = []

    unmanaged = []

    for resource_id in group["members"]:

        resource = resources.get(
            resource_id
        )

        if resource is None:

            stopped.append(
                resource_id
            )

            continue

        if not resource["managed"]:

            unmanaged.append(
                resource_id
            )

        if resource_id in failed_resources:

            failed.append(
                resource_id
            )

        if (
            resource["active"]
            and resource["node"]
        ):

            running.append(
                resource_id
            )

        else:

            stopped.append(
                resource_id
            )

    if len(running) == 0:

        state = "NOT RUNNING"

    elif (
        stopped
        or failed
        or unmanaged
    ):

        state = "DEGRADED"

    else:

        state = "RUNNING"

    group_states[group_id] = {

        "state": state,

        "running": running,

        "stopped": stopped,

        "failed": failed,

        "unmanaged": unmanaged
    }


# ============================================================
# RESOURCE COUNTS
# ============================================================

running_count = 0
stopped_count = 0
failed_count = 0
unmanaged_count = 0


for resource_id, resource in resources.items():

    if resource["active"]:

        running_count += 1

    else:

        stopped_count += 1

    if resource_id in failed_resources:

        failed_count += 1

    if not resource["managed"]:

        unmanaged_count += 1


# ============================================================
# NODE COUNTS
# ============================================================

online_nodes = 0
standby_nodes = 0
offline_nodes = 0
maintenance_nodes = 0


for node in nodes.values():

    if node["maintenance"]:

        maintenance_nodes += 1

    elif not node["online"]:

        offline_nodes += 1

    elif node["standby"]:

        standby_nodes += 1

    else:

        online_nodes += 1


# ============================================================
# GROUP COUNTS
# ============================================================

running_groups = 0
degraded_groups = 0
stopped_groups = 0


for state in group_states.values():

    if state["state"] == "RUNNING":

        running_groups += 1

    elif state["state"] == "DEGRADED":

        degraded_groups += 1

    else:

        stopped_groups += 1


# ============================================================
# CLNVRM DETECTION
# ============================================================

clnvrm_instances = defaultdict(
    lambda: {
        "resources": [],
        "nodes": set()
    }
)


for resource_id, resource in resources.items():

    resource_lower = resource_id.lower()

    if resource_lower.startswith(
        "clnvrm"
    ):

        parts = resource_lower.split(
            "-"
        )

        if len(parts) >= 1:

            instance = parts[0]

            clnvrm_instances[
                instance
            ]["resources"].append(
                resource_id
            )

            if resource["node"]:

                clnvrm_instances[
                    instance
                ]["nodes"].add(
                    resource["node"]
                )


# ============================================================
# NODE HEIGHT CALCULATION
# ============================================================

def node_height(node):

    resource_count = len(
        node["resources"]
    )

    return (

        NODE_HEADER_HEIGHT

        + 20

        + resource_count
        * (
            NODE_RESOURCE_HEIGHT
            + NODE_RESOURCE_GAP
        )

        + 20
    )


node_heights = {}

for node_name, node in nodes.items():

    node_heights[
        node_name
    ] = node_height(
        node
    )


max_node_height = max(
    node_heights.values(),
    default=300
)


# ============================================================
# DASHBOARD PANEL HEIGHT
# ============================================================

bottom_panel_height = 370


# ============================================================
# IMAGE DIMENSIONS
# ============================================================

node_names = sorted(
    nodes.keys()
)


node_count = max(
    len(node_names),
    1
)


image_width = (

    SIDE_MARGIN * 2

    + node_count
    * NODE_WIDTH

    + (node_count - 1)
    * NODE_GAP
)


image_height = (

    TOP_MARGIN

    + max_node_height

    + PANEL_GAP

    + bottom_panel_height

    + BOTTOM_MARGIN
)


# ============================================================
# CREATE IMAGE
# ============================================================

image = Image.new(
    "RGB",
    (
        image_width,
        image_height
    ),
    WHITE
)


draw = ImageDraw.Draw(
    image
)


# ============================================================
# TITLE
# ============================================================

centered_text(

    draw,

    image_width // 2,

    28,

    cluster_name
    + " - Pacemaker Cluster Resource Map",

    TITLE_FONT,

    DARK_BLUE
)


centered_text(

    draw,

    image_width // 2,

    58,

    "Connected through "
    + CLUSTER_IP
    + "   |   Generated: "
    + datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    ),

    SUBTITLE_FONT,

    GRAY
)


# ============================================================
# TOP RIGHT HEALTH BADGE
# ============================================================

cluster_healthy = (

    online_nodes == len(nodes)

    and standby_nodes == 0

    and offline_nodes == 0

    and maintenance_nodes == 0

    and running_groups == len(groups)

    and degraded_groups == 0

    and stopped_groups == 0

    and failed_count == 0

    and stopped_count == 0

    and unmanaged_count == 0

    and quorum_present
)


if cluster_healthy:

    health_text = "CLUSTER HEALTH: HEALTHY"

    health_subtext = (
        "All nodes and resources are "
        "running normally"
    )

    health_color = GREEN

    health_fill = LIGHT_GREEN

else:

    health_text = "CLUSTER HEALTH: ATTENTION"

    health_subtext = (
        "One or more cluster conditions "
        "require review"
    )

    health_color = RED

    health_fill = LIGHT_RED


badge_width = 330
badge_height = 58

badge_x1 = (
    image_width
    - SIDE_MARGIN
    - badge_width
)

badge_y1 = 8

draw.rounded_rectangle(

    (
        badge_x1,
        badge_y1,
        badge_x1 + badge_width,
        badge_y1 + badge_height
    ),

    radius=8,

    outline=health_color,

    width=2,

    fill=health_fill
)


draw.ellipse(

    (
        badge_x1 + 12,
        badge_y1 + 12,
        badge_x1 + 42,
        badge_y1 + 42
    ),

    fill=health_color
)


centered_text(

    draw,

    badge_x1 + 27,

    badge_y1 + 27,

    "✓" if cluster_healthy else "!",

    PANEL_TEXT_BOLD,

    WHITE
)


draw.text(

    (
        badge_x1 + 52,
        badge_y1 + 10
    ),

    health_text,

    font=PANEL_TEXT_BOLD,

    fill=health_color
)


draw.text(

    (
        badge_x1 + 52,
        badge_y1 + 32
    ),

    health_subtext,

    font=SMALL_FONT,

    fill=DARK_GREEN
    if cluster_healthy
    else RED
)


# ============================================================
# NODE DRAWING
# ============================================================

node_y = TOP_MARGIN


for node_name in node_names:

    node = nodes[node_name]

    x = (
        SIDE_MARGIN
        + node_names.index(node_name)
        * (
            NODE_WIDTH
            + NODE_GAP
        )
    )


    # --------------------------------------------------------
    # Determine node status
    # --------------------------------------------------------

    if node["maintenance"]:

        status = "MAINTENANCE"

        header_color = GRAY

    elif not node["online"]:

        status = "OFFLINE"

        header_color = RED

    elif node["standby"]:

        status = "STANDBY"

        header_color = ORANGE

    else:

        status = "ONLINE"

        header_color = GREEN


    # --------------------------------------------------------
    # Node box
    # --------------------------------------------------------

    draw.rounded_rectangle(

        (
            x,
            node_y,
            x + NODE_WIDTH,
            node_y + max_node_height
        ),

        radius=9,

        outline=BORDER,

        width=2,

        fill=WHITE
    )


    # --------------------------------------------------------
    # Header
    # --------------------------------------------------------

    draw.rounded_rectangle(

        (
            x,
            node_y,
            x + NODE_WIDTH,
            node_y + NODE_HEADER_HEIGHT
        ),

        radius=9,

        fill=header_color
    )


    draw.rectangle(

        (
            x,
            node_y
            + NODE_HEADER_HEIGHT
            - 10,
            x + NODE_WIDTH,
            node_y
            + NODE_HEADER_HEIGHT
        ),

        fill=header_color
    )


    centered_text(

        draw,

        x + NODE_WIDTH // 2,

        node_y + 25,

        shorten(
            node_name,
            29
        ),

        NODE_FONT,

        WHITE
    )


    # --------------------------------------------------------
    # Status
    # --------------------------------------------------------

    centered_text(

        draw,

        x + NODE_WIDTH // 2,

        node_y + 58,

        status,

        NODE_STATUS_FONT,

        WHITE
    )


    # --------------------------------------------------------
    # Resource count
    # --------------------------------------------------------

    centered_text(

        draw,

        x + NODE_WIDTH // 2,

        node_y + 84,

        "Resources: "
        + str(
            len(node["resources"])
        ),

        COUNT_FONT,

        WHITE
    )


    # --------------------------------------------------------
    # Resources
    # --------------------------------------------------------

    resource_y = (

        node_y
        + NODE_HEADER_HEIGHT
        + 12
    )


    for resource_id in sorted(
        node["resources"]
    ):

        resource = resources.get(
            resource_id
        )

        if resource is None:
            continue


        # Resource state

        if resource_id in failed_resources:

            resource_fill = LIGHT_RED

            resource_outline = RED

            state_text = "FAILED"

            state_color = RED

        elif not resource["managed"]:

            resource_fill = LIGHT_GRAY

            resource_outline = GRAY

            state_text = "UNMANAGED"

            state_color = GRAY

        elif not resource["active"]:

            resource_fill = LIGHT_ORANGE

            resource_outline = ORANGE

            state_text = "STOPPED"

            state_color = ORANGE

        else:

            resource_fill = LIGHT_GREEN

            resource_outline = GREEN

            state_text = "RUNNING"

            state_color = GREEN


        draw.rounded_rectangle(

            (
                x + 8,
                resource_y,
                x + NODE_WIDTH - 8,
                resource_y
                + NODE_RESOURCE_HEIGHT
            ),

            radius=5,

            outline=resource_outline,

            width=1,

            fill=resource_fill
        )


        group_id = resource_to_group.get(
            resource_id
        )


        if group_id:

            display_name = shorten(
                resource_id,
                25
            )

        else:

            display_name = shorten(
                resource_id,
                27
            )


        draw.text(

            (
                x + 16,
                resource_y + 9
            ),

            display_name,

            font=RESOURCE_FONT,

            fill=BLACK
        )


        state_width, _ = text_size(

            draw,

            state_text,

            SMALL_FONT
        )


        draw.text(

            (
                x
                + NODE_WIDTH
                - state_width
                - 16,
                resource_y + 9
            ),

            state_text,

            font=SMALL_FONT,

            fill=state_color
        )


        resource_y += (

            NODE_RESOURCE_HEIGHT
            + NODE_RESOURCE_GAP
        )


# ============================================================
# BOTTOM PANELS
# ============================================================

panel_y = (

    TOP_MARGIN
    + max_node_height
    + PANEL_GAP
)


available_width = (
    image_width
    - SIDE_MARGIN * 2
)


# Four panels

panel_width = (

    available_width
    - PANEL_GAP * 3
) / 4


# ============================================================
# PANEL DRAWING FUNCTION
# ============================================================

def draw_panel(
    x,
    y,
    width,
    height,
    title,
    header_color
):

    draw.rounded_rectangle(

        (
            x,
            y,
            x + width,
            y + height
        ),

        radius=7,

        outline=header_color,

        width=2,

        fill=WHITE
    )


    draw.rounded_rectangle(

        (
            x,
            y,
            x + width,
            y + PANEL_HEADER_HEIGHT
        ),

        radius=7,

        fill=header_color
    )


    draw.rectangle(

        (
            x,
            y + PANEL_HEADER_HEIGHT - 8,
            x + width,
            y + PANEL_HEADER_HEIGHT
        ),

        fill=header_color
    )


    draw.text(

        (
            x + 12,
            y + 10
        ),

        title,

        font=PANEL_FONT,

        fill=WHITE
    )


# ============================================================
# PANEL 1 - CLUSTER SUMMARY
# ============================================================

x1 = SIDE_MARGIN

draw_panel(

    x1,
    panel_y,
    panel_width,
    bottom_panel_height,
    "CLUSTER SUMMARY",
    BLUE
)


summary_x = x1 + PANEL_PADDING

summary_y = (
    panel_y
    + PANEL_HEADER_HEIGHT
    + 15
)


summary_lines = [

    (
        "Cluster Name",
        cluster_name
    ),

    (
        "Nodes",
        "{}/{}/{}/{}".format(
            len(nodes),
            online_nodes,
            standby_nodes,
            offline_nodes
        )
    ),

    (
        "Resource Groups",
        "{}/{}/{}".format(
            running_groups,
            degraded_groups,
            stopped_groups
        )
    ),

    (
        "Resources",
        "{}/{}/{}/{}".format(
            running_count,
            stopped_count,
            failed_count,
            unmanaged_count
        )
    ),

    (
        "Order Constraints",
        str(
            constraint_counts[
                "order"
            ]
        )
    ),

    (
        "Colocation",
        str(
            constraint_counts[
                "colocation"
            ]
        )
    ),

    (
        "Anti-colocation",
        str(
            constraint_counts[
                "anti_colocation"
            ]
        )
    ),

    (
        "Location",
        str(
            constraint_counts[
                "location"
            ]
        )
    ),

    (
        "Quorum",
        "Present"
        if quorum_present
        else "NOT PRESENT"
    )
]


for label, value in summary_lines:

    draw.text(

        (
            summary_x,
            summary_y
        ),

        label,

        font=PANEL_TEXT_FONT,

        fill=DARK_GRAY
    )


    value_width, _ = text_size(

        draw,

        value,

        PANEL_TEXT_BOLD
    )


    draw.text(

        (
            x1
            + panel_width
            - PANEL_PADDING
            - value_width,
            summary_y
        ),

        value,

        font=PANEL_TEXT_BOLD,

        fill=BLACK
    )


    summary_y += 30


# ============================================================
# PANEL 2 - RESOURCE DISTRIBUTION
# ============================================================

x2 = (

    x1
    + panel_width
    + PANEL_GAP
)


draw_panel(

    x2,
    panel_y,
    panel_width,
    bottom_panel_height,
    "RESOURCE DISTRIBUTION",
    GREEN
)


table_x = x2 + PANEL_PADDING

table_y = (
    panel_y
    + PANEL_HEADER_HEIGHT
    + 12
)


# Table columns

col_node = 0

col_resources = (
    panel_width * 0.68
)

col_groups = (
    panel_width * 0.86
)


draw.text(

    (
        table_x + col_node,
        table_y
    ),

    "Node",

    font=PANEL_TEXT_BOLD,

    fill=DARK_BLUE
)


draw.text(

    (
        table_x + col_resources,
        table_y
    ),

    "Resources",

    font=PANEL_TEXT_BOLD,

    fill=DARK_BLUE
)


draw.text(

    (
        table_x + col_groups,
        table_y
    ),

    "Groups",

    font=PANEL_TEXT_BOLD,

    fill=DARK_BLUE
)


table_y += 28


for node_name in node_names:

    node = nodes[node_name]

    group_count = 0

    groups_on_node = set()

    for resource_id in node[
        "resources"
    ]:

        group_id = resource_to_group.get(
            resource_id
        )

        if group_id:

            groups_on_node.add(
                group_id
            )

    group_count = len(
        groups_on_node
    )


    display_node = shorten(
        node_name,
        28
    )


    draw.text(

        (
            table_x + col_node,
            table_y
        ),

        display_node,

        font=SMALL_FONT,

        fill=DARK_GRAY
    )


    draw.text(

        (
            table_x + col_resources,
            table_y
        ),

        str(
            len(
                node["resources"]
            )
        ),

        font=PANEL_TEXT_FONT,

        fill=BLACK
    )


    draw.text(

        (
            table_x + col_groups,
            table_y
        ),

        str(
            group_count
        ),

        font=PANEL_TEXT_FONT,

        fill=BLACK
    )


    table_y += 28


# Total row

draw.line(

    (
        table_x,
        table_y - 7,
        table_x + panel_width - 24,
        table_y - 7
    ),

    fill=BORDER,

    width=1
)


draw.text(

    (
        table_x,
        table_y
    ),

    "TOTAL",

    font=PANEL_TEXT_BOLD,

    fill=DARK_BLUE
)


draw.text(

    (
        table_x + col_resources,
        table_y
    ),

    str(
        len(resources)
    ),

    font=PANEL_TEXT_BOLD,

    fill=BLACK
)


draw.text(

    (
        table_x + col_groups,
        table_y
    ),

    str(
        len(groups)
    ),

    font=PANEL_TEXT_BOLD,

    fill=BLACK
)


# ============================================================
# PANEL 3 - CONSTRAINTS + CLNVRM SERVICES
# ============================================================

x3 = (

    x2
    + panel_width
    + PANEL_GAP
)


draw_panel(

    x3,
    panel_y,
    panel_width,
    bottom_panel_height,
    "CONSTRAINTS & SERVICES",
    PURPLE
)


constraint_y = (

    panel_y
    + PANEL_HEADER_HEIGHT
    + 14
)


constraint_lines = [

    (
        "Order",
        constraint_counts[
            "order"
        ]
    ),

    (
        "Colocation",
        constraint_counts[
            "colocation"
        ]
    ),

    (
        "Anti-colocation",
        constraint_counts[
            "anti_colocation"
        ]
    ),

    (
        "Location",
        constraint_counts[
            "location"
        ]
    )
]


for label, count in constraint_lines:

    draw.text(

        (
            x3 + PANEL_PADDING,
            constraint_y
        ),

        label,

        font=PANEL_TEXT_FONT,

        fill=DARK_GRAY
    )


    count_text = str(count)

    count_width, _ = text_size(

        draw,

        count_text,

        PANEL_TEXT_BOLD
    )


    draw.text(

        (
            x3
            + panel_width
            - PANEL_PADDING
            - count_width,
            constraint_y
        ),

        count_text,

        font=PANEL_TEXT_BOLD,

        fill=BLACK
    )


    constraint_y += 25


# ------------------------------------------------------------
# CLNVRM services
# ------------------------------------------------------------

constraint_y += 8


draw.line(

    (
        x3 + PANEL_PADDING,
        constraint_y,
        x3 + panel_width - PANEL_PADDING,
        constraint_y
    ),

    fill=BORDER,

    width=1
)


constraint_y += 12


draw.text(

    (
        x3 + PANEL_PADDING,
        constraint_y
    ),

    "CLNVRM SERVICES",

    font=PANEL_TEXT_BOLD,

    fill=PURPLE
)


constraint_y += 25


draw.text(

    (
        x3 + PANEL_PADDING,
        constraint_y
    ),

    "Instances",

    font=PANEL_TEXT_FONT,

    fill=DARK_GRAY
)


draw.text(

    (
        x3
        + panel_width
        - PANEL_PADDING
        - 60,
        constraint_y
    ),

    str(
        len(
            clnvrm_instances
        )
    ),

    font=PANEL_TEXT_BOLD,

    fill=BLACK
)


constraint_y += 25


# Calculate average / common resource count

if clnvrm_instances:

    instance_counts = [

        len(data["resources"])

        for data in
        clnvrm_instances.values()
    ]

    if instance_counts:

        resource_per_instance = (
            min(instance_counts)
            if len(
                set(instance_counts)
            ) == 1
            else "varies"
        )

    else:

        resource_per_instance = 0

else:

    resource_per_instance = 0


draw.text(

    (
        x3 + PANEL_PADDING,
        constraint_y
    ),

    "Resources / instance",

    font=PANEL_TEXT_FONT,

    fill=DARK_GRAY
)


draw.text(

    (
        x3
        + panel_width
        - PANEL_PADDING
        - 60,
        constraint_y
    ),

    str(
        resource_per_instance
    ),

    font=PANEL_TEXT_BOLD,

    fill=BLACK
)


constraint_y += 25


# Anti-colocation status

anti_count = constraint_counts[
    "anti_colocation"
]


draw.text(

    (
        x3 + PANEL_PADDING,
        constraint_y
    ),

    "VIP anti-colocation",

    font=PANEL_TEXT_FONT,

    fill=DARK_GRAY
)


if anti_count > 0:

    anti_text = (
        "Configured ("
        + str(anti_count)
        + ")"
    )

    anti_color = GREEN

else:

    anti_text = "NOT CONFIGURED"

    anti_color = RED


draw.text(

    (
        x3
        + panel_width
        - PANEL_PADDING
        - 105,
        constraint_y
    ),

    anti_text,

    font=SMALL_FONT,

    fill=anti_color
)


# ============================================================
# PANEL 4 - CLUSTER HEALTH
# ============================================================

x4 = (

    x3
    + panel_width
    + PANEL_GAP
)


draw_panel(

    x4,
    panel_y,
    panel_width,
    bottom_panel_height,
    "CLUSTER HEALTH STATUS",
    GREEN
    if cluster_healthy
    else RED
)


health_y = (

    panel_y
    + PANEL_HEADER_HEIGHT
    + 16
)


if cluster_healthy:

    draw.text(

        (
            x4 + PANEL_PADDING,
            health_y
        ),

        "✓  All systems are running normally.",

        font=PANEL_TEXT_BOLD,

        fill=DARK_GREEN
    )

else:

    draw.text(

        (
            x4 + PANEL_PADDING,
            health_y
        ),

        "!  Problems detected.",

        font=PANEL_TEXT_BOLD,

        fill=RED
    )


health_y += 38


# Health checks

health_checks = [

    (
        online_nodes == len(nodes),
        "{} nodes online".format(
            online_nodes
        )
    ),

    (
        standby_nodes == 0,
        "{} nodes in standby".format(
            standby_nodes
        )
    ),

    (
        offline_nodes == 0,
        "{} nodes offline".format(
            offline_nodes
        )
    ),

    (
        maintenance_nodes == 0,
        "{} nodes in maintenance".format(
            maintenance_nodes
        )
    ),

    (
        running_groups == len(groups),
        "{} resource groups running".format(
            running_groups
        )
    ),

    (
        degraded_groups == 0,
        "{} degraded groups".format(
            degraded_groups
        )
    ),

    (
        failed_count == 0,
        "{} failed resources".format(
            failed_count
        )
    ),

    (
        stopped_count == 0,
        "{} stopped resources".format(
            stopped_count
        )
    ),

    (
        unmanaged_count == 0,
        "{} unmanaged resources".format(
            unmanaged_count
        )
    ),

    (
        quorum_present,
        "Quorum is present"
        if quorum_present
        else "QUORUM NOT PRESENT"
    ),

    (
        constraint_counts[
            "anti_colocation"
        ] > 0,
        "VIP anti-colocation configured"
        if constraint_counts[
            "anti_colocation"
        ] > 0
        else "VIP anti-colocation missing"
    )
]


for check_ok, text in health_checks:

    if check_ok:

        symbol = "✓"

        color = GREEN

    else:

        symbol = "!"

        color = RED


    draw.ellipse(

        (
            x4 + PANEL_PADDING,
            health_y + 1,
            x4 + PANEL_PADDING + 17,
            health_y + 18
        ),

        fill=color
    )


    centered_text(

        draw,

        x4 + PANEL_PADDING + 8,

        health_y + 9,

        symbol,

        SMALL_FONT,

        WHITE
    )


    draw.text(

        (
            x4
            + PANEL_PADDING
            + 26,
            health_y
        ),

        text,

        font=SMALL_FONT,

        fill=DARK_GRAY
        if check_ok
        else RED
    )


    health_y += 25


# ============================================================
# LEGEND
# ============================================================

legend_y = (
    image_height
    - 34
)


legend_items = [

    (
        "Running / Online",
        GREEN
    ),

    (
        "Stopped / Standby",
        ORANGE
    ),

    (
        "Failed / Offline",
        RED
    ),

    (
        "Unmanaged",
        GRAY
    ),

    (
        "Resource Group",
        PURPLE
    )
]


legend_x = SIDE_MARGIN


draw.text(

    (
        legend_x,
        legend_y - 7
    ),

    "Legend:",

    font=LEGEND_FONT,

    fill=DARK_BLUE
)


legend_x += 55


for label, color in legend_items:

    draw.ellipse(

        (
            legend_x,
            legend_y - 7,
            legend_x + 15,
            legend_y + 8
        ),

        fill=color
    )


    draw.text(

        (
            legend_x + 22,
            legend_y - 7
        ),

        label,

        font=LEGEND_FONT,

        fill=DARK_GRAY
    )


    label_width, _ = text_size(

        draw,

        label,

        LEGEND_FONT
    )


    legend_x += (
        30
        + label_width
    )


# ============================================================
# SAVE PNG
# ============================================================

timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
)


output_file = (

    OUTPUT_DIR

    / (
        safe_name(cluster_name)
        + "_resource_map_"
        + timestamp
        + ".png"
    )
)


image.save(
    output_file,
    "PNG"
)


# ============================================================
# CONSOLE SUMMARY
# ============================================================

print()
print("=" * 80)
print("CLUSTER SUMMARY")
print("=" * 80)
print()

print(
    "Cluster              : "
    + cluster_name
)

print(
    "Nodes                : "
    + str(len(nodes))
)

print(
    "  Online             : "
    + str(online_nodes)
)

print(
    "  Standby            : "
    + str(standby_nodes)
)

print(
    "  Offline            : "
    + str(offline_nodes)
)

print(
    "  Maintenance        : "
    + str(maintenance_nodes)
)

print()

print(
    "Resource groups      : "
    + str(len(groups))
)

print(
    "  Running            : "
    + str(running_groups)
)

print(
    "  Degraded           : "
    + str(degraded_groups)
)

print(
    "  Not running        : "
    + str(stopped_groups)
)

print()

print(
    "Resources            : "
    + str(len(resources))
)

print(
    "  Running            : "
    + str(running_count)
)

print(
    "  Stopped            : "
    + str(stopped_count)
)

print(
    "  Failed             : "
    + str(failed_count)
)

print(
    "  Unmanaged          : "
    + str(unmanaged_count)
)

print()

print(
    "Constraints:"
)

print(
    "  Order              : "
    + str(
        constraint_counts["order"]
    )
)

print(
    "  Colocation         : "
    + str(
        constraint_counts["colocation"]
    )
)

print(
    "  Anti-colocation    : "
    + str(
        constraint_counts["anti_colocation"]
    )
)

print(
    "  Location           : "
    + str(
        constraint_counts["location"]
    )
)

print()

print(
    "Quorum               : "
    + (
        "PRESENT"
        if quorum_present
        else "NOT PRESENT"
    )
)

print()

print(
    "Overall health       : "
    + (
        "HEALTHY"
        if cluster_healthy
        else "ATTENTION REQUIRED"
    )
)

print()

print(
    "PNG:"
)

print(
    str(output_file)
)

print()

print("=" * 80)