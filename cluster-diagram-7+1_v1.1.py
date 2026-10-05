#!/usr/bin/env python3

import os

import sys

import subprocess

import tempfile

import shutil

import re

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

CLUSTER_IP = "clnvrm001.mak.iss"

ssh_user = "root"

# Put your SSH password here.

# This is intentionally not copied from the previous script.

ssh_password = os.environ.get("Th@les01")
if not ssh_password:
    import getpass
    ssh_password = getpass.getpass("SSH password: ")

ssh_port = 22

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

# Space reserved immediately above each resource group for its label.
# Keeping this outside the group boundary prevents the label from
# obscuring either the preceding resource or a group member.
GROUP_LABEL_HEIGHT = 28

PANEL_GAP = 12

PANEL_HEADER_HEIGHT = 38

PANEL_PADDING = 12

FONT_TITLE = 30

FONT_SUBTITLE = 15

FONT_NODE = 17

FONT_NODE_STATUS = 15

FONT_COUNT = 13

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

GREEN = "#1B8E3E"

LIGHT_GREEN = "#E7F5E9"

DARK_GREEN = "#0B6B2D"

ORANGE = "#E68A00"

LIGHT_ORANGE = "#FFF1D6"

RED = "#C40000"

LIGHT_RED = "#FCE7E7"

PURPLE = "#7026A0"

GRAY = "#777777"

DARK_GRAY = "#444444"

LIGHT_GRAY = "#F2F3F5"

BORDER = "#AAB2BD"



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

            return ImageFont.truetype(path, size)

    return ImageFont.load_default()



TITLE_FONT = get_font(FONT_TITLE, True)

SUBTITLE_FONT = get_font(FONT_SUBTITLE, False)

NODE_FONT = get_font(FONT_NODE, True)

NODE_STATUS_FONT = get_font(FONT_NODE_STATUS, True)

COUNT_FONT = get_font(FONT_COUNT, False)

RESOURCE_FONT = get_font(FONT_RESOURCE, False)

PANEL_FONT = get_font(FONT_PANEL, True)

PANEL_TEXT_FONT = get_font(FONT_PANEL_TEXT, False)

PANEL_TEXT_BOLD = get_font(FONT_PANEL_TEXT, True)

SMALL_FONT = get_font(FONT_SMALL, False)

SMALL_BOLD = get_font(FONT_SMALL, True)

LEGEND_FONT = get_font(FONT_LEGEND, False)

# ============================================================
# CONSTRAINT DIAGRAM CONFIGURATION
# ============================================================
CONSTRAINT_GREEN = "#0B6B2D"
CONSTRAINT_BLUE = "#1555A5"
CONSTRAINT_ARROW_WIDTH = 3



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

    bbox = draw.textbbox((0, 0), text, font=font)

    return (

        bbox[2] - bbox[0],

        bbox[3] - bbox[1]

    )



def centered_text(draw, x, y, text, font, fill):

    width, height = text_size(draw, text, font)

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



def bool_from_string(value):

    return str(value).lower() in (

        "true",

        "yes",

        "on",

        "1"

    )



def int_or_none(value):

    try:

        return int(str(value))

    except Exception:

        return None



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

    with open(

        askpass_file,

        "w"

    ) as f:

        f.write("@echo off\n")

        f.write("echo " + password + "\n")

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

        environment["SSH_ASKPASS"] = askpass_file

        environment["SSH_ASKPASS_REQUIRE"] = "force"

        environment["DISPLAY"] = "none:0"

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

            ssh_user + "@" + CLUSTER_IP,

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

            print("Command:")

            print(command)

            print()

            print("SSH error:")

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

# CONNECTIVITY

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

    print("ERROR: SSH connection test failed.")

    sys.exit(1)

print("SSH connection successful.")



# ============================================================

# GET PACEMAKER DATA

# ============================================================

print("Getting Pacemaker XML...")

crm_xml = ssh_command(

    "crm_mon -1 -X"

)

print("Getting Pacemaker CIB...")

cib_xml = ssh_command(

    "cibadmin -Q"

)

print("Getting pcs status...")

pcs_status = ssh_command(

    "pcs status --full"

)



# ============================================================

# PARSE XML

# ============================================================

try:

    crm_root = ET.fromstring(crm_xml)

except Exception as e:

    print()

    print("ERROR parsing crm_mon XML:")

    print(str(e))

    sys.exit(1)

try:

    cib_root = ET.fromstring(cib_xml)

except Exception as e:

    print()

    print("ERROR parsing CIB XML:")

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

for node in crm_root.findall(".//nodes/node"):

    node_name = (

        node.get("uname")

        or node.get("name")

        or node.get("id")

    )

    if not node_name:

        continue

    online = bool_from_string(

        node.get("online", "false")

    )

    standby = bool_from_string(

        node.get("standby", "false")

    )

    maintenance = bool_from_string(

        node.get("maintenance", "false")

    )

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

    role="Stopped"

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

            "admin_disabled": False

        }

    else:

        resource = resources[resource_id]

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

    active = bool_from_string(

        elem.get("active", "false")

    )

    failed = bool_from_string(

        elem.get("failed", "false")

    )

    managed = not (

        elem.get("managed", "true").lower()

        == "false"

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

# RESOURCE GROUPS

# ============================================================

groups = {}

resources_section = None

for elem in cib_root.iter():

    if elem.tag == "resources":

        resources_section = elem

        break



if resources_section is not None:

    for group in resources_section.findall("group"):

        group_id = group.get("id")

        if not group_id:

            continue

        members = []

        for primitive in group.findall("primitive"):

            resource_id = primitive.get("id")

            if resource_id:

                members.append(resource_id)

        groups[group_id] = {

            "id": group_id,

            "members": members,

            "admin_disabled": False

        }



# ============================================================

# RESOURCE / GROUP META OPTIONS

# ============================================================

# This reads target-role=Stopped from the CIB.

#

# A disabled group is treated as an administrative state.

# Its member resources are therefore also considered

# administratively stopped for health purposes.

admin_disabled_resources = set()

admin_disabled_groups = set()



def element_has_target_role_stopped(element):

    for child in element.iter():

        if child.tag != "nvpair":

            continue

        if child.get("name") != "target-role":

            continue

        if str(

            child.get("value", "")

        ).lower() == "stopped":

            return True

    return False



# Check groups.

if resources_section is not None:

    for group in resources_section.findall("group"):

        group_id = group.get("id")

        if not group_id:

            continue

        if element_has_target_role_stopped(group):

            admin_disabled_groups.add(group_id)

            if group_id in groups:

                groups[group_id]["admin_disabled"] = True

            for primitive in group.findall("primitive"):

                resource_id = primitive.get("id")

                if resource_id:

                    admin_disabled_resources.add(

                        resource_id

                    )



# Check individual primitives.

if resources_section is not None:

    for primitive in resources_section.iter("primitive"):

        resource_id = primitive.get("id")

        if not resource_id:

            continue

        if element_has_target_role_stopped(

            primitive

        ):

            admin_disabled_resources.add(

                resource_id

            )



for resource_id in admin_disabled_resources:

    if resource_id in resources:

        resources[resource_id][

            "admin_disabled"

        ] = True



# ============================================================

# RESOURCE -> GROUP

# ============================================================

resource_to_group = {}

for group_id, group in groups.items():

    for resource_id in group["members"]:

        resource_to_group[resource_id] = group_id



# ============================================================

# FAILED RESOURCE ACTIONS

# ============================================================

# crm_mon XML is useful for current resource state, but

# failed actions shown by "pcs status" are not reliably exposed

# as current resource failed=true attributes.

#

# Therefore the script explicitly reads "pcs status --full"

# and parses its "Failed Resource Actions" section.

failed_actions = []

in_failed_section = False

resource_ids_sorted = sorted(

    resources.keys(),

    key=len,

    reverse=True

)

for raw_line in pcs_status.splitlines():

    line = raw_line.strip()

    if line.lower() == "failed resource actions:":

        in_failed_section = True

        continue

    if not in_failed_section:

        continue

    if line.startswith("Daemon Status:"):

        break

    if not line:

        continue

    if not line.startswith("*"):

        continue

    # Example:

    #

    # * clnvrm024-nfsdat01_monitor_60000 on

    #   tvsnvrapp017mp.mak.iss 'not running' (7):

    #

    # Because whitespace can vary, use the complete logical

    # line after removing formatting.

    action_text = line[1:].strip()

    parts = action_text.split()

    if not parts:

        continue

    action_id = parts[0]

    resource_id = None

    for candidate in resource_ids_sorted:

        if action_id.startswith(

            candidate + "_"

        ):

            resource_id = candidate

            break

    node_name = ""

    if "on" in parts:

        try:

            on_index = parts.index("on")

            if on_index + 1 < len(parts):

                node_name = parts[

                    on_index + 1

                ]

        except Exception:

            pass

    result_text = ""

    match = re.search(

        r"'([^']*)'\s+\((-?\d+)\)",

        action_text

    )

    if match:

        result_text = (

            match.group(1)

            + " ("

            + match.group(2)

            + ")"

        )

    failed_actions.append({

        "action": action_id,

        "resource": resource_id

        if resource_id

        else action_id,

        "node": node_name,

        "result": result_text

    })



failed_action_resources = set()

for action in failed_actions:

    if action["resource"] in resources:

        failed_action_resources.add(

            action["resource"]

        )



# ============================================================

# CURRENT RESOURCE FAILURES

# ============================================================

current_failed_resources = set()

for resource_id, resource in resources.items():

    if resource["failed"]:

        current_failed_resources.add(

            resource_id

        )



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

    "anti_colocation": 0,

    "vip_anti_colocation": 0,

    "vip_workload_colocation": 0,

    "core_to_nfsrec_order": 0,

    "nfsrec_to_picata_order": 0,

    "etc_to_updater_order": 0

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

            constraint_counts["order"] += 1

            first = constraint.get("first", "").lower()

            then = constraint.get("then", "").lower()

            if (
                first.startswith("rg-clnvrm")

                and first.endswith("-core")

                and then.startswith("clnvrm")

                and "-nfsrec" in then

            ):

                constraint_counts["core_to_nfsrec_order"] += 1

            elif (
                first.startswith("clnvrm")

                and "-nfsrec" in first

                and then.startswith("clnvrm")

                and "-picata" in then

            ):

                constraint_counts["nfsrec_to_picata_order"] += 1

            elif (
                first.startswith("clnvrm")

                and first.endswith("-nfsetc01")

                and then.startswith("clnvrm")

                and then.endswith("-pctcfg-updater")

            ):

                constraint_counts["etc_to_updater_order"] += 1

        elif tag == "rsc_colocation":

            constraint_counts["colocation"] += 1

            score = constraint.get(

                "score",

                ""

            ).upper()

            rsc = constraint.get("rsc", "").lower()

            with_rsc = constraint.get("with-rsc", "").lower()

            is_anti = (

                score == "-INFINITY"

                or score.startswith("-INFINITY")

            )

            if is_anti:

                constraint_counts["anti_colocation"] += 1

                if (

                    rsc.startswith("clnvrm")

                    and rsc.endswith("-vip")

                    and with_rsc.startswith("clnvrm")

                    and with_rsc.endswith("-vip")

                ):

                    constraint_counts[

                        "vip_anti_colocation"

                    ] += 1

            else:

                if (

                    rsc.startswith(("clnvrm", "rg-clnvrm"))

                    and with_rsc.startswith("clnvrm")

                    and with_rsc.endswith("-vip")

                ):

                    constraint_counts[

                        "vip_workload_colocation"

                    ] += 1

        elif tag == "rsc_location":

            constraint_counts["location"] += 1

        elif tag == "rsc_ticket":

            constraint_counts["ticket"] += 1



# ============================================================

# QUORUM

# ============================================================

quorum_present = True

pcs_status_lower = pcs_status.lower()

if "without quorum" in pcs_status_lower:

    quorum_present = False

elif "partition with quorum" in pcs_status_lower:

    quorum_present = True

else:

    crm_text_lower = crm_xml.lower()

    if "without quorum" in crm_text_lower:

        quorum_present = False

    elif "partition with quorum" in crm_text_lower:

        quorum_present = True



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

            stopped.append(resource_id)

            continue

        if not resource["managed"]:

            unmanaged.append(resource_id)

        if resource_id in current_failed_resources:

            failed.append(resource_id)

        if (

            resource["active"]

            and resource["node"]

        ):

            running.append(resource_id)

        else:

            stopped.append(resource_id)

    if group["admin_disabled"]:

        state = "DISABLED"

    elif len(running) == 0:

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

administratively_stopped_count = 0

unexpected_stopped_count = 0



for resource_id, resource in resources.items():

    if resource["active"]:

        running_count += 1

    else:

        stopped_count += 1

        if resource["admin_disabled"]:

            administratively_stopped_count += 1

        else:

            unexpected_stopped_count += 1

    if resource_id in current_failed_resources:

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

disabled_groups = 0



for state in group_states.values():

    if state["state"] == "RUNNING":

        running_groups += 1

    elif state["state"] == "DEGRADED":

        degraded_groups += 1

    elif state["state"] == "DISABLED":

        disabled_groups += 1

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

    if resource_lower.startswith("clnvrm"):

        parts = resource_lower.split("-")

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

# NODE HEIGHT

# ============================================================

def node_height(node):

    resource_count = len(

        node["resources"]

    )

    group_count = len({

        resource_to_group[resource_id]

        for resource_id in node["resources"]

        if resource_id in resource_to_group

    })

    return (

        NODE_HEADER_HEIGHT

        + 20

        + resource_count

        * (

            NODE_RESOURCE_HEIGHT

            + NODE_RESOURCE_GAP

        )

        + group_count * GROUP_LABEL_HEIGHT

        + 20

    )



node_heights = {}

for node_name, node in nodes.items():

    node_heights[node_name] = node_height(

        node

    )



max_node_height = max(

    node_heights.values(),

    default=300

)



# ============================================================

# UNASSIGNED / STOPPED RESOURCE STRIP

# ============================================================

unassigned_resources = []

for resource_id, resource in resources.items():

    if not resource["node"]:

        unassigned_resources.append(

            resource_id

        )



unassigned_resources.sort()

UNASSIGNED_STRIP_HEIGHT = 0

if unassigned_resources:

    UNASSIGNED_STRIP_HEIGHT = 125



# ============================================================

# DASHBOARD DIMENSIONS

# ============================================================

bottom_panel_height = 370

node_names = sorted(

    nodes.keys()

)

node_count = max(

    len(node_names),

    1

)

image_width = (

    SIDE_MARGIN * 2

    + node_count * NODE_WIDTH

    + (node_count - 1) * NODE_GAP

)

image_height = (

    TOP_MARGIN

    + max_node_height

    + UNASSIGNED_STRIP_HEIGHT

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

draw = ImageDraw.Draw(image)



# ============================================================

# HEALTH LOGIC

# ============================================================

# IMPORTANT:

#

# Administratively disabled resources are NOT considered

# cluster failures.

#

# Failed resource actions ARE considered an attention

# condition, even if the resource is currently running.

#

# A resource that is stopped without target-role=Stopped is

# considered an unexpected stopped resource.

cluster_healthy = (

    online_nodes == len(nodes)

    and standby_nodes == 0

    and offline_nodes == 0

    and maintenance_nodes == 0

    and degraded_groups == 0

    and stopped_groups == 0

    and unexpected_stopped_count == 0

    and failed_count == 0

    and len(failed_actions) == 0

    and unmanaged_count == 0

    and quorum_present

    and constraint_counts["anti_colocation"] > 0

)



if cluster_healthy:

    health_text = "CLUSTER HEALTH: HEALTHY"

    health_subtext = (

        "All active cluster conditions are normal"

    )

    health_color = GREEN

    health_fill = LIGHT_GREEN

else:

    health_text = "CLUSTER HEALTH: ATTENTION"

    health_subtext = (

        "One or more cluster conditions require review"

    )

    health_color = RED

    health_fill = LIGHT_RED



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

# HEALTH BADGE

# ============================================================

badge_width = 360

badge_height = 62

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

        badge_y1 + 13,

        badge_x1 + 43,

        badge_y1 + 44

    ),

    fill=health_color

)



centered_text(

    draw,

    badge_x1 + 27.5,

    badge_y1 + 28.5,

    "✓" if cluster_healthy else "!",

    PANEL_TEXT_BOLD,

    WHITE

)



draw.text(

    (

        badge_x1 + 53,

        badge_y1 + 10

    ),

    health_text,

    font=PANEL_TEXT_BOLD,

    fill=health_color

)



draw.text(

    (

        badge_x1 + 53,

        badge_y1 + 34

    ),

    health_subtext,

    font=SMALL_FONT,

    fill=DARK_GREEN if cluster_healthy else RED

)



# ============================================================

# NODE DRAWING

# ============================================================

resource_boxes = {}
node_boxes = {}
group_boxes = {}

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

    # NODE STATUS

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

    # NODE BOX

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

    node_boxes[node_name] = {
        "x1": x,
        "y1": node_y,
        "x2": x + NODE_WIDTH,
        "y2": node_y + max_node_height,
        "cx": x + NODE_WIDTH / 2
    }


    # --------------------------------------------------------

    # HEADER

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

            node_y + NODE_HEADER_HEIGHT - 10,

            x + NODE_WIDTH,

            node_y + NODE_HEADER_HEIGHT

        ),

        fill=header_color

    )

    centered_text(

        draw,

        x + NODE_WIDTH // 2,

        node_y + 25,

        shorten(node_name, 29),

        NODE_FONT,

        WHITE

    )

    centered_text(

        draw,

        x + NODE_WIDTH // 2,

        node_y + 58,

        status,

        NODE_STATUS_FONT,

        WHITE

    )

    centered_text(

        draw,

        x + NODE_WIDTH // 2,

        node_y + 84,

        "Resources: "

        + str(len(node["resources"])),

        COUNT_FONT,

        WHITE

    )

    # --------------------------------------------------------

    # RESOURCES

    # --------------------------------------------------------

    resource_y = (

        node_y

        + NODE_HEADER_HEIGHT

        + 12

    )

    def resource_sort_key(resource_id):
        rid = resource_id.lower()

        if rid.endswith("-vip"):
            return (0, rid)
        if rid.endswith("-nfsapp01"):
            return (10, rid)
        if rid.endswith("-nfslog01"):
            return (11, rid)
        if rid.endswith("-nfsdat01"):
            return (12, rid)
        if rid.endswith("-nfsetc01"):
            return (13, rid)

        match = re.search(r"-nfsrec(\d+)$", rid)
        if match:
            return (20, int(match.group(1)))

        return (50, rid)

    drawn_groups = set()

    for resource_id in sorted(
        node["resources"],
        key=resource_sort_key
    ):

        resource = resources.get(

            resource_id

        )

        if resource is None:

            continue

        group_id = resource_to_group.get(resource_id)

        if group_id and group_id not in drawn_groups:

            resource_y += GROUP_LABEL_HEIGHT

            drawn_groups.add(group_id)

        # State priority:

        # 1. Current failure

        # 2. Failed action history

        # 3. Unmanaged

        # 4. Administrative stopped

        # 5. Ordinary stopped

        # 6. Running

        if resource_id in current_failed_resources:

            resource_fill = LIGHT_RED

            resource_outline = RED

            state_text = "FAILED"

            state_color = RED

        elif resource_id in failed_action_resources:

            resource_fill = LIGHT_RED

            resource_outline = RED

            state_text = "ACTION FAIL"

            state_color = RED

        elif not resource["managed"]:

            resource_fill = LIGHT_GRAY

            resource_outline = GRAY

            state_text = "UNMANAGED"

            state_color = GRAY

        elif not resource["active"] and resource[

            "admin_disabled"

        ]:

            resource_fill = LIGHT_ORANGE

            resource_outline = ORANGE

            state_text = "DISABLED"

            state_color = ORANGE

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
        resource_boxes[resource_id] = {
            "x1": x + 8,
            "y1": resource_y,
            "x2": x + NODE_WIDTH - 8,
            "y2": resource_y + NODE_RESOURCE_HEIGHT,
            "cx": x + NODE_WIDTH / 2,
            "cy": resource_y + NODE_RESOURCE_HEIGHT / 2
        }


        display_name = shorten(

            resource_id,

            25

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


# ============================================================
# CONSTRAINT ARCHITECTURE DIAGRAM
# ============================================================
# Geometry used by the constraint annotations.
node_bottom = TOP_MARGIN + max_node_height
# Visualizes the validated model:
#
#   VIP <-> workload resources  colocation INFINITY
#   CORE -> NFSREC01-04         mandatory start order
#   NFSREC01-04 -> PICATA01-04  mandatory start order
#   NFSETC01 -> updater          mandatory start order
#   VIP <-> VIP                 anti-colocation -INFINITY
#
# The 21 pairwise VIP anti-colocation constraints are summarized in
# the dashboard rather than drawn between nodes; drawing them would
# obscure the resources without adding useful information.

def draw_arrowhead(draw_obj, x, y, angle, color, size=8):
    import math
    left = angle + math.pi * 0.82
    right = angle - math.pi * 0.82
    draw_obj.polygon(
        [
            (x, y),
            (x + size * math.cos(left), y + size * math.sin(left)),
            (x + size * math.cos(right), y + size * math.sin(right))
        ],
        fill=color
    )


def draw_dashed_polyline(draw_obj, points, fill, width=2, dash=8, gap=5):
    import math
    for p1, p2 in zip(points[:-1], points[1:]):
        x1, y1 = p1
        x2, y2 = p2
        dx = x2 - x1
        dy = y2 - y1
        length = math.hypot(dx, dy)
        if length == 0:
            continue

        ux = dx / length
        uy = dy / length
        pos = 0.0

        while pos < length:
            end = min(pos + dash, length)
            draw_obj.line(
                (
                    x1 + ux * pos,
                    y1 + uy * pos,
                    x1 + ux * end,
                    y1 + uy * end
                ),
                fill=fill,
                width=width
            )
            pos += dash + gap


# ------------------------------------------------------------
# Core group outlines
# ------------------------------------------------------------
for group_id, group in groups.items():
    member_boxes = [
        resource_boxes[rid]
        for rid in group["members"]
        if rid in resource_boxes
    ]
    if not member_boxes:
        continue

    x1 = min(b["x1"] for b in member_boxes) - 7
    # The boundary encloses only the group's actual members.  The
    # label is drawn in the dedicated whitespace above this boundary.
    y1 = min(b["y1"] for b in member_boxes) - 7
    x2 = max(b["x2"] for b in member_boxes) + 7
    y2 = max(b["y2"] for b in member_boxes) + 7

    group_boxes[group_id] = {
        "x1": x1,
        "y1": y1,
        "x2": x2,
        "y2": y2,
        "cx": (x1 + x2) / 2,
        "cy": (y1 + y2) / 2
    }

    draw.rounded_rectangle(
        (x1, y1, x2, y2),
        radius=8,
        outline=BLUE,
        width=2
    )

    label = group_id
    label_w, label_h = text_size(
        draw, label, PANEL_TEXT_BOLD
    )
    label_x = (x1 + x2 - label_w) / 2
    label_y = y1 - label_h - 3

    draw.rectangle(
        (
            label_x - 5,
            label_y - 2,
            label_x + label_w + 5,
            label_y + label_h + 2
        ),
        fill=WHITE
    )
    draw.text(
        (label_x, label_y),
        label,
        font=PANEL_TEXT_BOLD,
        fill=BLUE
    )


# ------------------------------------------------------------
# VIP <-> workload colocation
# ------------------------------------------------------------
vip_ids = sorted(
    rid for rid in resources
    if rid.lower().endswith("-vip")
)

for vip_id in vip_ids:
    instance = vip_id.rsplit("-", 1)[0]
    core_id = "rg-" + instance + "-core"

    if vip_id not in resource_boxes or core_id not in group_boxes:
        continue

    vb = resource_boxes[vip_id]
    gb = group_boxes[core_id]

    y1 = vb["y2"] + 2
    y2 = gb["y1"] - 2
    # Keep the colocation connector clear of the centered group label.
    connector_x = gb["x2"] - 14

    if y2 > y1 and constraint_counts["vip_workload_colocation"]:
        draw.line(
            (connector_x, y1, connector_x, y2),
            fill=CONSTRAINT_GREEN,
            width=CONSTRAINT_ARROW_WIDTH
        )
        draw_arrowhead(
            draw, connector_x, y2, 1.5708,
            CONSTRAINT_GREEN
        )
        draw_arrowhead(
            draw, connector_x, y1, -1.5708,
            CONSTRAINT_GREEN
        )


# ------------------------------------------------------------
# CORE -> NFSREC mandatory start order
# ------------------------------------------------------------
for group_id, gb in group_boxes.items():
    instance = group_id.replace("rg-", "").replace("-core", "")

    rec_ids = [
        rid for rid in resources
        if rid.lower().startswith(instance + "-nfsrec")
    ]

    rec_boxes = [
        resource_boxes[rid]
        for rid in rec_ids
        if rid in resource_boxes
    ]
    if not rec_boxes:
        continue

    first_y = min(b["y1"] for b in rec_boxes)
    last_y = max(b["y2"] for b in rec_boxes)

    start_y = gb["y2"] + 2
    end_y = first_y - 2

    # Mandatory start order: CORE must start before each NFSREC.
    if end_y > start_y and constraint_counts["core_to_nfsrec_order"]:
        draw.line(
            (gb["cx"], start_y, gb["cx"], end_y),
            fill=CONSTRAINT_BLUE,
            width=CONSTRAINT_ARROW_WIDTH
        )
        draw_arrowhead(
            draw, gb["cx"], end_y, 1.5708,
            CONSTRAINT_BLUE
        )

# ------------------------------------------------------------
# Constraint legend
# ------------------------------------------------------------
constraint_legend_y = node_bottom - 27
legend_items = [
    (CONSTRAINT_GREEN, "VIP ↔ workload colocated ×10 / instance", False),
    (CONSTRAINT_BLUE, "Order: CORE → NFSREC ×4", False),
    (CONSTRAINT_BLUE, "NFSREC → PICATA ×4; NFSETC → updater", False)
]

legend_x = SIDE_MARGIN + 8

for color, description, dashed in legend_items:
    if dashed:
        draw_dashed_polyline(
            draw,
            [
                (legend_x, constraint_legend_y + 8),
                (legend_x + 32, constraint_legend_y + 8)
            ],
            color,
            width=2,
            dash=6,
            gap=4
        )
    else:
        draw.line(
            (
                legend_x,
                constraint_legend_y + 8,
                legend_x + 32,
                constraint_legend_y + 8
            ),
            fill=color,
            width=3
        )

    draw.text(
        (legend_x + 40, constraint_legend_y),
        description,
        font=SMALL_FONT,
        fill=DARK_GRAY
    )

    desc_w, _ = text_size(
        draw, description, SMALL_FONT
    )
    legend_x += desc_w + 85


# Expected-vs-actual validation is intentionally not rendered in the image.


# UNASSIGNED / STOPPED RESOURCES

# ============================================================

node_bottom = (

    TOP_MARGIN

    + max_node_height

)

if unassigned_resources:

    strip_y = node_bottom + 8

    strip_x = SIDE_MARGIN

    strip_width = image_width - (

        SIDE_MARGIN * 2

    )

    draw.rounded_rectangle(

        (

            strip_x,

            strip_y,

            strip_x + strip_width,

            strip_y + UNASSIGNED_STRIP_HEIGHT - 8

        ),

        radius=7,

        outline=ORANGE,

        width=2,

        fill=LIGHT_ORANGE

    )

    draw.text(

        (

            strip_x + 12,

            strip_y + 9

        ),

        "STOPPED / NOT ASSIGNED TO A NODE",

        font=PANEL_TEXT_BOLD,

        fill=ORANGE

    )

    # Group stopped resources by CLNVRM instance.

    stopped_by_instance = defaultdict(list)

    for resource_id in unassigned_resources:

        lower_id = resource_id.lower()

        if lower_id.startswith("clnvrm"):

            instance = lower_id.split("-")[0]

        else:

            instance = "OTHER"

        stopped_by_instance[

            instance

        ].append(resource_id)

    text_x = strip_x + 12

    text_y = strip_y + 38

    line_height = 23

    for instance in sorted(

        stopped_by_instance.keys()

    ):

        resources_for_instance = (

            stopped_by_instance[instance]

        )

        instance_text = (

            instance.upper()

            + ": "

            + ", ".join(

                resources_for_instance

            )

        )

        instance_text = shorten(

            instance_text,

            175

        )

        draw.text(

            (

                text_x,

                text_y

            ),

            instance_text,

            font=SMALL_FONT,

            fill=DARK_GRAY

        )

        text_y += line_height

        if text_y > (

            strip_y

            + UNASSIGNED_STRIP_HEIGHT

            - 25

        ):

            break



# ============================================================

# BOTTOM PANELS

# ============================================================

panel_y = (

    TOP_MARGIN

    + max_node_height

    + UNASSIGNED_STRIP_HEIGHT

    + PANEL_GAP

)

available_width = (

    image_width

    - SIDE_MARGIN * 2

)

panel_width = (

    available_width

    - PANEL_GAP * 3

) / 4



# ============================================================

# PANEL FUNCTION

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

        "{}/{}/{}/{}".format(

            running_groups,

            disabled_groups,

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

        "Admin stopped",

        str(

            administratively_stopped_count

        )

    ),

    (

        "Unexpected stopped",

        str(

            unexpected_stopped_count

        )

    ),

    (

        "Failed actions",

        str(

            len(failed_actions)

        )

    ),

    (

        "Order Constraints",

        str(

            constraint_counts["order"]

        )

    ),

    (

        "Colocation",

        str(

            constraint_counts["colocation"]

        )

    ),

    (

        "Anti-colocation",

        str(

            constraint_counts["anti_colocation"]

        )

    ),

    (

        "VIP workload colocation",

        str(

            constraint_counts["vip_workload_colocation"]

        )

    ),

    (

        "VIP anti-colocation",

        str(

            constraint_counts["vip_anti_colocation"]

        )

    ),

    (

        "Location",

        str(

            constraint_counts["location"]

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

        fill=(

            RED

            if (

                label in (

                    "Unexpected stopped",

                    "Failed actions"

                )

                and value != "0"

            )

            else (

                ORANGE

                if label == "Admin stopped"

                and value != "0"

                else BLACK

            )

        )

    )

    summary_y += 25



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

col_node = 0

col_resources = panel_width * 0.68

col_groups = panel_width * 0.86

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

    groups_on_node = set()

    for resource_id in node["resources"]:

        group_id = resource_to_group.get(

            resource_id

        )

        if group_id:

            groups_on_node.add(

                group_id

            )

    draw.text(

        (

            table_x + col_node,

            table_y

        ),

        shorten(node_name, 28),

        font=SMALL_FONT,

        fill=DARK_GRAY

    )

    draw.text(

        (

            table_x + col_resources,

            table_y

        ),

        str(len(node["resources"])),

        font=PANEL_TEXT_FONT,

        fill=BLACK

    )

    draw.text(

        (

            table_x + col_groups,

            table_y

        ),

        str(len(groups_on_node)),

        font=PANEL_TEXT_FONT,

        fill=BLACK

    )

    table_y += 28



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

    str(len(resources)),

    font=PANEL_TEXT_BOLD,

    fill=BLACK

)

draw.text(

    (

        table_x + col_groups,

        table_y

    ),

    str(len(groups)),

    font=PANEL_TEXT_BOLD,

    fill=BLACK

)



# ============================================================

# PANEL 3 - CONSTRAINTS + SERVICES + FAILURES

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

    + 12

)

constraint_lines = [

    (

        "Order",

        constraint_counts["order"]

    ),

    (

        "CORE → NFSREC",

        constraint_counts["core_to_nfsrec_order"]

    ),

    (

        "NFSREC → PICATA",

        constraint_counts["nfsrec_to_picata_order"]

    ),

    (

        "NFSETC → updater",

        constraint_counts["etc_to_updater_order"]

    ),

    (

        "VIP workload coloc.",

        constraint_counts["vip_workload_colocation"]

    ),

    (

        "VIP anti-colocation",

        constraint_counts["vip_anti_colocation"]

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

    constraint_y += 23



constraint_y += 3

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

constraint_y += 10

draw.text(

    (

        x3 + PANEL_PADDING,

        constraint_y

    ),

    "CLNVRM SERVICES",

    font=PANEL_TEXT_BOLD,

    fill=PURPLE

)

constraint_y += 23

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

    str(len(clnvrm_instances)),

    font=PANEL_TEXT_BOLD,

    fill=BLACK

)

constraint_y += 23

if clnvrm_instances:

    instance_counts = [

        len(data["resources"])

        for data in clnvrm_instances.values()

    ]

    if (

        instance_counts

        and len(set(instance_counts)) == 1

    ):

        resource_per_instance = (

            instance_counts[0]

        )

    else:

        resource_per_instance = "varies"

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

    str(resource_per_instance),

    font=PANEL_TEXT_BOLD,

    fill=BLACK

)

constraint_y += 23

draw.text(

    (

        x3 + PANEL_PADDING,

        constraint_y

    ),

    "Admin stopped",

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

    str(administratively_stopped_count),

    font=PANEL_TEXT_BOLD,

    fill=ORANGE

)

constraint_y += 23

draw.text(

    (

        x3 + PANEL_PADDING,

        constraint_y

    ),

    "Failed actions",

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

    str(len(failed_actions)),

    font=PANEL_TEXT_BOLD,

    fill=(

        RED

        if failed_actions

        else GREEN

    )

)

# Show up to three failed actions.

if failed_actions:

    constraint_y += 27

    draw.text(

        (

            x3 + PANEL_PADDING,

            constraint_y

        ),

        "FAILED ACTIONS",

        font=SMALL_BOLD,

        fill=RED

    )

    constraint_y += 19

    for action in failed_actions[:3]:

        failure_line = (

            action["action"]

            + " @ "

            + action["node"]

        )

        draw.text(

            (

                x3 + PANEL_PADDING,

                constraint_y

            ),

            shorten(

                failure_line,

                42

            ),

            font=SMALL_FONT,

            fill=RED

        )

        constraint_y += 19



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

    GREEN if cluster_healthy else RED

)

health_y = (

    panel_y

    + PANEL_HEADER_HEIGHT

    + 14

)

if cluster_healthy:

    draw.text(

        (

            x4 + PANEL_PADDING,

            health_y

        ),

        "✓  All active systems are healthy.",

        font=PANEL_TEXT_BOLD,

        fill=DARK_GREEN

    )

else:

    draw.text(

        (

            x4 + PANEL_PADDING,

            health_y

        ),

        "!  Review conditions below.",

        font=PANEL_TEXT_BOLD,

        fill=RED

    )

health_y += 35

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

        running_groups == len(groups) - disabled_groups,

        "{} active resource groups running".format(

            running_groups

        )

    ),

    (

        True,

        "{} resource group(s) administratively stopped".format(

            disabled_groups

        )

    ),

    (

        degraded_groups == 0

        and stopped_groups == 0,

        "{} degraded / {} not running groups".format(

            degraded_groups,

            stopped_groups

        )

    ),

    (

        unexpected_stopped_count == 0,

        "{} unexpected stopped resources".format(

            unexpected_stopped_count

        )

    ),

    (

        administratively_stopped_count >= 0,

        "{} administratively stopped resources".format(

            administratively_stopped_count

        )

    ),

    (

        failed_count == 0,

        "{} currently failed resources".format(

            failed_count

        )

    ),

    (

        len(failed_actions) == 0,

        "{} failed resource actions".format(

            len(failed_actions)

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

        (
            constraint_counts["vip_workload_colocation"] > 0
            and constraint_counts["vip_anti_colocation"] > 0
        ),

        "VIP workload and anti-colocation configured"

        if (
            constraint_counts["vip_workload_colocation"] > 0
            and constraint_counts["vip_anti_colocation"] > 0
        )

        else "VIP colocation constraints missing"

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

        fill=DARK_GRAY if check_ok else RED

    )

    health_y += 23

    if health_y > (

        panel_y

        + bottom_panel_height

        - 20

    ):

        break



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

        "Stopped / Disabled",

        ORANGE

    ),

    (

        "Failed / Action failure",

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

    "  Disabled           : "

    + str(disabled_groups)

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

    "  Admin stopped      : "

    + str(administratively_stopped_count)

)

print(

    "  Unexpected stopped : "

    + str(unexpected_stopped_count)

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

    "Failed actions       : "

    + str(len(failed_actions))

)

for action in failed_actions:

    print(

        "  - "

        + action["action"]

        + " on "

        + action["node"]

        + " "

        + action["result"]

    )

print()

print("Constraints:")

print(

    "  Order              : "

    + str(constraint_counts["order"])

)

print(

    "  Colocation         : "

    + str(constraint_counts["colocation"])

)

print(

    "  Anti-colocation    : "

    + str(constraint_counts["anti_colocation"])

)

print(

    "    VIP workload     : "

    + str(constraint_counts["vip_workload_colocation"])

)

print(

    "    CORE -> NFSREC   : "

    + str(constraint_counts["core_to_nfsrec_order"])

)

print(

    "    NFSREC -> PICATA : "

    + str(constraint_counts["nfsrec_to_picata_order"])

)

print(

    "    NFSETC -> updater: "

    + str(constraint_counts["etc_to_updater_order"])

)

print(

    "    VIP anti-coloc   : "

    + str(constraint_counts["vip_anti_colocation"])

)

print(

    "  Location           : "

    + str(constraint_counts["location"])

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
