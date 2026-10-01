
from xmlrpc import client

import paramiko
import re
import sys
import socket

# ============================================================
# CONFIGURATION
# ============================================================

# IP address of any reachable node in the PCS cluster
PCS_NODE_IP = "clnvrm011.mak.iss"

# SSH credentials
SSH_USERNAME = "root"
SSH_PASSWORD = "Th@les01"

SSH_PORT = 22
SSH_TIMEOUT = 15

# ============================================================
# SSH CONNECTION
# ============================================================

def ssh_connect(host):
    """Connect to a Linux host using SSH."""

    client = paramiko.SSHClient()

    # Use the laptop's known_hosts file.
    # Unknown SSH host keys will be rejected.
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(
        hostname=host,
        port=SSH_PORT,
        username=SSH_USERNAME,
        password=SSH_PASSWORD,
        timeout=SSH_TIMEOUT,
        banner_timeout=SSH_TIMEOUT,
        auth_timeout=SSH_TIMEOUT,
        look_for_keys=False,
        allow_agent=False
    )

    return client


# ============================================================
# EXECUTE REMOTE COMMAND
# ============================================================

def run_command(client, command):
    """Execute a command and return exit code, stdout, stderr."""

    stdin, stdout, stderr = client.exec_command(
        command,
        timeout=60
    )

    exit_code = stdout.channel.recv_exit_status()

    output = stdout.read().decode(
        "utf-8", errors="replace"
    ).strip()

    error = stderr.read().decode(
        "utf-8", errors="replace"
    ).strip()

    return exit_code, output, error


# ============================================================
# GET ONLINE PCS NODES
# ============================================================

def get_online_nodes():
    """Query PCS status and extract online node hostnames."""

    print(f"\nConnecting to PCS node: {PCS_NODE_IP}")

    client = ssh_connect(PCS_NODE_IP)

    try:
        rc, output, error = run_command(
            client,
            "pcs status"
        )

        if rc != 0:
            raise RuntimeError(
                f"pcs status failed: {error or output}"
            )

        # Example:
        # * Online: [ node001.example.com node002.example.com ]

        match = re.search(
            r"Online:\s*\[(.*?)\]",
            output,
            re.DOTALL
        )

        if not match:
            raise RuntimeError(
                "Could not find the Online node list in pcs status."
            )

        nodes = match.group(1).split()

        if not nodes:
            raise RuntimeError(
                "PCS returned an empty Online node list."
            )

        print("\nOnline PCS nodes:")

        for node in nodes:
            print(f"  {node}")

        return nodes

    finally:
        client.close()


# ============================================================
# STOP AND DISABLE FIREWALL
# ============================================================

def disable_firewall(node):
    """Stop firewalld and disable it at boot."""

    print(f"\n[{node}] Connecting...")

    client = None

    try:
        client = ssh_connect(node)

        # Stop firewalld now, then disable it at boot.
        # The second command runs only if the first succeeds.
        command = (
            "systemctl stop firewalld && "
            "systemctl disable firewalld"
        )

        rc, output, error = run_command(
            client,
            command
        )

        if rc == 0:
            print(
                f"[{node}] SUCCESS: firewalld stopped "
                "and disabled."
            )

            # Verify the resulting state
            rc1, active, err1 = run_command(
                client,
                "systemctl is-active firewalld"
            )

            rc2, enabled, err2 = run_command(
                client,
                "systemctl is-enabled firewalld"
            )

            print(
                f"[{node}] Active state: {active or err1}"
            )

            print(
                f"[{node}] Enabled state: {enabled or err2}"
            )

        else:
            print(f"[{node}] FAILED (exit code {rc})")
            print(error or output)

    except (
        paramiko.SSHException,
        socket.error,
        TimeoutError,
        OSError
    ) as exc:
        print(f"[{node}] SSH ERROR: {exc}")

    finally:
        if client:
            client.close()


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("PCS CLUSTER FIREWALL MANAGEMENT")
    print("=" * 60)

    try:
        nodes = get_online_nodes()

    except Exception as exc:
        print(f"\nERROR: Could not retrieve PCS nodes: {exc}")
        sys.exit(1)

    print(f"\nFound {len(nodes)} online nodes.")

    # Ask for confirmation before changing all nodes
    confirmation = input(
        "\nStop and disable firewalld on ALL listed nodes? "
        "(yes/no): "
    ).strip().lower()

    if confirmation != "yes":
        print("Operation cancelled.")
        return

    for node in nodes:
        disable_firewall(node)

    print("\n" + "=" * 60)
    print("Firewall operation completed.")
    print("=" * 60)


if __name__ == "__main__":
    main()