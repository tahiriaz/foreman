#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Update fence_ilo4 STONITH resources from:

    privlvl=user

to:

    privlvl=operator

The script runs from a laptop/workstation and connects to one
Pacemaker cluster node using SSH.

THREADING MODEL
---------------

To avoid concurrent modifications to the Pacemaker CIB:

    1. Resource discovery              - sequential
    2. Resource inspection            - THREADED
    3. CIB updates                    - SEQUENTIAL
    4. Resource verification           - THREADED

Each worker uses its own SSH connection.

Requirements:
    Python 3.x
    paramiko

Install:

    pip install paramiko

Examples:

    python update_stonith_privlvl.py

    python update_stonith_privlvl.py --host clnvrm011.mak.iss

    python update_stonith_privlvl.py --host 10.101.18.21 --user root

    python update_stonith_privlvl.py --host clnvrm011.mak.iss --workers 5
"""


# ============================================================================
# IMPORTS
# ============================================================================

import sys
import os
import re
import socket
import getpass
import logging
import argparse

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

import paramiko


# ============================================================================
# CONFIGURATION
# ============================================================================

# ---------------------------------------------------------------------------
# Default cluster node.
#
# You can put an IP/DNS name here, or provide --host.
# ---------------------------------------------------------------------------

CLUSTER_HOST = "10.101.28.60"


# ---------------------------------------------------------------------------
# SSH
# ---------------------------------------------------------------------------

SSH_PORT = 22

SSH_USERNAME = "root"

# Leave empty to be prompted securely.
SSH_PASSWORD = "Th@les01"

# Optional SSH private key.
#
# Example:
#
# SSH_KEY_FILE = r"D:\Users\Lotfi\.ssh\id_rsa"
#
SSH_KEY_FILE = ""


# ---------------------------------------------------------------------------
# SUDO
# ---------------------------------------------------------------------------

USE_SUDO = False

# Leave empty to be prompted.
SUDO_PASSWORD = ""


# ---------------------------------------------------------------------------
# SSH host key handling
# ---------------------------------------------------------------------------

AUTO_ACCEPT_HOST_KEY = True


# ---------------------------------------------------------------------------
# Remote command timeout
# ---------------------------------------------------------------------------

COMMAND_TIMEOUT = 120


# ---------------------------------------------------------------------------
# Target fence agent
# ---------------------------------------------------------------------------

TARGET_AGENT = "fence_ilo4"


# ---------------------------------------------------------------------------
# Target privilege
# ---------------------------------------------------------------------------

TARGET_PRIVLVL = "operator"


# ---------------------------------------------------------------------------
# Number of worker threads.
#
# This affects inspection and verification.
#
# CIB updates remain sequential for safety.
# ---------------------------------------------------------------------------

MAX_WORKERS = 5


# ---------------------------------------------------------------------------
# Log file
# ---------------------------------------------------------------------------

LOG_FILE = "update-stonith-privlvl.log"


# ============================================================================
# LOGGING
# ============================================================================

logger = logging.getLogger(
    "update_stonith_privlvl"
)

logger.setLevel(
    logging.INFO
)

logger.propagate = False


if not logger.handlers:

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s"
    )

    console_handler = logging.StreamHandler(
        sys.stdout
    )

    console_handler.setLevel(
        logging.INFO
    )

    console_handler.setFormatter(
        formatter
    )

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )

    file_handler.setLevel(
        logging.INFO
    )

    file_handler.setFormatter(
        formatter
    )

    logger.addHandler(
        console_handler
    )

    logger.addHandler(
        file_handler
    )


# ============================================================================
# SSH CLASS
# ============================================================================

class ClusterSSH(object):

    def __init__(
        self,
        host,
        username,
        password=None,
        key_file=None,
        port=22,
        use_sudo=False,
        sudo_password=None
    ):

        self.host = host
        self.username = username
        self.password = password
        self.key_file = key_file
        self.port = port

        self.use_sudo = use_sudo
        self.sudo_password = sudo_password

        self.client = None


    # ------------------------------------------------------------------------
    # CONNECT
    # ------------------------------------------------------------------------

    def connect(self):

        logger.info(
            "Connecting to %s:%d...",
            self.host,
            self.port
        )

        # ------------------------------------------------------------
        # Resolve hostname first.
        # ------------------------------------------------------------

        try:

            addresses = socket.getaddrinfo(
                self.host,
                self.port,
                socket.AF_UNSPEC,
                socket.SOCK_STREAM
            )

        except socket.gaierror as exc:

            logger.error(
                "ERROR: Cannot resolve '%s'.",
                self.host
            )

            logger.error(
                "DNS/name resolution error: %s",
                exc
            )

            logger.error(
                "Use a resolvable DNS name or an IP address."
            )

            raise RuntimeError(
                "Unable to resolve cluster node '{}'.".format(
                    self.host
                )
            )


        # ------------------------------------------------------------
        # Display resolved addresses.
        # ------------------------------------------------------------

        resolved = []

        for item in addresses:

            sockaddr = item[4]

            if sockaddr:

                address = sockaddr[0]

                if address not in resolved:

                    resolved.append(
                        address
                    )


        if resolved:

            logger.info(
                "Resolved %s -> %s",
                self.host,
                ", ".join(resolved)
            )


        # ------------------------------------------------------------
        # Create SSH client.
        # ------------------------------------------------------------

        self.client = paramiko.SSHClient()


        if AUTO_ACCEPT_HOST_KEY:

            self.client.set_missing_host_key_policy(
                paramiko.AutoAddPolicy()
            )

        else:

            self.client.load_system_host_keys()

            self.client.set_missing_host_key_policy(
                paramiko.RejectPolicy()
            )


        connect_args = {
            "hostname": self.host,
            "port": self.port,
            "username": self.username,
            "timeout": 20,
            "banner_timeout": 20,
            "auth_timeout": 20,
            "look_for_keys": False,
            "allow_agent": False,
        }


        if self.key_file:

            connect_args["key_filename"] = (
                self.key_file
            )

        else:

            connect_args["password"] = (
                self.password
            )


        try:

            self.client.connect(
                **connect_args
            )

        except Exception as exc:

            logger.error(
                "ERROR: SSH connection to %s:%d failed.",
                self.host,
                self.port
            )

            logger.error(
                "%s",
                exc
            )

            self.close()

            raise


        transport = self.client.get_transport()

        if transport:

            transport.set_keepalive(
                30
            )


        logger.info(
            "SSH connection established."
        )


    # ------------------------------------------------------------------------
    # CLOSE
    # ------------------------------------------------------------------------

    def close(self):

        if self.client:

            try:

                self.client.close()

            except Exception:

                pass

            self.client = None


    # ------------------------------------------------------------------------
    # EXECUTE
    # ------------------------------------------------------------------------

    def execute(
        self,
        command,
        timeout=COMMAND_TIMEOUT
    ):

        if not self.client:

            raise RuntimeError(
                "SSH connection is not established."
            )


        # ------------------------------------------------------------
        # SUDO
        # ------------------------------------------------------------

        if self.use_sudo:

            escaped_command = command.replace(
                "'",
                "'\\''"
            )

            remote_command = (
                "sudo -S -p '' sh -c '{}'"
            ).format(
                escaped_command
            )

        else:

            remote_command = command


        stdin, stdout, stderr = (
            self.client.exec_command(
                remote_command,
                timeout=timeout,
                get_pty=self.use_sudo
            )
        )


        # ------------------------------------------------------------
        # Supply sudo password.
        # ------------------------------------------------------------

        if self.use_sudo:

            if not self.sudo_password:

                raise RuntimeError(
                    "sudo password is required."
                )

            stdin.write(
                self.sudo_password + "\n"
            )

            stdin.flush()


        # ------------------------------------------------------------
        # Read output.
        # ------------------------------------------------------------

        stdout_data = stdout.read()

        stderr_data = stderr.read()

        exit_status = (
            stdout.channel.recv_exit_status()
        )


        if isinstance(
            stdout_data,
            bytes
        ):

            stdout_data = stdout_data.decode(
                "utf-8",
                errors="replace"
            )


        if isinstance(
            stderr_data,
            bytes
        ):

            stderr_data = stderr_data.decode(
                "utf-8",
                errors="replace"
            )


        return (
            exit_status,
            stdout_data,
            stderr_data
        )


# ============================================================================
# CREATE SSH CONNECTION
# ============================================================================

def create_worker_ssh():

    ssh = ClusterSSH(
        host=GLOBAL_CONFIG["host"],
        username=GLOBAL_CONFIG["username"],
        password=GLOBAL_CONFIG["password"],
        key_file=GLOBAL_CONFIG["key_file"],
        port=GLOBAL_CONFIG["port"],
        use_sudo=GLOBAL_CONFIG["use_sudo"],
        sudo_password=GLOBAL_CONFIG["sudo_password"]
    )

    ssh.connect()

    return ssh


# ============================================================================
# GLOBAL WORKER CONFIGURATION
# ============================================================================

GLOBAL_CONFIG = {
    "host": None,
    "username": None,
    "password": None,
    "key_file": None,
    "port": 22,
    "use_sudo": False,
    "sudo_password": None,
}


# ============================================================================
# REMOTE COMMAND
# ============================================================================

def run_remote(
    ssh,
    command
):

    return ssh.execute(
        command
    )


# ============================================================================
# CHECK PCS
# ============================================================================

def check_pcs(
    ssh
):

    logger.info(
        "Checking Pacemaker cluster..."
    )


    rc, stdout, stderr = run_remote(
        ssh,
        "pcs status"
    )


    if rc != 0:

        logger.error(
            "ERROR: pcs status failed."
        )


        if stdout.strip():

            logger.error(
                "STDOUT:\n%s",
                stdout.strip()
            )


        if stderr.strip():

            logger.error(
                "STDERR:\n%s",
                stderr.strip()
            )


        return False


    logger.info(
        "Pacemaker cluster is accessible."
    )


    return True


# ============================================================================
# GET STONITH RESOURCES
# ============================================================================

def get_stonith_resources(
    ssh
):

    logger.info(
        ""
    )

    logger.info(
        "Getting STONITH resources..."
    )


    rc, stdout, stderr = run_remote(
        ssh,
        "pcs stonith config"
    )


    if rc != 0:

        logger.error(
            "ERROR: pcs stonith config failed."
        )


        if stdout.strip():

            logger.error(
                "STDOUT:\n%s",
                stdout.strip()
            )


        if stderr.strip():

            logger.error(
                "STDERR:\n%s",
                stderr.strip()
            )


        return []


    resources = []


    # ------------------------------------------------------------------------
    # Expected:
    #
    # Resource: fence_tvsnvrapp016mp (class=stonith type=fence_ilo4)
    # ------------------------------------------------------------------------

    for line in stdout.splitlines():

        line = line.strip()


        if not line.startswith(
            "Resource:"
        ):

            continue


        match = re.match(
            r"Resource:\s+(\S+)",
            line
        )


        if match:

            resource = match.group(1)


            if resource not in resources:

                resources.append(
                    resource
                )


    return resources


# ============================================================================
# GET RESOURCE CONFIG
# ============================================================================

def get_resource_config(
    ssh,
    resource
):

    command = (
        "pcs stonith config {}"
    ).format(
        resource
    )


    rc, stdout, stderr = run_remote(
        ssh,
        command
    )


    if rc != 0:

        return None


    return stdout


# ============================================================================
# GET RESOURCE TYPE
# ============================================================================

def get_resource_type(
    config
):

    if not config:

        return ""


    # ------------------------------------------------------------------------
    # Correct regex.
    #
    # Example:
    #
    # type=fence_ilo4
    # ------------------------------------------------------------------------

    match = re.search(
        r"\btype=([^\s\)]+)",
        config,
        flags=re.IGNORECASE
    )


    if match:

        return match.group(1).strip()


    # ------------------------------------------------------------------------
    # Fallback.
    # ------------------------------------------------------------------------

    if re.search(
        r"\bfence_ilo4\b",
        config,
        flags=re.IGNORECASE
    ):

        return TARGET_AGENT


    return ""


# ============================================================================
# GET PRIVLVL
# ============================================================================

def get_privlvl(
    config
):

    if not config:

        return None


    match = re.search(
        r"(?:^|\s)privlvl=([^\s]+)",
        config,
        flags=re.IGNORECASE
    )


    if match:

        return match.group(1).strip()


    return None


# ============================================================================
# INSPECT ONE RESOURCE
# ============================================================================
#
# This function is THREAD SAFE because it only READS configuration.
# ============================================================================

def inspect_resource(
    resource
):

    ssh = None


    try:

        logger.info(
            "[THREAD] Inspecting %s...",
            resource
        )


        ssh = create_worker_ssh()


        config = get_resource_config(
            ssh,
            resource
        )


        if config is None:

            return {
                "resource": resource,
                "status": "FAILED",
                "type": "",
                "privlvl": None,
                "config": None,
            }


        resource_type = get_resource_type(
            config
        )


        current_privlvl = get_privlvl(
            config
        )


        if (
            resource_type.lower()
            != TARGET_AGENT.lower()
        ):

            logger.info(
                "[THREAD] %s -> SKIPPED (%s)",
                resource,
                resource_type or "unknown"
            )

            return {
                "resource": resource,
                "status": "SKIPPED",
                "type": resource_type,
                "privlvl": current_privlvl,
                "config": config,
            }


        logger.info(
            "[THREAD] %s -> type=%s privlvl=%s",
            resource,
            resource_type,
            current_privlvl or "NOT SET"
        )


        return {
            "resource": resource,
            "status": "OK",
            "type": resource_type,
            "privlvl": current_privlvl,
            "config": config,
        }


    except Exception as exc:

        logger.error(
            "[THREAD] %s inspection failed: %s",
            resource,
            exc
        )


        return {
            "resource": resource,
            "status": "FAILED",
            "type": "",
            "privlvl": None,
            "config": None,
            "error": str(exc),
        }


    finally:

        if ssh:

            ssh.close()


# ============================================================================
# UPDATE ONE RESOURCE
# ============================================================================
#
# IMPORTANT:
#
# This function is intentionally NOT called from multiple threads.
#
# PCS modifies the Pacemaker CIB. We update resources sequentially to avoid
# concurrent CIB transactions.
# ============================================================================

def update_resource(
    ssh,
    resource
):

    command = (
        "pcs stonith update {} privlvl={}"
    ).format(
        resource,
        TARGET_PRIVLVL
    )


    logger.info(
        ""
    )


    logger.info(
        "Updating %s",
        resource
    )


    logger.info(
        "    privlvl -> %s",
        TARGET_PRIVLVL
    )


    rc, stdout, stderr = run_remote(
        ssh,
        command
    )


    if rc == 0:

        logger.info(
            "SUCCESS: %s updated.",
            resource
        )

        return True


    logger.error(
        "ERROR: Failed to update %s.",
        resource
    )


    if stdout.strip():

        logger.error(
            "STDOUT:\n%s",
            stdout.strip()
        )


    if stderr.strip():

        logger.error(
            "STDERR:\n%s",
            stderr.strip()
        )


    return False


# ============================================================================
# VERIFY ONE RESOURCE
# ============================================================================
#
# Verification is READ ONLY, therefore it can safely be threaded.
# ============================================================================

def verify_resource_threaded(
    resource
):

    ssh = None


    try:

        ssh = create_worker_ssh()


        config = get_resource_config(
            ssh,
            resource
        )


        if config is None:

            return {
                "resource": resource,
                "verified": False,
                "privlvl": None,
            }


        current_privlvl = get_privlvl(
            config
        )


        verified = (
            current_privlvl is not None
            and
            current_privlvl.lower()
            == TARGET_PRIVLVL.lower()
        )


        if verified:

            logger.info(
                "[THREAD] VERIFIED: %s privlvl=%s",
                resource,
                current_privlvl
            )

        else:

            logger.error(
                "[THREAD] VERIFICATION FAILED: %s "
                "privlvl=%s",
                resource,
                current_privlvl or "NOT SET"
            )


        return {
            "resource": resource,
            "verified": verified,
            "privlvl": current_privlvl,
        }


    except Exception as exc:

        logger.error(
            "[THREAD] Verification failed for %s: %s",
            resource,
            exc
        )


        return {
            "resource": resource,
            "verified": False,
            "privlvl": None,
            "error": str(exc),
        }


    finally:

        if ssh:

            ssh.close()


# ============================================================================
# PARALLEL INSPECTION
# ============================================================================

def inspect_resources_parallel(
    resources,
    max_workers
):

    results = {}


    logger.info(
        ""
    )

    logger.info(
        "Inspecting %d STONITH resources using %d threads...",
        len(resources),
        max_workers
    )


    with ThreadPoolExecutor(
        max_workers=max_workers
    ) as executor:

        future_map = {}


        for resource in resources:

            future = executor.submit(
                inspect_resource,
                resource
            )

            future_map[future] = resource


        for future in as_completed(
            future_map
        ):

            resource = future_map[future]


            try:

                result = future.result()

                results[resource] = result


            except Exception as exc:

                logger.error(
                    "[THREAD] Unexpected failure for %s: %s",
                    resource,
                    exc
                )


                results[resource] = {
                    "resource": resource,
                    "status": "FAILED",
                    "type": "",
                    "privlvl": None,
                    "config": None,
                    "error": str(exc),
                }


    return results


# ============================================================================
# PARALLEL VERIFICATION
# ============================================================================

def verify_resources_parallel(
    resources,
    max_workers
):

    results = {}


    if not resources:

        return results


    logger.info(
        ""
    )

    logger.info(
        "Verifying %d resource(s) using %d threads...",
        len(resources),
        max_workers
    )


    with ThreadPoolExecutor(
        max_workers=max_workers
    ) as executor:

        future_map = {}


        for resource in resources:

            future = executor.submit(
                verify_resource_threaded,
                resource
            )

            future_map[future] = resource


        for future in as_completed(
            future_map
        ):

            resource = future_map[future]


            try:

                result = future.result()

                results[resource] = result


            except Exception as exc:

                logger.error(
                    "[THREAD] Unexpected verification "
                    "failure for %s: %s",
                    resource,
                    exc
                )


                results[resource] = {
                    "resource": resource,
                    "verified": False,
                    "privlvl": None,
                    "error": str(exc),
                }


    return results


# ============================================================================
# ARGUMENTS
# ============================================================================

def parse_arguments():

    parser = argparse.ArgumentParser(
        description=(
            "Update fence_ilo4 STONITH resources "
            "to privlvl=operator."
        )
    )


    parser.add_argument(
        "--host",
        default=CLUSTER_HOST,
        help=(
            "Cluster node IP or DNS name."
        )
    )


    parser.add_argument(
        "--user",
        default=SSH_USERNAME,
        help=(
            "SSH username."
        )
    )


    parser.add_argument(
        "--password",
        default=None,
        help=(
            "SSH password. "
            "If omitted, prompt securely."
        )
    )


    parser.add_argument(
        "--key",
        default=SSH_KEY_FILE,
        help=(
            "SSH private key."
        )
    )


    parser.add_argument(
        "--port",
        type=int,
        default=SSH_PORT,
        help=(
            "SSH port. Default 22."
        )
    )


    parser.add_argument(
        "--sudo",
        action="store_true",
        help=(
            "Run PCS commands through sudo."
        )
    )


    parser.add_argument(
        "--sudo-password",
        default=None,
        help=(
            "sudo password."
        )
    )


    parser.add_argument(
        "--workers",
        type=int,
        default=MAX_WORKERS,
        help=(
            "Number of worker threads. "
            "Default: {}.".format(
                MAX_WORKERS
            )
        )
    )


    return parser.parse_args()


# ============================================================================
# MAIN
# ============================================================================

def main():

    global GLOBAL_CONFIG


    args = parse_arguments()


    # ------------------------------------------------------------------------
    # Validate workers.
    # ------------------------------------------------------------------------

    if args.workers < 1:

        logger.error(
            "ERROR: --workers must be at least 1."
        )

        return 1


    # ------------------------------------------------------------------------
    # HOST
    # ------------------------------------------------------------------------

    host = args.host


    if not host:

        host = input(
            "Cluster node IP/DNS name: "
        ).strip()


    if not host:

        logger.error(
            "ERROR: Cluster node was not specified."
        )

        return 1


    # ------------------------------------------------------------------------
    # USER
    # ------------------------------------------------------------------------

    username = args.user


    if not username:

        username = input(
            "SSH username: "
        ).strip()


    if not username:

        logger.error(
            "ERROR: SSH username was not specified."
        )

        return 1


    # ------------------------------------------------------------------------
    # PASSWORD
    # ------------------------------------------------------------------------

    password = args.password


    if (
        not args.key
        and
        password is None
    ):

        password = getpass.getpass(
            "SSH password: "
        )


    # ------------------------------------------------------------------------
    # SUDO PASSWORD
    # ------------------------------------------------------------------------

    sudo_password = args.sudo_password


    if (
        args.sudo
        and
        sudo_password is None
    ):

        sudo_password = getpass.getpass(
            "sudo password: "
        )


    # ------------------------------------------------------------------------
    # Store worker configuration.
    # ------------------------------------------------------------------------

    GLOBAL_CONFIG = {
        "host": host,
        "username": username,
        "password": password,
        "key_file": args.key or None,
        "port": args.port,
        "use_sudo": args.sudo,
        "sudo_password": sudo_password,
    }


    # ------------------------------------------------------------------------
    # HEADER
    # ------------------------------------------------------------------------

    logger.info("")

    logger.info(
        "=" * 70
    )

    logger.info(
        "STONITH privilege-level update"
    )

    logger.info(
        "=" * 70
    )

    logger.info(
        "Cluster node : %s",
        host
    )

    logger.info(
        "SSH user     : %s",
        username
    )

    logger.info(
        "Target agent : %s",
        TARGET_AGENT
    )

    logger.info(
        "Target level : %s",
        TARGET_PRIVLVL
    )

    logger.info(
        "SSH port     : %d",
        args.port
    )

    logger.info(
        "Workers      : %d",
        args.workers
    )

    logger.info(
        "Sudo         : %s",
        "YES" if args.sudo else "NO"
    )

    logger.info(
        "=" * 70
    )


    ssh = ClusterSSH(
        host=host,
        username=username,
        password=password,
        key_file=args.key or None,
        port=args.port,
        use_sudo=args.sudo,
        sudo_password=sudo_password,
    )


    try:

        # ====================================================================
        # CONNECT
        # ====================================================================

        ssh.connect()


        # ====================================================================
        # CHECK CLUSTER
        # ====================================================================

        if not check_pcs(
            ssh
        ):

            return 1


        # ====================================================================
        # GET STONITH RESOURCES
        # ====================================================================

        resources = get_stonith_resources(
            ssh
        )


        if not resources:

            logger.info(
                "No STONITH resources found."
            )

            return 0


        logger.info(
            ""
        )

        logger.info(
            "Found %d STONITH resource(s):",
            len(resources)
        )


        for resource in resources:

            logger.info(
                "  %s",
                resource
            )


        # ====================================================================
        # CLOSE INITIAL SSH CONNECTION
        #
        # Worker threads create their own connections.
        # ====================================================================

        ssh.close()


        # ====================================================================
        # STEP 1:
        #
        # PARALLEL RESOURCE INSPECTION
        # ====================================================================

        inspection_results = (
            inspect_resources_parallel(
                resources,
                args.workers
            )
        )


        # ====================================================================
        # Determine which resources need modification.
        # ====================================================================

        resources_to_update = []


        failed_inspection = []


        for resource in resources:

            result = inspection_results.get(
                resource
            )


            if not result:

                failed_inspection.append(
                    resource
                )

                continue


            if result["status"] == "FAILED":

                failed_inspection.append(
                    resource
                )

                continue


            if result["status"] != "OK":

                continue


            current_privlvl = result[
                "privlvl"
            ]


            if (
                current_privlvl
                and
                current_privlvl.lower()
                == TARGET_PRIVLVL.lower()
            ):

                continue


            resources_to_update.append(
                resource
            )


        # ====================================================================
        # STEP 2:
        #
        # SEQUENTIAL CIB UPDATES
        #
        # We intentionally do NOT parallelize this.
        # ====================================================================

        logger.info(
            ""
        )

        logger.info(
            "=" * 70
        )

        logger.info(
            "CIB UPDATE PHASE"
        )

        logger.info(
            "=" * 70
        )


        updated = []


        if resources_to_update:

            logger.info(
                "Resources requiring update: %d",
                len(resources_to_update)
            )


            # Reconnect for CIB updates.

            ssh = ClusterSSH(
                host=host,
                username=username,
                password=password,
                key_file=args.key or None,
                port=args.port,
                use_sudo=args.sudo,
                sudo_password=sudo_password,
            )


            ssh.connect()


            for resource in resources_to_update:

                success = update_resource(
                    ssh,
                    resource
                )


                if success:

                    updated.append(
                        resource
                    )


            ssh.close()


        else:

            logger.info(
                "No fence_ilo4 resources require modification."
            )


        # ====================================================================
        # STEP 3:
        #
        # PARALLEL VERIFICATION
        # ====================================================================

        verification_targets = list(
            resources_to_update
        )


        verification_results = (
            verify_resources_parallel(
                verification_targets,
                args.workers
            )
        )


        verified = []

        verification_failed = []


        for resource in verification_targets:

            result = verification_results.get(
                resource
            )


            if (
                result
                and
                result.get(
                    "verified",
                    False
                )
            ):

                verified.append(
                    resource
                )

            else:

                verification_failed.append(
                    resource
                )


        # ====================================================================
        # FINAL SUMMARY
        # ====================================================================

        logger.info(
            ""
        )

        logger.info(
            "=" * 70
        )

        logger.info(
            "SUMMARY"
        )

        logger.info(
            "=" * 70
        )


        already_correct = []


        for resource in resources:

            result = inspection_results.get(
                resource
            )


            if not result:

                continue


            if (
                result["status"] == "OK"
                and
                result["privlvl"]
                and
                result["privlvl"].lower()
                == TARGET_PRIVLVL.lower()
            ):

                already_correct.append(
                    resource
                )


        non_ilo = []


        for resource in resources:

            result = inspection_results.get(
                resource
            )


            if not result:

                continue


            if result["status"] == "SKIPPED":

                non_ilo.append(
                    resource
                )


        logger.info(
            "STONITH resources found : %d",
            len(resources)
        )

        logger.info(
            "Already correct         : %d",
            len(already_correct)
        )

        logger.info(
            "Updated                 : %d",
            len(updated)
        )

        logger.info(
            "Verified                : %d",
            len(verified)
        )

        logger.info(
            "Non-fence_ilo4 skipped  : %d",
            len(non_ilo)
        )

        logger.info(
            "Inspection failed      : %d",
            len(failed_inspection)
        )

        logger.info(
            "Verification failed    : %d",
            len(verification_failed)
        )


        # --------------------------------------------------------------------
        # Detailed lists.
        # --------------------------------------------------------------------

        if already_correct:

            logger.info(
                ""
            )

            logger.info(
                "ALREADY CORRECT:"
            )


            for resource in already_correct:

                logger.info(
                    "  %s",
                    resource
                )


        if updated:

            logger.info(
                ""
            )

            logger.info(
                "UPDATED:"
            )


            for resource in updated:

                logger.info(
                    "  %s",
                    resource
                )


        if verified:

            logger.info(
                ""
            )

            logger.info(
                "VERIFIED:"
            )


            for resource in verified:

                logger.info(
                    "  %s",
                    resource
                )


        if non_ilo:

            logger.info(
                ""
            )

            logger.info(
                "SKIPPED NON-fence_ilo4:"
            )


            for resource in non_ilo:

                logger.info(
                    "  %s",
                    resource
                )


        if failed_inspection:

            logger.info(
                ""
            )

            logger.info(
                "INSPECTION FAILED:"
            )


            for resource in failed_inspection:

                logger.info(
                    "  %s",
                    resource
                )


        if verification_failed:

            logger.info(
                ""
            )

            logger.info(
                "VERIFICATION FAILED:"
            )


            for resource in verification_failed:

                logger.info(
                    "  %s",
                    resource
                )


        logger.info(
            "=" * 70
        )


        # ====================================================================
        # FAILURE CONDITIONS
        # ====================================================================

        if failed_inspection:

            return 1


        if verification_failed:

            return 1


        return 0


    except KeyboardInterrupt:

        logger.warning(
            "Interrupted by user."
        )

        return 130


    except Exception as exc:

        logger.exception(
            "FATAL ERROR: %s",
            exc
        )

        return 1


    finally:

        ssh.close()

        logger.info(
            "SSH connection closed."
        )


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":

    sys.exit(
        main()
    )