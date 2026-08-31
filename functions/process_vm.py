# BUILD_MARKER: FOREMAN_VM_FOLDER_RESOLUTION_V3_20260830

from datetime import datetime, timedelta, timezone

import threading

import requests

from functions import dns, foreman, vars
from functions.shared import is_valid


VMWARE_FOLDER_CACHE_LOCK = threading.Lock()
VMWARE_FOLDER_CACHE = None


def _normalize_folder_path(
    value,
):
    """Normalize slashes without changing folder-name case or spaces."""
    if not is_valid(
        value
    ):
        return ""

    path = str(
        value
    ).strip().replace(
        "\\",
        "/",
    )

    while "//" in path:
        path = path.replace(
            "//",
            "/",
        )

    if len(
        path
    ) > 1:
        path = path.rstrip(
            "/"
        )

    return path


def _folder_relative_after_vm(
    value,
):
    """
    Return the part below a datacenter's VM root.

    Examples:
      /ISS/vm/A/B       -> A/B
      /Datacenters/ISS/vm/A/B -> A/B
      A/B               -> A/B
    """
    path = _normalize_folder_path(
        value
    )

    if not path:
        return ""

    lowered = path.lower()

    marker = "/vm/"

    marker_index = lowered.find(
        marker
    )

    if marker_index >= 0:
        return path[
            marker_index
            + len(
                marker
            ):
        ].strip(
            "/"
        )

    if lowered.endswith(
        "/vm"
    ):
        return ""

    return path.strip(
        "/"
    )


def _canonical_vm_folder_candidates(
    value,
):
    """
    Produce compatible vSphere/Fog folder-path variants.

    The Excel data can contain the path users naturally see in vSphere, e.g.:
        /ISS/vm/MTR-RTR Project/TVS/Python-Test

    Fog/Foreman commonly exposes the same inventory folder as:
        /Datacenters/ISS/vm/MTR-RTR Project/TVS/Python-Test

    Foreman itself can also expose a relative full_path. We therefore resolve
    against Foreman's own available_folders API rather than assuming one
    format.
    """
    raw = _normalize_folder_path(
        value
    )

    if not raw:
        return []

    candidates = []

    def add(
        candidate,
    ):
        normalized = _normalize_folder_path(
            candidate
        )

        if (
            normalized
            and normalized
            not in candidates
        ):
            candidates.append(
                normalized
            )

    add(
        raw
    )

    if not raw.startswith(
        "/"
    ):
        add(
            "/" + raw
        )

    lowered = raw.lower()

    # Excel/vSphere UI-style path:
    #   /ISS/vm/Folder/Subfolder
    # Convert to the canonical vSphere inventory path:
    #   /Datacenters/ISS/vm/Folder/Subfolder
    parts = [
        part
        for part in raw.strip(
            "/"
        ).split(
            "/"
        )
        if part
    ]

    if (
        len(
            parts
        ) >= 2
        and parts[
            0
        ].lower()
        != "datacenters"
        and parts[
            1
        ].lower()
        == "vm"
    ):
        add(
            "/Datacenters/{}".format(
                raw
                if raw.startswith("/")
                else "/" + raw
            )
        )

    # Already a full inventory path but missing the leading slash.
    if lowered.startswith(
        "datacenters/"
    ):
        add(
            "/" + raw
        )

    relative = _folder_relative_after_vm(
        raw
    )

    if relative:
        add(
            relative
        )
        add(
            "/" + relative
        )

    return candidates


def _foreman_available_vmware_folders():
    """
    Retrieve and cache the folders that Foreman can actually see through the
    configured VMware compute resource.

    This is deliberately done through Foreman, not directly against vCenter,
    so validation uses the exact same vSphere credentials/datacenter scope that
    Foreman will use during VM creation.
    """
    global VMWARE_FOLDER_CACHE

    with VMWARE_FOLDER_CACHE_LOCK:

        if VMWARE_FOLDER_CACHE is not None:
            return VMWARE_FOLDER_CACHE

        compute_id = get_compute_id()

        endpoint = (
            "{}/api/v2/compute_resources/{}/available_folders"
            .format(
                vars.FOREMAN_URL.rstrip(
                    "/"
                ),
                compute_id,
            )
        )

        folders = []
        page = 1

        while True:

            response = requests.get(
                endpoint,
                auth=(
                    vars.USER,
                    vars.PASSWORD,
                ),
                headers={
                    "Content-Type":
                        "application/json",

                    "Accept":
                        "application/json",
                },
                params={
                    "page":
                        page,

                    "per_page":
                        1000,
                },
                verify=vars.VERIFY_SSL,
                timeout=(
                    vars.HTTP_CONNECT_TIMEOUT,
                    vars.HTTP_READ_TIMEOUT,
                ),
            )

            if response.status_code != 200:
                raise RuntimeError(
                    "Unable to query VMware folders from Foreman "
                    "compute resource '{}'. HTTP {}: {}"
                    .format(
                        vars.COMPUTE_RESOURCE,
                        response.status_code,
                        response.text[:800],
                    )
                )

            try:
                data = response.json()
            except (
                TypeError,
                ValueError,
            ):
                raise RuntimeError(
                    "Foreman available_folders returned invalid JSON."
                )

            if not isinstance(
                data,
                dict,
            ):
                raise RuntimeError(
                    "Foreman available_folders returned an "
                    "unexpected JSON structure."
                )

            page_results = data.get(
                "results",
                [],
            )

            if not isinstance(
                page_results,
                list,
            ):
                raise RuntimeError(
                    "Foreman available_folders response does not "
                    "contain a results list."
                )

            folders.extend(
                page_results
            )

            total = data.get(
                "total"
            )

            if not page_results:
                break

            if (
                isinstance(
                    total,
                    int,
                )
                and len(
                    folders
                )
                >= total
            ):
                break

            # A short page is also an end-of-results indication.
            if len(
                page_results
            ) < 1000:
                break

            page += 1

        VMWARE_FOLDER_CACHE = folders

        print(
            "Foreman VMware folder inventory loaded: "
            "{} folder(s) visible through compute resource '{}'."
            .format(
                len(
                    folders
                ),
                vars.COMPUTE_RESOURCE,
            )
        )

        return VMWARE_FOLDER_CACHE


def _folder_result_paths(
    folder,
):
    """Return all path-like values exposed by Foreman's folder object."""
    values = []

    if not isinstance(
        folder,
        dict,
    ):
        return values

    for key in (
        "full_path",
        "path",
        "id",
    ):

        value = _normalize_folder_path(
            folder.get(
                key
            )
        )

        if (
            value
            and value not in values
        ):
            values.append(
                value
            )

    return values


def _folder_path_to_send(
    folder,
):
    """
    Prefer Foreman's full_path because it is the provider's actual inventory
    path. Fall back to path/id only for older Foreman/fog response formats.
    """
    if not isinstance(
        folder,
        dict,
    ):
        return ""

    for key in (
        "full_path",
        "path",
        "id",
    ):

        value = _normalize_folder_path(
            folder.get(
                key
            )
        )

        if value:
            return value

    return ""


def resolve_vmware_folder_path(
    excel_folder,
):
    """
    Resolve Excel vm_folder to a path Foreman/Fog has confirmed exists.

    Matching order:
      1. exact match against full_path/path/id
      2. match by path relative to the datacenter's /vm root
      3. unique leaf folder-name match

    An ambiguous leaf-name match fails rather than risking placement in the
    wrong VMware folder.
    """
    raw = _normalize_folder_path(
        excel_folder
    )

    if not raw:
        raise ValueError(
            "vm_folder is empty"
        )

    candidates = _canonical_vm_folder_candidates(
        raw
    )

    folders = _foreman_available_vmware_folders()

    normalized_candidates = {
        candidate.lower()
        for candidate in candidates
    }

    # ---------------------------------------------------------------
    # 1. Exact path/id match.
    # ---------------------------------------------------------------
    for folder in folders:

        for result_path in _folder_result_paths(
            folder
        ):

            if (
                result_path.lower()
                in normalized_candidates
            ):

                resolved = _folder_path_to_send(
                    folder
                )

                if resolved:
                    return (
                        resolved,
                        folder,
                    )

    # ---------------------------------------------------------------
    # 2. Match the relative path under the datacenter VM root.
    # ---------------------------------------------------------------
    requested_relative = (
        _folder_relative_after_vm(
            raw
        )
    )

    relative_matches = []

    if requested_relative:

        requested_relative_key = (
            requested_relative
            .strip(
                "/"
            )
            .lower()
        )

        for folder in folders:

            for result_path in _folder_result_paths(
                folder
            ):

                result_relative = (
                    _folder_relative_after_vm(
                        result_path
                    )
                )

                if (
                    result_relative
                    and result_relative
                    .strip(
                        "/"
                    )
                    .lower()
                    == requested_relative_key
                ):

                    relative_matches.append(
                        folder
                    )
                    break

    # De-duplicate by the provider path we would actually send.
    unique_relative = {}

    for folder in relative_matches:

        send_path = _folder_path_to_send(
            folder
        )

        if send_path:
            unique_relative[
                send_path.lower()
            ] = folder

    if len(
        unique_relative
    ) == 1:

        folder = list(
            unique_relative.values()
        )[0]

        return (
            _folder_path_to_send(
                folder
            ),
            folder,
        )

    if len(
        unique_relative
    ) > 1:

        raise ValueError(
            "vm_folder '{}' is ambiguous in Foreman. "
            "Multiple VMware folders match the relative path '{}': {}"
            .format(
                raw,
                requested_relative,
                ", ".join(
                    sorted(
                        _folder_path_to_send(
                            folder
                        )
                        for folder in unique_relative.values()
                    )
                ),
            )
        )

    # ---------------------------------------------------------------
    # 3. Last-resort unique leaf-name match.
    # ---------------------------------------------------------------
    leaf = raw.strip(
        "/"
    ).split(
        "/"
    )[-1]

    leaf_matches = [
        folder
        for folder in folders
        if str(
            folder.get(
                "name",
                "",
            )
        ).strip().lower()
        == leaf.lower()
    ]

    if len(
        leaf_matches
    ) == 1:

        folder = leaf_matches[
            0
        ]

        return (
            _folder_path_to_send(
                folder
            ),
            folder,
        )

    if len(
        leaf_matches
    ) > 1:

        raise ValueError(
            "vm_folder '{}' could not be matched by full path, "
            "and leaf folder '{}' is not unique. Matching folders: {}"
            .format(
                raw,
                leaf,
                ", ".join(
                    sorted(
                        _folder_path_to_send(
                            folder
                        )
                        for folder in leaf_matches
                    )
                ),
            )
        )

    canonical_hint = (
        candidates[
            1
        ]
        if len(
            candidates
        ) > 1
        else raw
    )

    raise ValueError(
        "VMware folder '{}' was not found through Foreman compute "
        "resource '{}'. Foreman can only create into folders visible "
        "through that compute resource. Candidate vSphere inventory "
        "path: '{}'."
        .format(
            raw,
            vars.COMPUTE_RESOURCE,
            canonical_hint,
        )
    )


def get_compute_id():
    return foreman.get_cached_resource_id(
        "api/v2/compute_resources",
        vars.COMPUTE_RESOURCE,
    )


def get_image_id(image_name):
    """Resolve the Foreman image/template configured on the VM Excel row."""
    if not is_valid(
        image_name
    ):
        raise ValueError(
            "VM image/template name is empty. Required Excel column: {}"
            .format(
                vars.VM_IMAGE_NAME_COLUMN
            )
        )

    compute_id = get_compute_id()

    return foreman.get_cached_resource_id(
        "api/v2/compute_resources/{}/images".format(
            compute_id
        ),
        str(
            image_name
        ).strip(),
    )


def get_ansible_job_id():
    return foreman.get_cached_resource_id(
        "api/v2/job_templates",
        vars.ANSIBLE_JOB_NAME,
    )


def sched_ansible_role(hostname, delay):
    """Schedule the configured Foreman Ansible job."""
    result = {
        "success": False,
        "hostname": hostname,
        "scheduled_time": None,
        "message": "",
    }

    try:
        start_time = (
            datetime.now(
                timezone.utc
            )
            + timedelta(
                seconds=int(
                    delay
                )
            )
        ).isoformat().replace(
            "+00:00",
            "Z",
        )

        result[
            "scheduled_time"
        ] = start_time

        payload = {
            "job_invocation": {
                "job_template_id": (
                    get_ansible_job_id()
                ),
                "target_hosts": hostname,
                "targeting_type": vars.ANSIBLE_TARGETING_TYPE,
                "search_query": (
                    "name = {}".format(
                        hostname
                    )
                ),
                "scheduling": {
                    "start_at": start_time
                },
                "description": (
                    "Scheduled Ansible run for {} "
                    "after provisioning".format(
                        hostname
                    )
                ),
                "concurrency_control": {
                    "concurrency_level": vars.ANSIBLE_CONCURRENCY_LEVEL
                },
            }
        }

        response = foreman.post_job_invocation(
            payload
        )

        if response.status_code == 201:
            message = (
                "Ansible job for {} successfully scheduled "
                "to run at {}".format(
                    hostname,
                    start_time,
                )
            )

            print(
                message
            )

            result.update({
                "success": True,
                "message": message,
            })

            return result

        message = (
            "Failed to schedule Ansible run job for {}. "
            "HTTP {}: {}".format(
                hostname,
                response.status_code,
                response.text,
            )
        )

        print(
            message
        )

        result[
            "message"
        ] = message

    except requests.exceptions.Timeout as error:
        result[
            "message"
        ] = (
            "Timeout while scheduling Ansible job for {}: {}"
            .format(
                hostname,
                error,
            )
        )

    except requests.exceptions.RequestException as error:
        result[
            "message"
        ] = (
            "HTTP/connection error while scheduling Ansible "
            "job for {}: {}".format(
                hostname,
                error,
            )
        )

    except Exception as error:
        result[
            "message"
        ] = (
            "Error scheduling Ansible run job for {}: {}"
            .format(
                hostname,
                error,
            )
        )

    print(
        result[
            "message"
        ]
    )

    return result


def create(vm):
    """Create/reuse a VM, process DNS and schedule Ansible."""
    hostname = str(
        vm.get(
            "logical_name",
            "UNKNOWN",
        )
    ).strip()

    short_name = hostname.split(
        ".",
        1,
    )[0]

    result = {
        "success": False,
        "status": "Failed",
        "details": "",
        "hostname": hostname,
        "foreman_success": False,
        "foreman_status": "Failed",
        "foreman_message": "",
        "dns_success": False,
        "dns_status": "Not Run",
        "dns_message": "",
        "ansible_success": False,
        "ansible_status": "Not Run",
        "ansible_message": "",
        "message": "",
    }

    try:
        existing = foreman.get_host(
            hostname,
            short_name,
        )

        already_exists = bool(
            existing
        )

        if already_exists:
            _set_existing_vm(
                result,
                hostname,
                existing,
            )

        else:
            payload = create_payload(
                vm
            )

            with foreman.host_creation_slot(
                hostname
            ):
                # Final existence check under the same creation lock.
                existing = foreman.get_host(
                    hostname,
                    short_name,
                )

                if existing:
                    already_exists = True

                    _set_existing_vm(
                        result,
                        hostname,
                        existing,
                    )

                else:
                    response = foreman.create_host(
                        payload
                    )

                    if response.status_code == 201:
                        try:
                            created = (
                                foreman.verify_created_managed_host(
                                    response=response,
                                    expected_names=(
                                        hostname,
                                        short_name,
                                    ),
                                    expected_organization_id=(
                                        payload["host"].get(
                                            "organization_id"
                                        )
                                    ),
                                    expected_location_id=(
                                        payload["host"].get(
                                            "location_id"
                                        )
                                    ),
                                )
                            )

                        except Exception as verify_error:
                            host_id = (
                                foreman.get_response_host_id(
                                    response
                                )
                            )

                            message = (
                                "CRITICAL: Foreman returned HTTP 201 "
                                "for VM {}, but POST-CREATE "
                                "VERIFICATION FAILED. Foreman host ID: "
                                "{}. Error: {}. DNS and Ansible will "
                                "NOT run. Check Foreman before rerunning "
                                "this VM because manual cleanup may be "
                                "required.".format(
                                    hostname,
                                    (
                                        host_id
                                        if host_id
                                        else "Unknown"
                                    ),
                                    verify_error,
                                )
                            )

                            print(
                                message
                            )

                            result.update({
                                "foreman_success": False,
                                "foreman_status": "Failed",
                                "foreman_message": message,
                                "message": message,
                                "details": message,
                            })

                            return result

                        foreman_message = (
                            foreman.describe_host(
                                created
                            )
                        )

                        result.update({
                            "foreman_success": True,
                            "foreman_status": "Successful",
                            "foreman_message": foreman_message,
                        })

                        print(
                            "Successfully created {} in Foreman."
                            .format(
                                hostname
                            )
                        )

                        print(
                            "POST-CREATE VERIFICATION PASSED: {}"
                            .format(
                                foreman_message
                            )
                        )

                    elif foreman.is_duplicate_host_response(
                        response
                    ):
                        existing = foreman.get_host(
                            hostname,
                            short_name,
                        )

                        if existing:
                            already_exists = True

                            _set_existing_vm(
                                result,
                                hostname,
                                existing,
                                duplicate_response=True,
                            )

                        else:
                            message = (
                                "Foreman returned duplicate-name HTTP "
                                "422 for VM {}, but an exact managed-host "
                                "lookup found no matching host. Treating "
                                "this as FAILED. This can indicate a "
                                "hidden/orphan Host::Base record. "
                                "Response: {}".format(
                                    hostname,
                                    response.text,
                                )
                            )

                            print(
                                message
                            )

                            result.update({
                                "message": message,
                                "details": message,
                            })

                            return result

                    else:
                        message = (
                            "Failed to create {}. HTTP {}: {}"
                            .format(
                                hostname,
                                response.status_code,
                                response.text,
                            )
                        )

                        print(
                            message
                        )

                        result.update({
                            "message": message,
                            "details": message,
                        })

                        return result

        # Foreman creation lock has been released here.
        _process_dns(
            vm,
            result,
        )

        if already_exists:
            result.update({
                "ansible_success": True,
                "ansible_status": "Skipped",
                "ansible_message": (
                    "VM already exists in Foreman; "
                    "Ansible not rescheduled"
                ),
            })

            print(
                "Skipping Ansible scheduling for existing "
                "VM {}.".format(
                    hostname
                )
            )

        else:
            ansible_result = (
                sched_ansible_role(
                    hostname,
                    vars.ANSIBLE_DELAY,
                )
            )

            result.update({
                "ansible_success": (
                    ansible_result[
                        "success"
                    ]
                ),
                "ansible_status": (
                    "Successful"
                    if ansible_result[
                        "success"
                    ]
                    else "Failed"
                ),
                "ansible_message": (
                    ansible_result[
                        "message"
                    ]
                ),
            })

        _finalize_result(
            result
        )

        return result

    except Exception as error:
        message = (
            "Error processing Foreman VM {}: {}"
            .format(
                hostname,
                error,
            )
        )

        print(
            message
        )

        result.update({
            "message": message,
            "details": message,
        })

        return result


def _set_existing_vm(
    result,
    hostname,
    existing,
    duplicate_response=False,
):
    """Mark an exact managed VM host as already existing."""
    foreman_message = (
        foreman.describe_host(
            existing
        )
    )

    result.update({
        "foreman_success": True,
        "foreman_status": "Already Exists",
        "foreman_message": foreman_message,
    })

    if duplicate_response:
        print(
            "Foreman returned duplicate-name HTTP 422 for {}, "
            "and exact VM verification succeeded: {}"
            .format(
                hostname,
                foreman_message,
            )
        )
    else:
        print(
            "Foreman VM {} already exists: {}"
            .format(
                hostname,
                foreman_message,
            )
        )


def _process_dns(vm, result):
    """Run DNS processing and update the VM result."""
    hostname = result[
        "hostname"
    ]

    try:
        dns_result = dns.create_dns_records(
            vm
        )

        dns_success = (
            dns_result.get(
                "status"
            ) == "Successful"
        )

        dns_message = dns_result.get(
            "details",
            "",
        )

        result.update({
            "dns_success": dns_success,
            "dns_status": dns_result.get(
                "status",
                "Failed",
            ),
            "dns_message": dns_message,
        })

        if dns_success:
            suffix = (
                ": {}".format(
                    dns_message
                )
                if dns_message
                else ""
            )

            print(
                "DNS creation completed for {}{}"
                .format(
                    hostname,
                    suffix,
                )
            )

        else:
            print(
                "WARNING: Foreman stage completed for {}, "
                "but DNS failed: {}".format(
                    hostname,
                    (
                        dns_message
                        or "Unknown DNS error"
                    ),
                )
            )

    except Exception as error:
        result.update({
            "dns_success": False,
            "dns_status": "Failed",
            "dns_message": str(
                error
            ),
        })

        print(
            "WARNING: Foreman stage completed for {}, but DNS "
            "raised an exception: {}".format(
                hostname,
                error,
            )
        )


def _finalize_result(result):
    """Set overall VM provisioning status."""
    foreman_text = result[
        "foreman_status"
    ]

    if result[
        "foreman_message"
    ]:
        foreman_text = "{} ({})".format(
            foreman_text,
            result[
                "foreman_message"
            ],
        )

    parts = [
        "Foreman: {}".format(
            foreman_text
        ),
        "DNS: {}".format(
            result[
                "dns_status"
            ]
        ),
        "Ansible: {}".format(
            result[
                "ansible_status"
            ]
        ),
    ]

    failures = []

    if (
        not result[
            "dns_success"
        ]
        and result[
            "dns_message"
        ]
    ):
        failures.append(
            "DNS Error: {}".format(
                result[
                    "dns_message"
                ]
            )
        )

    if (
        not result[
            "ansible_success"
        ]
        and result[
            "ansible_message"
        ]
    ):
        failures.append(
            "Ansible Error: {}".format(
                result[
                    "ansible_message"
                ]
            )
        )

    result[
        "success"
    ] = all((
        result[
            "foreman_success"
        ],
        result[
            "dns_success"
        ],
        result[
            "ansible_success"
        ],
    ))

    result[
        "status"
    ] = (
        "Successful"
        if result[
            "success"
        ]
        else "Partial"
    )

    details = "; ".join(
        parts + failures
    )

    result.update({
        "message": details,
        "details": details,
    })


def create_payload(vm):
    """Build a Foreman VMware VM payload from the selected Excel row."""
    hostname = vm.get(
        "logical_name",
        "UNKNOWN",
    )

    if not is_valid(
        vm.get(
            "logical_name"
        )
    ):
        raise ValueError(
            "Missing logical_name for VM"
        )

    image_name = vm.get(
        vars.VM_IMAGE_NAME_COLUMN
    )

    vm_folder = vm.get(
        vars.VM_FOLDER_COLUMN
    )

    if not is_valid(
        image_name
    ):
        raise ValueError(
            "VM {} is missing required {}."
            .format(
                hostname,
                vars.VM_IMAGE_NAME_COLUMN,
            )
        )

    if not is_valid(
        vm_folder
    ):
        raise ValueError(
            "VM {} is missing required {}."
            .format(
                hostname,
                vars.VM_FOLDER_COLUMN,
            )
        )

    (
        resolved_vm_folder,
        resolved_folder_info,
    ) = resolve_vmware_folder_path(
        vm_folder
    )

    if (
        _normalize_folder_path(
            vm_folder
        )
        != _normalize_folder_path(
            resolved_vm_folder
        )
    ):
        print(
            "VM {} VMware folder resolved: Excel='{}' -> Foreman='{}'"
            .format(
                hostname,
                _normalize_folder_path(
                    vm_folder
                ),
                resolved_vm_folder,
            )
        )
    else:
        print(
            "VM {} VMware folder verified through Foreman: '{}'"
            .format(
                hostname,
                resolved_vm_folder,
            )
        )

    hostgroup_name = (
        foreman.gethostgroup(
            vm[
                "subsystems"
            ],
            vm[
                "function"
            ],
            vm[
                "variation"
            ],
        )
    )

    if not is_valid(
        hostgroup_name
    ):
        raise ValueError(
            "No Foreman hostgroup mapping found for "
            "{} / {} / {}".format(
                vm[
                    "subsystems"
                ],
                vm[
                    "function"
                ],
                vm[
                    "variation"
                ],
            )
        )

    organization_id, location_id = (
        foreman.get_scope_ids()
    )

    compute_attributes = {
        "cpus": int(
            vm[
                "cpu"
            ]
        ),

        # Foreman VMware expects MB. Excel stores RAM in GB.
        "memory_mb": int(
            float(
                vm[
                    "ram_(gb)"
                ]
            )
            * 1024
        ),

        "start":
            vars.VM_START_ON_CREATE,

        # VMware destination folder belongs under compute_attributes.
        "path":
            resolved_vm_folder,

        "volumes_attributes":
            [],
    }

    payload = {
        "host": {
            "name":
                vm[
                    "logical_name"
                ],

            "hostgroup_id": (
                foreman.get_cached_resource_id(
                    "api/v2/hostgroups",
                    hostgroup_name,
                )
            ),

            "organization_id":
                organization_id,

            "location_id":
                location_id,

            "compute_resource_id": (
                get_compute_id()
            ),

            # Per-row Foreman image/template from os_template_name.
            "image_id": (
                get_image_id(
                    image_name
                )
            ),

            "provision_method":
                vars.VM_PROVISION_METHOD,

            "managed":
                True,

            "compute_attributes":
                compute_attributes,

            "interfaces_attributes":
                [],

            "host_parameters_attributes": (
                foreman.gethost_parameters(
                    vm.get(
                        "foreman_parameters",
                        vars.EMPTY_VALUE,
                    ),
                    vm[
                        "ntp1"
                    ],
                    vm[
                        "ntp2"
                    ],
                )
            ),
        }
    }

    print(
        "VM {} Foreman settings: image='{}'; folder='{}'; "
        "disk_type='{}'; cpu={}; ram_gb={}"
        .format(
            hostname,
            str(
                image_name
            ).strip(),
            resolved_vm_folder,
            str(
                vm.get(
                    vars.VM_DISK_TYPE_COLUMN,
                    "",
                )
            ).strip(),
            vm[
                "cpu"
            ],
            vm[
                "ram_(gb)"
            ],
        )
    )

    _add_interfaces(
        payload,
        vm,
    )

    _add_disks(
        payload,
        vm,
    )

    if not payload[
        "host"
    ][
        "compute_attributes"
    ][
        "volumes_attributes"
    ]:
        raise ValueError(
            "VM {} has no valid disks configured"
            .format(
                hostname
            )
        )

    return payload


def _vmware_disk_provisioning(
    value,
):
    """
    Convert Excel virtual_disk_type into Foreman VMware volume attributes.

    VMware volume creation uses thin/eager_zero rather than a generic
    storage_type field.
    """
    if not is_valid(
        value
    ):
        raise ValueError(
            "virtual_disk_type is empty"
        )

    normalized = str(
        value
    ).strip().lower()

    normalized = normalized.replace(
        "-",
        " ",
    ).replace(
        "_",
        " ",
    )

    normalized = " ".join(
        normalized.split()
    )

    thin_values = {
        "thin",
        "thin provision",
        "thin provisioned",
        "thin provisioning",
    }

    thick_lazy_values = {
        "thick",
        "thick lazy",
        "thick lazy zeroed",
        "lazy zeroed thick",
        "lazy zero thick",
    }

    thick_eager_values = {
        "thick eager",
        "thick eager zeroed",
        "eager zeroed thick",
        "eager zero thick",
    }

    if normalized in thin_values:
        return {
            "thin":
                "true",

            "eager_zero":
                "false",
        }

    if normalized in thick_lazy_values:
        return {
            "thin":
                "false",

            "eager_zero":
                "false",
        }

    if normalized in thick_eager_values:
        return {
            "thin":
                "false",

            "eager_zero":
                "true",
        }

    raise ValueError(
        "Unsupported virtual_disk_type '{}'. "
        "Use Thin, Thick/Thick Lazy Zeroed, or Thick Eager Zeroed."
        .format(
            value
        )
    )



def _add_interfaces(payload, vm):
    """Add VM network interfaces."""
    hostname = vm.get(
        "logical_name",
        "UNKNOWN",
    )

    has_fe = is_valid(
        vm.get(
            "fe_ip_address"
        )
    )

    has_me = is_valid(
        vm.get(
            "me_ip_address"
        )
    )

    if not has_fe:
        if has_me:
            raise ValueError(
                "VM {} has a MiddleEnd IP address ({}) but "
                "no FrontEnd IP address. MiddleEnd-only "
                "provisioning is not defined.".format(
                    hostname,
                    vm.get(
                        "me_ip_address"
                    ),
                )
            )

        raise ValueError(
            "VM {} has no valid FrontEnd or MiddleEnd "
            "IP address".format(
                hostname
            )
        )

    domain_id = (
        foreman.get_cached_resource_id(
            "api/domains",
            vm[
                "domain_name"
            ],
        )
    )

    fe_subnet_id = (
        foreman.get_cached_resource_id(
            "api/v2/subnets",
            vm[
                "fe_vlan_name"
            ],
        )
    )

    base_name = str(
        vm[
            "logical_name"
        ]
    ).replace(
        ".{}".format(
            vm[
                "domain_name"
            ]
        ),
        "",
    )

    if has_me:
        me_subnet_id = (
            foreman.get_cached_resource_id(
                "api/v2/subnets",
                vm[
                    "me_vlan_name"
                ],
            )
        )

        payload[
            "host"
        ][
            "interfaces_attributes"
        ].extend([
            {
                "primary": True,
                "provision": True,
                "managed": True,
                "name": base_name,
                "domain_id": domain_id,
                "subnet_id": me_subnet_id,
                "ip": vm[
                    "me_ip_address"
                ],
                "compute_attributes": {
                    "type": vars.VM_NETWORK_ADAPTER_TYPE,
                    "network": vm[
                        "me_vlan_name"
                    ],
                },
            },
            {
                "primary": False,
                "provision": False,
                "managed": True,
                "subnet_id": fe_subnet_id,
                "ip": vm[
                    "fe_ip_address"
                ],
                "compute_attributes": {
                    "type": vars.VM_NETWORK_ADAPTER_TYPE,
                    "network": vm[
                        "fe_vlan_name"
                    ],
                },
            },
        ])

    else:
        payload[
            "host"
        ][
            "interfaces_attributes"
        ].append({
            "primary": True,
            "provision": True,
            "managed": True,
            "name": base_name,
            "domain_id": domain_id,
            "subnet_id": fe_subnet_id,
            "ip": vm[
                "fe_ip_address"
            ],
            "compute_attributes": {
                "type": vars.VM_NETWORK_ADAPTER_TYPE,
                "network": vm[
                    "fe_vlan_name"
                ],
            },
        })


def _add_disks(payload, vm):
    """Add system and optional data disks using Excel virtual_disk_type."""
    hostname = vm.get(
        "logical_name",
        "UNKNOWN",
    )

    volumes = payload[
        "host"
    ][
        "compute_attributes"
    ][
        "volumes_attributes"
    ]

    disk_type = vm.get(
        vars.VM_DISK_TYPE_COLUMN
    )

    try:
        provisioning = (
            _vmware_disk_provisioning(
                disk_type
            )
        )

    except ValueError as exc:
        raise ValueError(
            "VM {}: {}"
            .format(
                hostname,
                exc,
            )
        )

    disk_specs = (
        (
            "storage1_disk_size_system",
            "storage1_datastore_system",
            "system",
        ),
        (
            "storage2_disk_size_data",
            "storage2_datastore_data",
            "data",
        ),
    )

    for (
        size_key,
        datastore_key,
        label,
    ) in disk_specs:

        if not is_valid(
            vm.get(
                size_key
            )
        ):
            continue

        if not is_valid(
            vm.get(
                datastore_key
            )
        ):
            raise ValueError(
                "VM {}: {} disk size is defined but "
                "{} is missing".format(
                    hostname,
                    label,
                    datastore_key,
                )
            )

        volumes.append({
            "size_gb": int(
                float(
                    vm[
                        size_key
                    ]
                )
            ),

            "datastore": str(
                vm[
                    datastore_key
                ]
            ).strip(),

            "thin":
                provisioning[
                    "thin"
                ],

            "eager_zero":
                provisioning[
                    "eager_zero"
                ],
        })

