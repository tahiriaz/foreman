# BUILD_MARKER: CENTRAL_PROJECT_CONFIG_V18_VM_CREATE_EXCEL_FIELDS_20260830

import os


# ============================================================================
# PROJECT PATHS
# ============================================================================

# vars.py lives under <project>\functions\vars.py.
FUNCTIONS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(FUNCTIONS_DIR)
TEMPLATES_DIR = os.path.join(PROJECT_DIR, "Templates")
SCRIPTS_DIR = os.path.join(PROJECT_DIR, "scripts")
LOG_DIR = os.path.join(PROJECT_DIR, "logs")


# ============================================================================
# EXCEL / INVENTORY - SHARED
# ============================================================================

# Workbook and sheet are shared by Foreman provisioning and iLO automation.
EXCEL_FILENAME = 'Resource List-v7.6.xlsx'
RESOURCE_LIST = os.path.join(TEMPLATES_DIR, EXCEL_FILENAME)
SHEET_NAME = 'General Resource List'

EXCEL_ENGINE = 'openpyxl'
EMPTY_VALUE = 'NODATAFOUND'

# Stop optimized workbook scans after this many consecutive empty rows.
EXCEL_EMPTY_ROW_STOP = 25

# Values treated as empty/invalid throughout inventory and provisioning logic.
INVALID_VALUES = {'', 'N.A', 'NAN', 'NONE', 'NODATAFOUND'}


# ============================================================================
# GLOBAL EXCEL RANGE / GENERAL EXECUTION
# ============================================================================

# Inclusive Excel row range shared by all scripts that process the resource list:
# Foreman provisioning, rack-mount iLO, blade iLO, RAID, and future automation.
START_ROW = 928
END_ROW = 951

# Overall Foreman/DNS orchestration worker pool.
MAX_WORKERS = 8
LOG_FILE_PREFIX = 'provisioning'

# Common file prefixes for console logs and standardized summary CSVs.
# Root scripts use these names so logging/report artifacts remain predictable.
SCRIPT_ARTIFACT_PREFIXES = {
    'create_foreman_host': 'Foreman_Host',
    'configure_ilo_RM': 'ILO_RM',
    'configure_ilo_BL': 'ILO_BL',
    'configure_raid_RM': 'RAID_RM',
    'configure_raid_BL': 'RAID_BL',
    'create_dns_records': 'DNS',
    'gen_oaconfig': 'OA_Config',
    'gen_clusterconfig': 'Cluster_Config',
    'get_mac_RM': 'MAC_RM',
    'get_mac_BL': 'MAC_BL',
    'check_vmware_vms': 'VMware_VM_Check',
}


# ============================================================================
# FOREMAN
# ============================================================================

FOREMAN_URL = 'https://idsfrk02.mak.iss'
USER = 'localadmin'
PASSWORD = 'Th@les01'

DOMAIN_NAME = 'mak.iss'
ORG_NAME = 'Thales KSA'
LOCATION_NAME = 'Shamiyah Project'

VERIFY_SSL = True

# requests timeout = (connection timeout, response/read timeout)
HTTP_CONNECT_TIMEOUT = 10
HTTP_READ_TIMEOUT = 120
RESOURCE_LOOKUP_TIMEOUT = 10

# Post-create verification through /api/hosts/<id>.
FOREMAN_VERIFY_ATTEMPTS = 5
FOREMAN_VERIFY_DELAY = 1

# IMPORTANT:
# Parallel POST /api/hosts requests on this Foreman installation have been
# observed to occasionally create malformed Host::Base records with type=nil.
# Keep host creation serialized unless the Foreman-side issue is resolved.
FOREMAN_CREATE_CONCURRENCY = 1
FOREMAN_CREATE_SETTLE_SECONDS = 1


# ============================================================================
# FOREMAN - PHYSICAL HOST NEXT-BOOT NETWORK / PXE
# ============================================================================

# When True, a newly-created physical Foreman host is configured for one-time
# network/PXE boot immediately after Foreman POST-create verification succeeds,
# and the server is started/rebooted immediately so PXE installation begins
# automatically.
#
# Existing Foreman hosts are NOT modified by this workflow.  The PXE action is
# only triggered for a host that was newly created in the current run.
FOREMAN_PHYSICAL_NETWORK_BOOT_ENABLED = True

# Physical equipment types handled by the post-Foreman boot workflow.
FOREMAN_PHYSICAL_NETWORK_BOOT_RACK_TYPES = ['NVR', 'VCA', 'ESXi']
FOREMAN_PHYSICAL_NETWORK_BOOT_BLADE_TYPES = [
    'NVR Blade Server',
    'VCA Blade Server',
]

# Direct iLO Redfish behavior.
FOREMAN_PHYSICAL_NETWORK_BOOT_VERIFY_ILO_SSL = False
FOREMAN_PHYSICAL_NETWORK_BOOT_CONNECT_TIMEOUT_SECONDS = 10
FOREMAN_PHYSICAL_NETWORK_BOOT_REQUEST_TIMEOUT_SECONDS = 20

# Direct iLO transport handling.
# RemoteDisconnected/ConnectionReset is retried and is NOT by itself treated
# as "iLO unreachable". Blade OA fallback is allowed only when TCP/443 cannot
# be reached after these checks.
FOREMAN_PHYSICAL_NETWORK_BOOT_ILO_REQUEST_RETRIES = 3
FOREMAN_PHYSICAL_NETWORK_BOOT_ILO_RETRY_DELAY_SECONDS = 2
FOREMAN_PHYSICAL_NETWORK_BOOT_ILO_TCP_PROBE_TIMEOUT_SECONDS = 3
FOREMAN_PHYSICAL_NETWORK_BOOT_ILO_TCP_PROBE_RETRIES = 2

FOREMAN_PHYSICAL_NETWORK_BOOT_POWER_OFF_TIMEOUT_SECONDS = 90
FOREMAN_PHYSICAL_NETWORK_BOOT_POLL_INTERVAL_SECONDS = 5
FOREMAN_PHYSICAL_NETWORK_BOOT_POST_ERROR_STRING = (
    'UnableToModifyDuringSystemPOST'
)

# Python 3.6 is intentionally retained for this project. Paramiko imports
# cryptography, whose installed version emits deprecation warnings simply
# because the interpreter is Python 3.6. physical_boot.py now imports Paramiko
# lazily only when OA fallback is actually needed and suppresses only these
# known cryptography deprecation messages during that import.
FOREMAN_PHYSICAL_NETWORK_BOOT_SUPPRESS_CRYPTO_DEPRECATION_WARNINGS = True

# Blade fallback through the ACTIVE Onboard Administrator.
# OA lookup scans the COMPLETE worksheet because OA rows can be outside the
# Foreman START_ROW / END_ROW range.
FOREMAN_PHYSICAL_NETWORK_BOOT_OA_SSH_PORT = 22
FOREMAN_PHYSICAL_NETWORK_BOOT_OA_CONNECT_TIMEOUT_SECONDS = 15
FOREMAN_PHYSICAL_NETWORK_BOOT_OA_KEEPALIVE_SECONDS = 5
FOREMAN_PHYSICAL_NETWORK_BOOT_OA_COMMAND_TIMEOUT_SECONDS = 120
FOREMAN_PHYSICAL_NETWORK_BOOT_OA_QUIET_SECONDS = 5
FOREMAN_PHYSICAL_NETWORK_BOOT_OA_LINE_DELAY_SECONDS = 0.02

# Keep the overall Foreman worker pool parallel, but serialize HPONCFG work
# for blades belonging to the same enclosure when OA fallback is necessary.
FOREMAN_PHYSICAL_NETWORK_BOOT_OA_SERIALIZE_PER_ENCLOSURE = True
FOREMAN_PHYSICAL_NETWORK_BOOT_OA_RIBCL_RETRIES = 3
FOREMAN_PHYSICAL_NETWORK_BOOT_OA_RIBCL_RETRY_DELAY_SECONDS = 2


# ============================================================================
# NETWORK / FOREMAN RESOURCES
# ============================================================================

SUBNET_FE = 'mtr_tvs_nvr_fe'
SUBNET_BE = 'mtr_tvs_nvr_be'
SUBNET_ME = 'mtr_tvs_nvr_me'

MTR_PXE_SUBNET = 'mtr_nvr_pxe'
RTR_PXE_SUBNET = 'rtr_nvr_pxe'


# ============================================================================
# VMWARE / VCENTER INVENTORY CHECK
# ============================================================================

# vCenter used by check_vmware_vms.py.
VMWARE_HOST = 'infvirvcr01sf.mak.iss'
VMWARE_PORT = 443
VMWARE_USERNAME = 'Administrator@vsphere.local'
VMWARE_PASSWORD = 'Th@les01'

# Set True only when the vCenter certificate chain/name is trusted by the
# machine running the script.
VMWARE_VERIFY_SSL = False

# requests timeout = (connection timeout, response/read timeout)
VMWARE_CONNECT_TIMEOUT_SECONDS = 10
VMWARE_READ_TIMEOUT_SECONDS = 60

# Retry transient vCenter REST transport/server errors.
VMWARE_HTTP_RETRIES = 3
VMWARE_HTTP_RETRY_DELAY_SECONDS = 2

# Excel selection for this check. The script still uses shared RESOURCE_LIST,
# SHEET_NAME, EXCEL_ENGINE, START_ROW, END_ROW, EMPTY_VALUE and INVALID_VALUES.
VMWARE_EQUIPMENT_TYPE = 'Virtual Machine'
VMWARE_REQUIRED_COLUMNS = [
    'equipment_type',
    'hostname',
    'logical_name',
    'fe_ip_address',
    'me_ip_address',
]

# fe_ip_address must contain a valid IP for every Virtual Machine row.
# me_ip_address may be empty; when populated it must also be a valid IP.
VMWARE_FE_IP_REQUIRED = True

# Row checks are local after one vCenter inventory download, but they retain
# the project parallel-worker pattern.
VMWARE_CHECK_MAX_WORKERS = MAX_WORKERS

# Guest-IP discovery is performed in parallel against vCenter. VMware Tools
# must provide guest networking data for vCenter to report guest IP addresses.
VMWARE_IP_LOOKUP_MAX_WORKERS = MAX_WORKERS

# When True, a row with no detected IP conflict is reported Partial instead of
# Successful if one or more existing VMs could not be inspected for guest IPs.
# This prevents a false "IP is free" result when VMware Tools data is missing.
VMWARE_REQUIRE_COMPLETE_IP_INVENTORY = False

# Standard console-log / summary-CSV prefix.
VMWARE_REPORT_PREFIX = 'VMware_VM_Check'


# ============================================================================
# VMWARE / VM PROVISIONING
# ============================================================================

HOSTGROUP_NAME = 'TVS_VMs'
COMPUTE_RESOURCE = 'ISS vDC'

# VM creation resolves the image, destination folder and disk provisioning type
# from each Virtual Machine Excel row. These two legacy variables are retained
# only for compatibility with older external scripts; process_vm.py no longer
# uses them when creating a VM.
IMAGE_NAME = 'RHEL 8.10'
VSTORAGE_TYPE = 'thin'

VM_IMAGE_NAME_COLUMN = 'os_template_name'
VM_FOLDER_COLUMN = 'vm_folder'
VM_DISK_TYPE_COLUMN = 'virtual_disk_type'

# Exact required data fields for equipment_type='Virtual Machine'.
# equipment_type itself remains the resource selector used by inventory.py.
VM_CREATION_REQUIRED_COLUMNS = [
    'project',
    'subsystems',
    'function',
    'variation',
    'hostname',
    'logical_name',
    'vm_folder',
    'cpu',
    'ram_(gb)',
    'storage1_datastore_system',
    'storage1_disk_size_system',
    'storage2_datastore_data',
    'storage2_disk_size_data',
    'virtual_disk_type',
    'domain_name',
    'fe_vlan_name',
    'fe_ip_address',
    'os_template_name',
    'ntp1',
    'ntp2',
]

VM_PROVISION_METHOD = 'image'
VM_NETWORK_ADAPTER_TYPE = 'VirtualVmxnet3'
VM_START_ON_CREATE = '1'


# ============================================================================
# ANSIBLE
# ============================================================================

ANSIBLE_JOB_NAME = 'Ansible Roles - Ansible Default'
ANSIBLE_DELAY = 360
ANSIBLE_TARGETING_TYPE = 'static_query'
ANSIBLE_CONCURRENCY_LEVEL = 1


# ============================================================================
# DNS
# ============================================================================

DNS_SERVER = '10.130.2.11'
DNS_SERVER_USER = 'MAK.ISS\\Administrator'
DNS_SERVER_PASS = 'Th@les01'

POWERSHELL_EXECUTABLE = 'powershell.exe'
DNS_SCRIPT_FILENAME = 'add_dns_records.ps1'
DNS_SCRIPT = os.path.join(SCRIPTS_DIR, DNS_SCRIPT_FILENAME)
DNS_TEMP_DIR_NAME = 'foreman_dns'

# Standalone DNS creation uses the global MAX_WORKERS, RESOURCE_LIST,
# SHEET_NAME, START_ROW, END_ROW, EXCEL_EMPTY_ROW_STOP and LOG_DIR.
DNS_REPORT_PREFIX = 'DNS_Report'

# Retained for compatibility with existing code.
DNS_DIR = SCRIPTS_DIR
DNS_FILENAME = 'dns_vm.csv'


# ============================================================================
# iLO - SHARED CREDENTIALS / LICENSING / FENCING
# ============================================================================

# Rack-mount and blade iLO credentials are intentionally separate because the
# supplied scripts use different local administrator accounts.
ILO_RM_USERNAME = 'Administrator'
ILO_RM_PASSWORD = 'Th@les01'

OA_USERNAME = 'Administrator'
OA_PASSWORD = 'Th@les01'

ILO_BL_USERNAME = 'thlocaladmin'
ILO_BL_PASSWORD = 'Th@les018664'

ILO_ADVANCED_LICENSE_KEY = '35SCR-RYLML-CBK7N-TD3B9-GGBW2'

FENCE_USER_NAME = 'Pacemaker Fence'
FENCE_USER_LOGIN = 'hpilofence'
FENCE_USER_PASSWORD = 'Th@les01'


# ============================================================================
# iLO - SHARED NETWORK / LDAP / TIMEZONE
# ============================================================================

ILO_DOMAIN = 'mak.iss'
ILO_IPMI_PORT = 623
ILO_REDFISH_PORT = 443
ILO_TIMEZONE_SEARCH = 'Riyadh'

LDAP_PORT = 636
LDAP_GROUP_NAME = 'CN=ILOAdmins,OU=Roles,OU=IT,OU=ISS,DC=mak,DC=iss'
LDAP_GROUP_SID = ''
LDAP_GROUP_PRIVILEGES = '1,2,3,4,5,6'
LDAP_USER_CONTEXTS = ['OU=IT,OU=ISS,DC=mak,DC=iss',
 'CN=Users,DC=mak,DC=iss',
 'CN=Builtin,DC=mak,DC=iss',
 '@mak.iss']

# Shared site/scope settings used by rack-mount and blade iLO automation.
# RM and BL intentionally use the same DIRECTORY_SERVER for each scope.
ILO_SCOPE_SETTINGS = {
    "SIL": {
        "GATEWAY": '10.101.18.1',
        "SUBNET_MASK": '255.255.254.0',
        "PRIMARY_DNS": '10.130.2.11',
        "SECONDARY_DNS": '10.130.2.12',
        "PRIMARY_NTP": '10.101.18.1',
        "SECONDARY_NTP": '10.130.2.11',
        "DIRECTORY_SERVER": 'INFCOSADU001MP.mak.iss',
        "NAS_BASEDIR":
            'ssip.mtr-rec.infstonas001mp.mak.iss:'
            '/ifs/infstonas001mp/mtr-rec/',
        "VIP_NIC": 'vlan126',
        "VIP_MASK": 23,
        "CLUSTER_PREFIX": 'clnvrs',
    },
    "MTR": {
        "GATEWAY": '10.101.18.1',
        "SUBNET_MASK": '255.255.254.0',
        "PRIMARY_DNS": '10.130.2.11',
        "SECONDARY_DNS": '10.130.2.12',
        "PRIMARY_NTP": '10.101.18.1',
        "SECONDARY_NTP": '10.130.2.11',
        "DIRECTORY_SERVER": 'INFCOSADU001MP.mak.iss',
        "NAS_BASEDIR":
            'ssip.mtr-rec.infstonas001mp.mak.iss:'
            '/ifs/infstonas001mp/mtr-rec/',
        "VIP_NIC": 'vlan126',
        "VIP_MASK": 23,
        "CLUSTER_PREFIX": 'clnvrm',
    },
    "RTR": {
        "GATEWAY": '10.102.18.1',
        "SUBNET_MASK": '255.255.254.0',
        "PRIMARY_DNS": '10.130.4.11',
        "SECONDARY_DNS": '10.130.4.12',
        "PRIMARY_NTP": '10.102.18.1',
        "SECONDARY_NTP": '10.130.4.11',
        "DIRECTORY_SERVER": 'INFCOSADU001RP.mak.iss',
        "NAS_BASEDIR":
            'ssip.rtr-rec.infstonas001rp.mak.iss:'
            '/ifs/infstonas001rp/rtr-rec/',
        "VIP_NIC": 'vlan226',
        "VIP_MASK": 23,
        "CLUSTER_PREFIX": 'clnvrr',
    },
}

ILO_LDAP_CERT_FILENAME = "iss_root_ca.crt"
ILO_LDAP_CERT_FILE = os.path.join(TEMPLATES_DIR, ILO_LDAP_CERT_FILENAME)


# ============================================================================
# iLO RACK-MOUNT - EXCEL / EXECUTION
# ============================================================================

ILO_RM_EQUIPMENT_TYPES = ['NVR', 'VCA', 'ESXi']
ILO_RM_MAX_WORKERS = 16
ILO_RM_REPORT_PREFIX = "ILO_RM_Report"


# ============================================================================
# iLO RACK-MOUNT - REDFISH / RESET / DEBUG
# ============================================================================

ILO_RM_DEBUG_MODE = False
ILO_RM_REQUEST_TIMEOUT = 30

ILO_RM_RESET_INITIAL_WAIT_SECONDS = 20
ILO_RM_RESET_RETRY_INTERVAL_SECONDS = 10
ILO_RM_RESET_MAX_WAIT_SECONDS = 300


# ============================================================================
# iLO BLADE - EXCEL / EXECUTION / REPORTING
# ============================================================================

ILO_BL_VALID_EQUIPMENT_TYPES = ['NVR Blade Server', 'VCA Blade Server']
ILO_BL_EXCEL_COLUMNS = {'enclosure_physical_name',
 'enclosure_slot',
 'equipment_type',
 'hostname',
 'ilo_hostname',
 'ilo_ip',
 'scope'}
ILO_BL_REQUIRED_COLUMNS = ['enclosure_slot', 'ilo_ip', 'scope', 'hostname', 'ilo_hostname']
ILO_BL_EXCEL_EMPTY_ROW_STOP = EXCEL_EMPTY_ROW_STOP
ILO_BL_RIBCL_CONCURRENT_SESSIONS = 4
ILO_BL_REDFISH_CONCURRENT_SESSIONS = 16
ILO_BL_REPORT_PREFIX = "ILO_BL_Report"


# ============================================================================
# iLO BLADE - RIBCL / SSH / REDFISH / POST HANDLING
# ============================================================================

ILO_BL_DEBUG = False
ILO_BL_DEBUG_ON_FAILURE = True

ILO_BL_SSH_PORT = 22
ILO_BL_SSH_CONNECT_TIMEOUT = 15
ILO_BL_SSH_KEEPALIVE_INTERVAL = 5

ILO_BL_COMMAND_TIMEOUT = 120
ILO_BL_COMMAND_QUIET_TIME = 20.0
ILO_BL_HPONCFG_LINE_DELAY = 0.02

ILO_BL_AUTH_RETRIES = 5
ILO_BL_AUTH_RETRY_DELAY = 5
ILO_BL_LOGIN_PENALTY_WAIT = 32

ILO_BL_REDFISH_TIMEOUT = 25
ILO_BL_HTTP_SAFE_RETRIES = 2

ILO_BL_POST_ERROR_STRING = 'UnableToModifyDuringSystemPOST'
ILO_BL_POWER_OFF_POLL_INTERVAL = 5
ILO_BL_POWER_OFF_TIMEOUT = 90
ILO_BL_SETTLE_AFTER_POWEROFF = 5


# ============================================================================
# RAID - SHARED
# ============================================================================

# RAID automation uses the same global RESOURCE_LIST, SHEET_NAME,
# START_ROW and END_ROW defined above.
RAID_EXCEL_EMPTY_ROW_STOP = EXCEL_EMPTY_ROW_STOP

RAID_LEVEL = 'Raid1'
RAID_DISPLAY_NAME = 'RAID1'
RAID_DATA_DRIVE_COUNT = 2

# -1 = maximum available logical-drive capacity.
RAID_CAPACITY_GIB = -1

# Both rack-mount and blade RAID scripts currently use the same worker limit
# and storage discovery/build timeouts.
RAID_MAX_WORKERS = 16
RAID_CONTROLLER_TIMEOUT_MINUTES = 10
RAID_TIMEOUT_MINUTES = 30
RAID_POLL_INTERVAL_SECONDS = 30

# Common Redfish retry/auth behavior used by RAID automation.
RAID_AUTH_RETRIES = 3
RAID_AUTH_RETRY_DELAY_SECONDS = 10
RAID_HTTP_RETRY_TOTAL = 3
RAID_HTTP_RETRY_BACKOFF_FACTOR = 2
RAID_HTTP_RETRY_STATUS_CODES = (500, 502, 503, 504)


# ============================================================================
# RAID - RACK-MOUNT / GEN10+
# ============================================================================

RAID_RM_EQUIPMENT_TYPES = ['ESXi', 'NVR', 'VCA']
RAID_RM_REQUIRED_COLUMNS = ['ilo_ip']

RAID_RM_REQUEST_TIMEOUT_SECONDS = 20
RAID_RM_WRITE_TIMEOUT_SECONDS = 30

RAID_RM_REBOOT_DETECTION_TIMEOUT_SECONDS = 90
RAID_RM_REBOOT_DETECTION_POLL_SECONDS = 5
RAID_RM_POWER_OFF_TIMEOUT_SECONDS = 60
RAID_RM_POWER_ON_INITIAL_WAIT_SECONDS = 10

# iLO can reject BootSourceOverrideTarget changes while the host is in
# POST/System Utilities with iLO.2.21.UnableToModifyDuringSystemPOST.
# When enabled, configure_raid_RM.py powers the host off, verifies Off state,
# then retries the one-time BiosSetup boot override while the host is off.
RAID_RM_BOOT_OVERRIDE_POST_RECOVERY = True
RAID_RM_BOOT_OVERRIDE_RETRY_INTERVAL_SECONDS = 5
RAID_RM_BOOT_OVERRIDE_RETRY_TIMEOUT_SECONDS = 60

# DMTF MR-controller RAID apply / clean-volume handling.
# Fast initialization clears boot/partition metadata so an old OS cannot
# continue booting from a RAID volume that was deleted and recreated with
# the same geometry. Use 'Full' only when a complete block overwrite is
# required; it can take a long time on large drives.
# Maximum time allowed for DMTF RAID apply/visibility. The script does NOT
# sleep for this whole period; it polls continuously at the interval below and
# proceeds immediately when the expected RAID1 becomes visible.
RAID_RM_DMTF_APPLY_TIMEOUT_SECONDS = 300
RAID_RM_DMTF_POLL_INTERVAL_SECONDS = 5

# RAID volume initialization policy:
#
# - A genuinely NEW RAID volume is always initialized by configure_raid_RM.py
#   so stale partition/boot metadata cannot survive on previously-used disks.
#
# - When an EXISTING RAID is overwritten/recreated, initialization is controlled
#   by RAID_RM_INITIALIZE_OVERWRITTEN_VOLUME.
#
# True  = initialize the recreated/overwritten RAID volume.
# False = recreate the RAID but do not initialize its logical volume.
RAID_RM_INITIALIZE_OVERWRITTEN_VOLUME = False

# Fast is intended for normal provisioning. Full can take a long time because
# it writes the complete logical volume.
# HPE MR Redfish Volume.Initialize parameters.
#
# Foreground + Fast = quick erase / initialize; this clears the first/last
# metadata regions including old boot/partition information.
#
# Foreground + Slow = full erase / initialize and can take a long time.
RAID_RM_INITIALIZE_METHOD = 'Foreground'
RAID_RM_INITIALIZE_TYPE = 'Fast'
RAID_RM_INITIALIZE_ACTION_DISCOVERY_TIMEOUT_SECONDS = 60
RAID_RM_INITIALIZE_POLL_INTERVAL_SECONDS = 5
RAID_RM_INITIALIZE_TIMEOUT_SECONDS = 300
RAID_RM_INITIALIZE_SETTLE_SECONDS = 5

RAID_RM_REPORT_PREFIX = 'RAID_RM_DL380_Gen10Plus'


# ============================================================================
# RAID - BLADE / GEN9
# ============================================================================

# Blade RAID uses the same blade iLO credentials as the blade iLO
# configuration script.
RAID_BL_EQUIPMENT_TYPES = list(ILO_BL_VALID_EQUIPMENT_TYPES)
RAID_BL_REQUIRED_COLUMNS = ['enclosure_slot', 'ilo_ip']

RAID_BL_REQUEST_TIMEOUT_SECONDS = 15

RAID_BL_ISO_URL = (
    'https://infidsrep001sp.mak.iss:8443/'
    'BL460c-Gen9-P244br-RAID1-UEFI.iso'
)

RAID_BL_REPORT_PREFIX = 'RAID_BL'



# ============================================================================
# OA CONFIG GENERATOR
# ============================================================================

# gen_oaconfig.py intentionally scans the complete configured worksheet so
# configuration files can be generated for every enclosure. It therefore does
# not use START_ROW / END_ROW. It uses the shared RESOURCE_LIST, SHEET_NAME,
# TEMPLATES_DIR, INVALID_VALUES, DOMAIN_NAME, LDAP_USER_CONTEXTS and
# ILO_SCOPE_SETTINGS defined above.

OA_CONFIG_TEMPLATE_FILENAME = 'OACONFIG.j2'
OA_CONFIG_OUTPUT_DIR = os.path.join(PROJECT_DIR, 'oaconfig_scripts')

OA_APP_CERT_FILENAME = 'iss_app_cert.pem'
OA_NWS_CERT_FILENAME = 'iss_nws_cert.pem'
OA_APP_CERT_FILE = os.path.join(TEMPLATES_DIR, OA_APP_CERT_FILENAME)
OA_NWS_CERT_FILE = os.path.join(TEMPLATES_DIR, OA_NWS_CERT_FILENAME)

OA_ILO_ADMIN_GROUP = 'ILOAdmins'

# Reuse the existing primary DNS server as the OA remote syslog destination.
OA_REMOTE_SYSLOG_SERVER = DNS_SERVER

OA_SNMP_COMMUNITY = 'ISS-PUB'
OA_SNMP_CONTACT = 'Aftab Ahmed'
OA_SNMP_LOCATION = 'Makkah'

OA_REQUIRED_COLUMNS = [
    'equipment_type',
    'enclosure_physical_name',
    'scope',
    'enclosure_slot',
    'hostname',
    'ilo_ip',
]

OA_SERVER_ENCLOSURE_TYPE = 'Server Enclosure'
OA_ENCLOSURE_OA_TYPE = 'Enclosure OA'
OA_ENCLOSURE_SWITCH_TYPE = 'Enclosure Switch'
OA_BLADE_EQUIPMENT_TYPES = [
    'NVR Blade Server',
    'VCA Blade Server',
]

OA_COMPONENT_EQUIPMENT_TYPES = (
    [OA_ENCLOSURE_OA_TYPE]
    + OA_BLADE_EQUIPMENT_TYPES
    + [OA_ENCLOSURE_SWITCH_TYPE]
)

OA_BLADE_SLOT_COUNT = 16
OA_INTERCONNECT_SLOT_COUNT = 8


# ============================================================================
# SERIAL / MAC ADDRESS COLLECTION - SHARED
# ============================================================================

# Both MAC collection scripts write the same serial/MAC columns.
MAC_SERIAL_COLUMN = 'serial_no'
MAC_NIC_COLUMNS = [
    'nic0_mac',
    'nic1_mac',
    'nic2_mac',
    'nic3_mac',
    'nic4_mac',
    'nic5_mac',
]
MAC_MAX_ADDRESSES = len(MAC_NIC_COLUMNS)
MAC_OUTPUT_COLUMNS = [MAC_SERIAL_COLUMN] + MAC_NIC_COLUMNS


# ============================================================================
# SERIAL / MAC ADDRESS COLLECTION - RACK-MOUNT
# ============================================================================

# Uses the same rack-mount iLO credentials, RESOURCE_LIST, SHEET_NAME,
# START_ROW and END_ROW defined above.
MAC_RM_TARGET_EQUIPMENT = {
    'ESXI': 4,
    'NVR': 4,
    'VCA': 4,
}

MAC_RM_REQUIRED_COLUMNS = (
    ['ilo_ip', 'equipment_type']
    + MAC_OUTPUT_COLUMNS
)

# Preserve the existing 16-session behavior while deriving it from the
# rack-mount iLO concurrency setting.
MAC_RM_MAX_WORKERS = ILO_RM_MAX_WORKERS

MAC_RM_PING_COUNT = 2
MAC_RM_PING_TIMEOUT_MS = 300

MAC_RM_API_TIMEOUT_SECONDS = 10
MAC_RM_API_RETRIES = 3
MAC_RM_API_RETRY_BACKOFF = 1
MAC_RM_API_RETRY_STATUS_CODES = (
    429,
    500,
    502,
    503,
    504,
)

MAC_RM_DEBUG = False


# ============================================================================
# SERIAL / MAC ADDRESS COLLECTION - BLADE / OA
# ============================================================================

# get_mac_BL.py intentionally scans the worksheet from row 2 because it first
# needs to locate the requested enclosure and both OA addresses. The shared
# EXCEL_EMPTY_ROW_STOP controls optimized early termination.
MAC_BL_REQUIRED_COLUMNS = [
    'equipment_physical_name',
    'enclosure_physical_name',
    'equipment_type',
    'enclosure_slot',
    'ilo_ip',
] + MAC_OUTPUT_COLUMNS

MAC_BL_EXCEL_EMPTY_ROW_STOP = EXCEL_EMPTY_ROW_STOP

# OA connection settings used specifically by the MAC collection script.
MAC_BL_OA_CONNECT_TIMEOUT = 10
MAC_BL_OA_BANNER_TIMEOUT = ILO_BL_SSH_CONNECT_TIMEOUT
MAC_BL_OA_AUTH_TIMEOUT = ILO_BL_SSH_CONNECT_TIMEOUT
MAC_BL_OA_KEEPALIVE_INTERVAL = ILO_BL_SSH_KEEPALIVE_INTERVAL

MAC_BL_OA_SHELL_SETTLE_SECONDS = 1
MAC_BL_OA_COMMAND_TIMEOUT_SECONDS = 60
MAC_BL_OA_COMMAND_SETTLE_SECONDS = 0.5
MAC_BL_OA_POLL_INTERVAL_SECONDS = 0.1


# ============================================================================
# CLUSTER CONFIG GENERATOR
# ============================================================================

# gen_clusterconfig.py intentionally reads the COMPLETE configured worksheet.
# START_ROW / END_ROW and EXCEL_EMPTY_ROW_STOP are not used by this generator
# because blade nodes and their corresponding VIP rows can be located anywhere
# in the resource list. Cluster-specific scope values are merged into the shared
# ILO_SCOPE_SETTINGS dictionary above.

CLUSTER_OUTPUT_DIR = os.path.join(PROJECT_DIR, 'cluster_scripts')

CLUSTER_TOKEN_TIMEOUT = 10000

CLUSTER_HA_USERNAME = 'hacluster'
CLUSTER_HA_PASSWORD = 'Th@les01'

CLUSTER_RESOURCE_COUNT = 13

# Pacemaker fencing reuses the project's centralized fencing account.
CLUSTER_FENCE_USERNAME = FENCE_USER_LOGIN
CLUSTER_FENCE_PASSWORD = FENCE_USER_PASSWORD

CLUSTER_PICATA_CONFIG_UPDATE_AGENT = 'systemd:configuration-updater'

CLUSTER_BLADE_EQUIPMENT_TYPE = 'nvr blade server'
CLUSTER_VIP_COMPONENT_SHORT_NAME = 'vip'
CLUSTER_VIP_COMPONENT_NAME = 'network video recorder'

CLUSTER_NODE_GROUP_SIZE = 8
CLUSTER_INDEX_STEP = 10
CLUSTER_VIP_COUNT_PER_CLUSTER = 7

CLUSTER_REQUIRED_COLUMNS = [
    'equipment_type',
    'enclosure_physical_name',
    'scope',
    'hostname',
    'logical_name',
    'ilo_ip',
    'cl_ip_address',
    'me_ip_address',
    'component_short_name',
    'component',
    'alias',
    'fe_ip_address',
]


# ============================================================================
# HOSTGROUP MAPPING
# ============================================================================

hg_map = {'acscem1': 'ACS',
 'cwdsdp1': 'SDP',
 'cwdvca1': 'VCA',
 'infics1': 'IT',
 'infids1': 'IT',
 'infims1': 'IT',
 'infitc1': 'IT',
 'infsrv1': 'IT',
 'infsup1': 'Supervision',
 'infvir1': 'IT',
 'tvsnvr1': 'NVR',
 'tvsnvr2': 'NVR2',
 'tvsvms1': 'TVS',
 'ucscal1': 'UCS',
 'ucscis1': 'UCS',
 'ucsimg1': 'UCS'}
