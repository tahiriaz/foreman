# BUILD_MARKER: FOREMAN_SERIAL_CREATE_PXE_V2_20260830

from functions import dns, foreman, physical_boot, vars
from functions.shared import is_valid


NETWORKS = (
    ("fe", False),
    ("me", True),
    ("be", False),
    ("cl", False),
)


def create(host):
    """Create/reuse a physical Foreman host and then process DNS."""
    hostname = str(
        host.get(
            "hostname",
            "UNKNOWN",
        )
    ).strip()

    logical_name = host.get(
        "logical_name"
    )

    result = {
        "success": False,
        "status": "Failed",
        "details": "",
        "hostname": hostname,
        "foreman_success": False,
        "foreman_status": "Failed",
        "foreman_message": "",
        "foreman_created": False,
        "boot_required": False,
        "boot_success": True,
        "boot_status": "Not Run",
        "boot_message": "",
        "dns_success": False,
        "dns_status": "Not Run",
        "dns_message": "",
        "message": "",
    }

    try:
        # Fast existence check. Existing hosts do not need the creation lock.
        existing = foreman.get_host(
            hostname,
            logical_name,
        )

        if existing:
            _set_existing_host(
                result,
                hostname,
                existing,
            )

        else:
            # Payload construction/resource lookups can run concurrently.
            payload = create_payload(
                host
            )

            # Only the dangerous Foreman host creation transaction is serialized.
            with foreman.host_creation_slot(
                hostname
            ):
                # IMPORTANT:
                # Re-check after acquiring the slot in case another thread/run
                # created this object while this worker was waiting.
                existing = foreman.get_host(
                    hostname,
                    logical_name,
                )

                if existing:
                    _set_existing_host(
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
                                        logical_name,
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
                                "CRITICAL: Foreman returned HTTP 201 for {}, "
                                "but POST-CREATE VERIFICATION FAILED. "
                                "Foreman host ID: {}. Error: {}. "
                                "DNS will NOT run. Check Foreman before "
                                "rerunning this host because manual cleanup "
                                "may be required.".format(
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
                            "foreman_created": True,
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
                            logical_name,
                        )

                        if existing:
                            _set_existing_host(
                                result,
                                hostname,
                                existing,
                                duplicate_response=True,
                            )

                        else:
                            message = (
                                "Foreman returned duplicate-name HTTP 422 "
                                "for {}, but an exact managed-host lookup "
                                "found no matching host. Treating this as "
                                "FAILED. This can indicate a hidden/orphan "
                                "Foreman Host::Base record. Response: {}"
                                .format(
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

        # The Foreman creation slot has been released by this point.
        #
        # Only a host CREATED successfully in this run is prepared for PXE.
        # Exact hosts that already existed in Foreman are intentionally not
        # rebooted or modified.
        _process_physical_network_boot(
            host,
            result,
        )

        # DNS remains outside the serialized Foreman creation section, so DNS
        # and post-Foreman iLO/OA work remain parallel across host workers.
        _process_dns(
            host,
            result,
        )

        _finalize_result(
            result
        )

        return result

    except Exception as error:
        message = (
            "Error processing Foreman host {}: {}"
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


def _set_existing_host(
    result,
    hostname,
    existing,
    duplicate_response=False,
):
    """Mark an exact managed host as already existing."""
    foreman_message = foreman.describe_host(
        existing
    )

    result.update({
        "foreman_success": True,
        "foreman_status": "Already Exists",
        "foreman_message": foreman_message,
    })

    if duplicate_response:
        print(
            "Foreman returned duplicate-name HTTP 422 for {}, "
            "and exact managed-host verification succeeded: {}"
            .format(
                hostname,
                foreman_message,
            )
        )
    else:
        print(
            "Foreman host {} already exists: {}"
            .format(
                hostname,
                foreman_message,
            )
        )


def _process_physical_network_boot(
    host,
    result,
):
    """Configure PXE/Network next boot only for a newly-created Foreman host."""

    if not result.get(
        "foreman_created"
    ):

        result.update({
            "boot_required": False,
            "boot_success": True,
            "boot_status": "Not Run",
            "boot_message": (
                "Not run because Foreman host was not newly created "
                "in this execution"
            ),
        })

        return

    if not (
        vars.FOREMAN_PHYSICAL_NETWORK_BOOT_ENABLED
    ):

        result.update({
            "boot_required": False,
            "boot_success": True,
            "boot_status": "Disabled",
            "boot_message": (
                "Physical-host next-boot network/PXE "
                "configuration is disabled in vars.py"
            ),
        })

        print(
            "Physical PXE boot is disabled for {}."
            .format(
                result[
                    "hostname"
                ]
            )
        )

        return

    if not (
        physical_boot.is_supported_physical_host(
            host
        )
    ):

        result.update({
            "boot_required": False,
            "boot_success": True,
            "boot_status": "Skipped",
            "boot_message": (
                "Equipment type is not in the configured "
                "physical-host PXE type lists"
            ),
        })

        return

    result[
        "boot_required"
    ] = True

    try:

        boot_result = (
            physical_boot.configure_next_network_boot(
                host
            )
        )

        boot_success = bool(
            boot_result.get(
                "success"
            )
        )

        result.update({
            "boot_success": boot_success,
            "boot_status": boot_result.get(
                "status",
                (
                    "Successful"
                    if boot_success
                    else "Failed"
                ),
            ),
            "boot_message": boot_result.get(
                "details",
                "",
            ),
        })

        if boot_success:

            print(
                "Next boot configured for network/PXE on {}: {}"
                .format(
                    result[
                        "hostname"
                    ],
                    result[
                        "boot_message"
                    ],
                )
            )

        else:

            print(
                "WARNING: Foreman host {} was created, but "
                "next-boot network/PXE configuration failed: {}"
                .format(
                    result[
                        "hostname"
                    ],
                    result[
                        "boot_message"
                    ]
                    or "Unknown PXE error",
                )
            )

    except Exception as error:

        result.update({
            "boot_success": False,
            "boot_status": "Failed",
            "boot_message": str(
                error
            ),
        })

        print(
            "WARNING: Foreman host {} was created, but "
            "next-boot network/PXE raised an exception: {}"
            .format(
                result[
                    "hostname"
                ],
                error,
            )
        )


def _process_dns(host, result):
    """Run DNS processing and update the physical-host result."""
    hostname = result[
        "hostname"
    ]

    try:
        dns_result = dns.create_dns_records(
            host
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
                "WARNING: Foreman stage completed for {}, but "
                "DNS failed: {}".format(
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
    """Set final physical-host provisioning status."""

    foreman_text = (
        result[
            "foreman_status"
        ]
    )

    if result[
        "foreman_message"
    ]:

        foreman_text = "{} ({})".format(
            foreman_text,
            result[
                "foreman_message"
            ],
        )

    boot_text = (
        result.get(
            "boot_status",
            "Not Run",
        )
    )

    if result.get(
        "boot_message"
    ):

        boot_text = "{} ({})".format(
            boot_text,
            result[
                "boot_message"
            ],
        )

    dns_text = (
        result.get(
            "dns_status",
            "Not Run",
        )
    )

    if result.get(
        "dns_message"
    ):

        dns_text = "{} ({})".format(
            dns_text,
            result[
                "dns_message"
            ],
        )

    details = (
        "Foreman: {}; Boot: {}; DNS: {}"
        .format(
            foreman_text,
            boot_text,
            dns_text,
        )
    )

    failed_components = []

    if not result.get(
        "dns_success"
    ):

        failed_components.append(
            "DNS"
        )

    if (
        result.get(
            "boot_required"
        )
        and not result.get(
            "boot_success"
        )
    ):

        failed_components.append(
            "Boot"
        )

    if failed_components:

        result.update({
            "success": False,
            "status": "Partial",
            "message": details,
            "details": details,
        })

        return

    result.update({
        "success": True,
        "status": "Successful",
        "message": details,
        "details": details,
    })



def create_payload(host):
    """Build a Foreman payload for a physical server."""
    hostname = host.get(
        "hostname",
        "UNKNOWN",
    )

    if not is_valid(
        host.get(
            "hostname"
        )
    ):
        raise ValueError(
            "Missing hostname"
        )

    hostgroup_name = foreman.gethostgroup(
        host["subsystems"],
        host["function"],
        host["variation"],
    )

    if not is_valid(
        hostgroup_name
    ):
        raise ValueError(
            "No Foreman hostgroup mapping found for "
            "{} / {} / {}".format(
                host["subsystems"],
                host["function"],
                host["variation"],
            )
        )

    organization_id, location_id = (
        foreman.get_scope_ids()
    )

    payload = {
        "host": {
            "name": host[
                "hostname"
            ],
            "hostgroup_id": (
                foreman.get_cached_resource_id(
                    "api/v2/hostgroups",
                    hostgroup_name,
                )
            ),
            "organization_id": organization_id,
            "location_id": location_id,
            "build": True,
            "managed": True,
            "host_parameters_attributes": (
                foreman.gethost_parameters(
                    host[
                        "foreman_parameters"
                    ],
                    host.get(
                        "ntp1",
                        vars.EMPTY_VALUE,
                    ),
                    host.get(
                        "ntp2",
                        vars.EMPTY_VALUE,
                    ),
                )
            ),
            "interfaces_attributes": [],
        }
    }

    add_interfaces(
        payload,
        host,
    )

    if not payload[
        "host"
    ][
        "interfaces_attributes"
    ]:
        raise ValueError(
            "No valid network interfaces were generated "
            "for host {}".format(
                hostname
            )
        )

    return payload


def add_interfaces(payload, host):
    """Add physical, bond and VLAN interfaces."""
    interfaces = []

    domain_id = (
        foreman.get_cached_resource_id(
            "api/domains",
            vars.DOMAIN_NAME,
        )
    )

    for bond_index in range(
        3
    ):
        interfaces.extend(
            _build_bond(
                host,
                bond_index,
                domain_id,
            )
        )

    for prefix, primary in NETWORKS:
        vlan = _build_vlan(
            host,
            prefix,
            primary,
            domain_id,
        )

        if vlan:
            interfaces.append(
                vlan
            )

    payload[
        "host"
    ][
        "interfaces_attributes"
    ] = interfaces

    return payload


def _build_bond(host, bond_index, domain_id):
    """Build one bond plus its two physical interfaces."""
    nic_a_index = (
        bond_index * 2
    )
    nic_b_index = (
        nic_a_index + 1
    )

    nic_a_name = host.get(
        "nic{}_name".format(
            nic_a_index
        )
    )

    nic_b_name = host.get(
        "nic{}_name".format(
            nic_b_index
        )
    )

    bond_name = host.get(
        "bond{}_name".format(
            bond_index
        )
    )

    if not all((
        is_valid(
            nic_a_name
        ),
        is_valid(
            nic_b_name
        ),
        is_valid(
            bond_name
        ),
    )):
        return []

    nic_a = {
        "identifier": nic_a_name,
        "type": "interface",
        "mac": host[
            "nic{}_mac".format(
                nic_a_index
            )
        ],
        "managed": True,
        "primary": False,
    }

    nic_b = {
        "identifier": nic_b_name,
        "type": "interface",
        "mac": host[
            "nic{}_mac".format(
                nic_b_index
            )
        ],
        "managed": True,
        "primary": False,
    }

    if bond_index == 0:
        nic_a.update({
            "provision": True,
            "domain_id": domain_id,
            "subnet_id": (
                foreman.get_cached_resource_id(
                    "api/v2/subnets",
                    host[
                        "nic0_pxe_subnet_name"
                    ],
                )
            ),
        })

    bond = {
        "identifier": bond_name,
        "type": "bond",
        "mode": host[
            "bond{}_type".format(
                bond_index
            )
        ],
        "attached_devices": host[
            "bond{}_devs".format(
                bond_index
            )
        ],
        "managed": True,
        "primary": False,
    }

    for prefix, _ in NETWORKS:
        if (
            host.get(
                "{}_interface_type"
                .format(
                    prefix
                )
            ) == "bond"
            and host.get(
                "{}_attach_to".format(
                    prefix
                )
            ) == bond_name
        ):
            bond.update({
                "ip": host[
                    "{}_ip_address".format(
                        prefix
                    )
                ],
                "domain_id": domain_id,
                "subnet_id": (
                    foreman.get_cached_resource_id(
                        "api/v2/subnets",
                        host[
                            "{}_vlan_name"
                            .format(
                                prefix
                            )
                        ],
                    )
                ),
            })

    return [
        nic_a,
        nic_b,
        bond,
    ]


def _build_vlan(
    host,
    prefix,
    primary,
    domain_id,
):
    """Build a VLAN interface when VLAN mode is configured."""
    ip_key = (
        "{}_ip_address".format(
            prefix
        )
    )

    if (
        not is_valid(
            host.get(
                ip_key
            )
        )
        or host.get(
            "{}_interface_type"
            .format(
                prefix
            )
        ) != "vlan"
    ):
        return None

    return {
        "identifier": host[
            "{}_interface_name".format(
                prefix
            )
        ],
        "type": "interface",
        "tag": int(
            host[
                "{}_vlan_id".format(
                    prefix
                )
            ]
        ),
        "attached_to": host[
            "{}_attach_to".format(
                prefix
            )
        ],
        "ip": host[
            ip_key
        ],
        "subnet_id": (
            foreman.get_cached_resource_id(
                "api/v2/subnets",
                host[
                    "{}_vlan_name".format(
                        prefix
                    )
                ],
            )
        ),
        "domain_id": domain_id,
        "managed": True,
        "virtual": True,
        "primary": primary,
    }