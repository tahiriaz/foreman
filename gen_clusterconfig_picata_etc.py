"""Generate cluster configurations with the NAS-backed ``/etc/picata`` mount.

This variant reuses all inventory handling and configuration settings from
``gen_clusterconfig.py``.  For every VIP resource group it adds:

    {NAS_BASEDIR}{cluster}/{resource-group}/etc/picata -> /etc/picata

It also avoids PCS resource-set ordering syntax (``then set ...``), which is
not supported by older PCS releases.  Equivalent individual start-order
constraints are generated instead.
"""

import sys
import re

import gen_clusterconfig as base_generator

from functions import vars
from functions.output_log import run_logged_main


BASE_BUILD_CLUSTER_CONTENTS = base_generator.build_cluster_contents
NODE_RESOURCE_COUNT = vars.CLUSTER_RESOURCE_COUNT + 1
FENCE_PRIVILEGE = "operator"


def to_fqdn(hostname):
    """Return a normalized FQDN, retaining an already qualified hostname."""
    if base_generator.is_missing(hostname):
        return hostname

    normalized_hostname = str(hostname).strip().rstrip(".")

    if "." in normalized_hostname:
        return normalized_hostname

    return "{}.{}".format(
        normalized_hostname,
        vars.DOMAIN_NAME,
    )


def build_cluster_contents(
    cluster_name,
    group,
    vip_dataframe,
    scope_config,
):
    """Build the standard configuration with FQDN nodes and the etc mount."""
    fqdn_group = group.copy()

    for hostname_column in (
        "logical_name",
        "hostname",
    ):
        fqdn_group[hostname_column] = fqdn_group[hostname_column].apply(
            to_fqdn
        )

    before_content, after_content = BASE_BUILD_CLUSTER_CONTENTS(
        cluster_name,
        fqdn_group,
        vip_dataframe,
        scope_config,
    )

    # The hpilofence iLO account is configured with the Operator role.  The
    # fence_ilo4 resource must use the matching protocol privilege level.
    before_content = before_content.replace(
        " pcmk_host_list=",
        " privlvl={} pcmk_host_list=".format(
            FENCE_PRIVILEGE,
        ),
    )

    # A complete resource group now consumes one additional resource slot.
    before_content = before_content.replace(
        "rcount={}".format(
            vars.CLUSTER_RESOURCE_COUNT,
        ),
        "rcount={}".format(
            NODE_RESOURCE_COUNT,
        ),
    )

    cluster_path = cluster_name.lower()
    nas_basedir = scope_config["NAS_BASEDIR"]

    # Each core resource group receives its own NAS-backed Picata config
    # directory.  Place it immediately after the data mount in group order.
    data_mount = (
        "pcs resource create {alias}-nfsdat01 "
        "ocf:heartbeat:Filesystem "
        "device='{nas_basedir}{cluster}/{alias}/data' "
        "directory='/data' fstype='nfs' "
        'options="rw,nfsvers=3,tcp,hard,rsize=1048576,wsize=1048576,'
        'noatime,nodiratime,nconnect=8,nolock" '
        "--group rg-{alias}-core op monitor interval=60s"
    )
    etc_mount = (
        "pcs resource create {alias}-nfsetc01 "
        "ocf:heartbeat:Filesystem "
        "device='{nas_basedir}{cluster}/{alias}/etc/picata' "
        "directory='/etc/picata' fstype='nfs' "
        'options="rw,nfsvers=3,tcp,hard,rsize=1048576,wsize=1048576,'
        'noatime,nodiratime,nconnect=8,nolock" '
        "--group rg-{alias}-core op monitor interval=60s"
    )

    for alias in _cluster_aliases(cluster_name, scope_config):
        formatted_data_mount = data_mount.format(
            alias=alias,
            nas_basedir=nas_basedir,
            cluster=cluster_path,
        )
        formatted_etc_mount = etc_mount.format(
            alias=alias,
            nas_basedir=nas_basedir,
            cluster=cluster_path,
        )

        if formatted_data_mount not in before_content:
            # The base generator omitted this alias because no matching VIP
            # exists in the workbook, so there is no resource group to alter.
            continue

        before_content = before_content.replace(
            formatted_data_mount,
            "{}\n{}".format(
                formatted_data_mount,
                formatted_etc_mount,
            ),
            1,
        )
        before_content = before_content.replace(
            "pcs resource utilization rg-{}-core rcount=3".format(alias),
            "pcs resource utilization rg-{}-core rcount=4".format(alias),
            1,
        )

        # Older PCS versions do not accept the resource-set form
        # "then set ... sequential=false".  Separate order constraints keep
        # the same dependency while allowing dependent resources to start in
        # parallel once the core group is active.
        storage_set_constraint = (
            "pcs constraint order start rg-{alias}-core then set "
            "{alias}-nfsrec01 {alias}-nfsrec02 {alias}-nfsrec03 "
            "{alias}-nfsrec04 sequential=false"
        ).format(alias=alias)
        storage_constraints = "\n".join(
            "pcs constraint order start rg-{alias}-core then start {alias}-{resource}".format(
                alias=alias,
                resource=resource,
            )
            for resource in (
                "nfsrec01",
                "nfsrec02",
                "nfsrec03",
                "nfsrec04",
            )
        )
        before_content = before_content.replace(
            storage_set_constraint,
            storage_constraints,
            1,
        )

        application_set_constraint = (
            "pcs constraint order start rg-{alias}-core then set "
            "{alias}-pctcfg-updater {alias}-picata01 {alias}-picata02 "
            "{alias}-picata03 {alias}-picata04 sequential=false"
        ).format(alias=alias)
        application_constraints = "\n".join(
            "pcs constraint order start rg-{alias}-core then start {alias}-{resource}".format(
                alias=alias,
                resource=resource,
            )
            for resource in (
                "pctcfg-updater",
                "picata01",
                "picata02",
                "picata03",
                "picata04",
            )
        )
        configuration_order_constraints = "\n".join(
            "pcs constraint order start {alias}-pctcfg-updater then start {alias}-{resource}".format(
                alias=alias,
                resource=resource,
            )
            for resource in (
                "picata01",
                "picata02",
                "picata03",
                "picata04",
            )
        )
        after_content = after_content.replace(
            application_set_constraint,
            "{}\n{}".format(
                application_constraints,
                configuration_order_constraints,
            ),
            1,
        )

    return before_content, after_content


def _cluster_aliases(cluster_name, scope_config):
    """Return the VIP aliases that the base generator can create."""
    cluster_index = int(
        re.search(
            r"\d+",
            cluster_name,
        ).group()
    )
    return [
        "{}{:03d}".format(
            scope_config["CLUSTER_PREFIX"],
            cluster_index + offset,
        )
        for offset in range(
            1,
            vars.CLUSTER_VIP_COUNT_PER_CLUSTER + 1,
        )
    ]


def main():
    """Run the standard generator with this variant's content builder."""
    base_generator.build_cluster_contents = build_cluster_contents
    return base_generator.main()


if __name__ == "__main__":
    sys.exit(
        run_logged_main(
            main,
            log_prefix=vars.SCRIPT_ARTIFACT_PREFIXES["gen_clusterconfig"],
            title="CLUSTER COMMAND GENERATOR WITH PICATA ETC MOUNT",
        )
    )
