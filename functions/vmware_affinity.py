# BUILD_MARKER: VMWARE_AFFINITY_V1_20260901

import ssl
import threading
import time

from functions import vars


_AFFINITY_LOCK = threading.Lock()


class AffinityGroupNotFound(Exception):
    """Raised when the requested vSphere VM DRS group does not exist."""


def _load_pyvmomi():
    """Load pyVmomi only when an affinity-enabled VM actually needs it."""
    try:
        from pyVim.connect import Disconnect, SmartConnect
        from pyVmomi import vim
    except ImportError as error:
        raise RuntimeError(
            "pyVmomi is required for affinity-group placement but is not "
            "installed. Install pyVmomi 7.0.3 for this Python 3.6 project. "
            "Original import error: {}".format(error)
        )

    return Disconnect, SmartConnect, vim


def _connect_vcenter(SmartConnect):
    """Connect to the configured vCenter."""
    ssl_context = (
        ssl.create_default_context()
        if vars.VMWARE_VERIFY_SSL
        else ssl._create_unverified_context()
    )

    return SmartConnect(
        host=vars.VMWARE_HOST,
        port=vars.VMWARE_PORT,
        user=vars.VMWARE_USERNAME,
        pwd=vars.VMWARE_PASSWORD,
        sslContext=ssl_context,
    )


def _wait_for_task(task, timeout_seconds):
    """Wait for a vSphere task to finish and raise on failure/timeout."""
    deadline = time.time() + int(timeout_seconds)

    while str(task.info.state).lower() in ("queued", "running"):
        if time.time() >= deadline:
            raise RuntimeError(
                "vCenter task timed out after {} seconds".format(
                    timeout_seconds
                )
            )
        time.sleep(1)

    if str(task.info.state).lower() == "success":
        return task.info.result

    error = task.info.error
    message = getattr(error, "msg", None) if error is not None else None
    raise RuntimeError(message or str(error) or "Unknown vCenter task error")


def _find_vm(content, vim, hostname):
    """Find a VM using either FQDN or short logical name."""
    expected_names = {
        str(hostname).strip().lower(),
        str(hostname).strip().split(".", 1)[0].lower(),
    }
    view = content.viewManager.CreateContainerView(
        content.rootFolder,
        [vim.VirtualMachine],
        True,
    )

    try:
        for vm_obj in view.view:
            if str(vm_obj.name).strip().lower() in expected_names:
                return vm_obj
    finally:
        view.Destroy()

    return None


def _wait_for_vm(content, vim, hostname):
    """Wait for the Foreman-created VM to become visible in vCenter."""
    deadline = time.time() + int(vars.VM_AFFINITY_VM_WAIT_SECONDS)

    while time.time() < deadline:
        vm_obj = _find_vm(content, vim, hostname)
        if vm_obj is not None:
            return vm_obj
        time.sleep(vars.VM_AFFINITY_POLL_SECONDS)

    raise RuntimeError(
        "VM '{}' did not appear in vCenter within {} seconds".format(
            hostname,
            vars.VM_AFFINITY_VM_WAIT_SECONDS,
        )
    )


def _get_vm_cluster(vm_obj, vim):
    """Return the ClusterComputeResource containing the VM."""
    resource_pool = getattr(vm_obj, "resourcePool", None)

    while resource_pool is not None:
        owner = getattr(resource_pool, "owner", None)
        if isinstance(owner, vim.ClusterComputeResource):
            return owner
        resource_pool = getattr(resource_pool, "parent", None)

    runtime_host = getattr(getattr(vm_obj, "runtime", None), "host", None)
    parent = getattr(runtime_host, "parent", None) if runtime_host else None

    if isinstance(parent, vim.ClusterComputeResource):
        return parent

    raise RuntimeError(
        "Unable to determine the vSphere cluster for VM '{}'".format(
            vm_obj.name
        )
    )


def _find_vm_group(cluster, vim, group_name):
    """Find one existing VM DRS group by exact name."""
    groups = getattr(cluster.configurationEx, "group", None) or []

    for group in groups:
        if isinstance(group, vim.cluster.VmGroup) and group.name == group_name:
            return group

    return None


def _is_group_member(group, vm_obj):
    """Return True when the VM already belongs to the group."""
    vm_moid = vm_obj._moId

    return any(
        member._moId == vm_moid
        for member in (getattr(group, "vm", None) or [])
    )


def _add_vm_to_group(cluster, vim, vm_obj, group):
    """Add a VM to an existing DRS VM group and verify membership."""
    members = list(getattr(group, "vm", None) or [])

    if any(member._moId == vm_obj._moId for member in members):
        return

    members.append(vm_obj)

    updated_group = vim.cluster.VmGroup(
        name=group.name,
        vm=members,
    )
    group_spec = vim.cluster.GroupSpec(
        operation="edit",
        info=updated_group,
    )
    cluster_spec = vim.cluster.ConfigSpecEx(
        groupSpec=[group_spec],
    )

    task = cluster.ReconfigureComputeResource_Task(
        spec=cluster_spec,
        modify=True,
    )
    _wait_for_task(task, vars.VM_AFFINITY_TASK_TIMEOUT_SECONDS)


def assign_vm_to_group(hostname, group_name):
    """
    Add a newly-created VM to an existing vSphere VM DRS group.

    This function never prevents the caller from powering on the VM. Any
    vCenter/pyVmomi/group error is returned as Warning so process_vm.py can
    start the VM anyway and expose the warning in the final report.
    """
    result = {
        "success": False,
        "status": "Warning",
        "hostname": hostname,
        "group": group_name,
        "cluster": "",
        "message": "",
    }
    service_instance = None
    Disconnect = None

    try:
        Disconnect, SmartConnect, vim = _load_pyvmomi()
        service_instance = _connect_vcenter(SmartConnect)
        content = service_instance.RetrieveContent()
        vm_obj = _wait_for_vm(content, vim, hostname)
        cluster = _get_vm_cluster(vm_obj, vim)
        result["cluster"] = cluster.name

        # Cluster-group edits are read/modify/write operations. Serialize them
        # within this provisioning process so parallel VM workers cannot lose
        # each other's membership updates.
        with _AFFINITY_LOCK:
            group = _find_vm_group(cluster, vim, group_name)

            if group is None:
                raise AffinityGroupNotFound(
                    "Affinity group '{}' does not exist in vSphere cluster "
                    "'{}'".format(group_name, cluster.name)
                )

            if _is_group_member(group, vm_obj):
                result.update({
                    "success": True,
                    "status": "Successful",
                    "message": (
                        "VM '{}' is already a member of affinity group '{}' "
                        "in cluster '{}'".format(
                            vm_obj.name,
                            group.name,
                            cluster.name,
                        )
                    ),
                })
                return result

            _add_vm_to_group(cluster, vim, vm_obj, group)

            refreshed_group = _find_vm_group(cluster, vim, group_name)
            if (
                refreshed_group is None
                or not _is_group_member(refreshed_group, vm_obj)
            ):
                raise RuntimeError(
                    "vCenter accepted the affinity-group update but VM '{}' "
                    "could not be verified in group '{}'".format(
                        vm_obj.name,
                        group_name,
                    )
                )

        result.update({
            "success": True,
            "status": "Successful",
            "message": (
                "VM '{}' added to affinity group '{}' in cluster '{}'".format(
                    vm_obj.name,
                    group_name,
                    cluster.name,
                )
            ),
        })
        return result

    except AffinityGroupNotFound as error:
        result["message"] = str(error)
        return result
    except Exception as error:
        result["message"] = (
            "Unable to place VM '{}' in affinity group '{}': {}".format(
                hostname,
                group_name,
                error,
            )
        )
        return result
    finally:
        if service_instance is not None and Disconnect is not None:
            try:
                Disconnect(service_instance)
            except Exception:
                pass
