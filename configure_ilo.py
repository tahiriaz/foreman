#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import time
from pathlib import Path
import paramiko
from jinja2 import Environment, FileSystemLoader, StrictUndefined

# ============================================================================
# OA & iLO CONFIGURATION
# ============================================================================

OA_IP = "10.101.18.210"
OA_USERNAME = "Administrator"
OA_PASSWORD = "Siljeddah15"
BAY_NUMBER = 8

ILO_LOGIN = "admin"
ILO_PASSWORD = "password"

FENCE_USER_NAME = "Pacemaker Fence"
FENCE_USER_LOGIN = "hpilofence"
FENCE_USER_PASSWORD = "Th@les01"

IPMI_PORT = "623"

ILO_DOMAIN = "mak.iss"
PRIMARY_DNS = "10.130.2.11"
SECONDARY_DNS = "10.130.2.12"
DIRECTORY_SERVER = "INFCOSADU001MP.mak.iss"

DIR_USER_CONTEXT_1 = "OU=IT,OU=ISS,DC=mak,DC=iss"
DIR_USER_CONTEXT_2 = "CN=Users,DC=mak,DC=iss"
DIR_USER_CONTEXT_3 = "CN=Builtin,DC=mak,DC=iss"
DIR_USER_CONTEXT_4 = "@mak.iss"

# ============================================================================
# SETTINGS & PATHS
# ============================================================================

DEBUG_MODE = 1

SSH_PORT = 22
SSH_CONNECT_TIMEOUT = 15
COMMAND_TIMEOUT = 180
COMMAND_QUIET_TIME = 15.0 

BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "Templates"
TEMPLATE_FILE = "ilo_config.xml.j2"

# ============================================================================
# LOGIC
# ============================================================================

def create_jinja_environment():
    return Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        undefined=StrictUndefined,
        autoescape=False,
        keep_trailing_newline=True,
    )

def render_template(add_user, apply_ipmi_config):
    env = create_jinja_environment()
    template = env.get_template(TEMPLATE_FILE)
    return template.render(
        add_user=add_user,
        apply_ipmi_config=apply_ipmi_config,
        ilo_login=ILO_LOGIN, ilo_password=ILO_PASSWORD,
        fence_user_name=FENCE_USER_NAME, fence_user_login=FENCE_USER_LOGIN,
        fence_user_password=FENCE_USER_PASSWORD,
        ipmi_port=IPMI_PORT,
        ilo_domain=ILO_DOMAIN, primary_dns=PRIMARY_DNS,
        secondary_dns=SECONDARY_DNS, directory_server=DIRECTORY_SERVER,
        dir_user_context_1=DIR_USER_CONTEXT_1,
        dir_user_context_2=DIR_USER_CONTEXT_2,
        dir_user_context_3=DIR_USER_CONTEXT_3,
        dir_user_context_4=DIR_USER_CONTEXT_4,
    )

class OAConnection(object):
    def __init__(self, hostname, username, password, port=22):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.client = None
        self.channel = None

    def connect(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(
            hostname=self.hostname, port=self.port,
            username=self.username, password=self.password,
            timeout=SSH_CONNECT_TIMEOUT, look_for_keys=False, allow_agent=False,
        )
        self.channel = self.client.invoke_shell()
        time.sleep(1)
        self._drain_channel()

    def close(self):
        if self.channel:
            try: self.channel.close()
            except Exception: pass
        if self.client:
            try: self.client.close()
            except Exception: pass

    def _drain_channel(self):
        if not self.channel: return ""
        output = ""
        while self.channel.recv_ready():
            data = self.channel.recv(65535)
            if not data: break
            output += data.decode("utf-8", errors="replace")
        return output

    def read_command_output(self, timeout=COMMAND_TIMEOUT):
        output = ""
        deadline = time.monotonic() + timeout
        quiet_since = None

        while time.monotonic() < deadline:
            if self.channel.recv_ready():
                data = self.channel.recv(65535)
                if not data: break
                output += data.decode("utf-8", errors="replace")
                quiet_since = None
            else:
                if quiet_since is None:
                    quiet_since = time.monotonic()
                elif time.monotonic() - quiet_since >= COMMAND_QUIET_TIME:
                    break
                time.sleep(0.1)
        else:
            raise TimeoutError("Timed out waiting for OA command output.")
        return output

    def execute_hponcfg(self, bay_number, ribcl, end_marker="ILO_RIBCL_EOF"):
        self._drain_channel()
        command = "HPONCFG {0} << {1}\n{2}\n{1}\n".format(
            bay_number, end_marker, ribcl.rstrip()
        )
        for line in command.splitlines():
            self.channel.send(line + "\n")
            time.sleep(0.05)
        return self.read_command_output()

def check_fence_user(oa):
    print(f"Checking if user '{FENCE_USER_LOGIN}' exists on Bay {BAY_NUMBER}...")
    ribcl = '<RIBCL VERSION="2.0">\n<LOGIN USER_LOGIN="{0}" PASSWORD="{1}">\n<USER_INFO MODE="read">\n<GET_USER USER_LOGIN="{2}"/>\n</USER_INFO>\n</LOGIN>\n</RIBCL>'.format(
        ILO_LOGIN, ILO_PASSWORD, FENCE_USER_LOGIN
    )
    output = oa.execute_hponcfg(bay_number=BAY_NUMBER, ribcl=ribcl, end_marker="ILO_USER_CHECK_EOF")
    
    # Parse all hex status codes returned by the iLO
    statuses = re.findall(r'<RESPONSE\s+STATUS=["\']([^"\']+)["\']', output, re.IGNORECASE)
    
    if "0x000A" in statuses:
        return False # 0x000A specifically means "User not found"
        
    if "0x0000" in statuses:
        return True # User was successfully queried
        
    return False

def check_ipmi_settings(oa):
    print(f"Checking current IPMI settings on Bay {BAY_NUMBER}...")
    ribcl = '<RIBCL VERSION="2.0">\n<LOGIN USER_LOGIN="{0}" PASSWORD="{1}">\n<RIB_INFO MODE="read">\n<GET_GLOBAL_SETTINGS/>\n</RIB_INFO>\n</LOGIN>\n</RIBCL>'.format(
        ILO_LOGIN, ILO_PASSWORD
    )
    output = oa.execute_hponcfg(bay_number=BAY_NUMBER, ribcl=ribcl, end_marker="ILO_IPMI_CHECK_EOF")
    
    port_match = re.search(r'IPMI_DCMI_OVER_LAN_PORT\s*VALUE\s*=\s*["\'](\d+)["\']', output, re.IGNORECASE)
    enabled_match = re.search(r'IPMI_DCMI_OVER_LAN_ENABLED\s*VALUE\s*=\s*["\']([Yy])["\']', output, re.IGNORECASE)
    
    is_enabled = bool(enabled_match)
    port_is_target = bool(port_match and port_match.group(1) == str(IPMI_PORT))
    
    if is_enabled and port_is_target:
        print(f"-> IPMI is already ENABLED on port {IPMI_PORT}. Skipping IPMI configuration.")
        return False
    else:
        print("-> IPMI needs configuration. Queuing global settings update.")
        return True

def validate_hponcfg_result(output):
    if "END RIBCL RESULTS" not in output:
        print("\nERROR: OA did not finish sending the RIBCL results. The SSH read timed out.")
        return False

    # Extract all RESPONSE tags and their messages
    responses = re.findall(r'<RESPONSE\s+STATUS=["\']([^"\']+)["\']\s+MESSAGE=[\'"]([^\'"]+)[\'"]', output, re.IGNORECASE)
    
    has_error = False
    for status, message in responses:
        # 0x0000 is success. Any other code is a failure for that specific block.
        if status != "0x0000":
            print(f"ERROR returned by iLO: STATUS={status} | MESSAGE='{message}'")
            has_error = True
            
    if has_error:
        print("\nFAILURE: iLO rejected one or more configuration blocks. See above errors.")
        return False
    
    print("\nSUCCESS: Configuration applied. (Note: iLO may take 3-5 minutes to reboot and apply directory changes).")
    return True

def main():
    print(f"Starting configuration for Bay {BAY_NUMBER}...")

    template_path = TEMPLATE_DIR / TEMPLATE_FILE
    if not template_path.is_file():
        print(f"ERROR: Template missing: {template_path}", file=sys.stderr)
        return 1

    oa = OAConnection(hostname=OA_IP, username=OA_USERNAME, password=OA_PASSWORD, port=SSH_PORT)

    try:
        oa.connect()
        
        user_exists = check_fence_user(oa)
        if user_exists:
            print(f"-> User '{FENCE_USER_LOGIN}' exists. Skipping creation.")
        else:
            print(f"-> User '{FENCE_USER_LOGIN}' missing. Queuing creation.")

        apply_ipmi = check_ipmi_settings(oa)

        ribcl = render_template(add_user=not user_exists, apply_ipmi_config=apply_ipmi)
        print("-> Pushing RIBCL configuration (this will take 10-20 seconds for the OA to process)...")
        
        result = oa.execute_hponcfg(bay_number=BAY_NUMBER, ribcl=ribcl)

        if DEBUG_MODE == 1:
            print("\n" + "=" * 78)
            print("DEBUG: RAW RIBCL RESULTS")
            print("=" * 78)
            print(result)
            print("=" * 78 + "\n")

        if not validate_hponcfg_result(result):
            return 1
            
        return 0

    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 5
    finally:
        oa.close()

if __name__ == "__main__":
    sys.exit(main())