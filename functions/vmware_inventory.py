# BUILD_MARKER: VMWARE_NAME_IP_INVENTORY_CHECK_V2_20260830

import ipaddress
import time
from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
)
from urllib.parse import quote

import requests
import urllib3

from functions import vars
from functions.shared import is_valid


urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)


class VCenterError(Exception):
    """Base exception for vCenter REST operations."""


class VCenterAuthenticationError(VCenterError):
    """Raised when vCenter credentials are rejected."""


class VCenterClient(object):
    """
    Small vCenter REST client.

    Supports:
      - modern /api/session + /api/vcenter/vm
      - legacy /rest/com/vmware/cis/session + /rest/vcenter/vm

    Guest IP discovery first tries the guest networking interfaces API and then
    falls back to guest identity (primary IP) when the interfaces endpoint is
    unavailable.

    No pyVmomi dependency is required.
    """

    def __init__(
        self,
        hostname=None,
        username=None,
        password=None,
        port=None,
        verify_ssl=None,
    ):

        self.hostname = (
            vars.VMWARE_HOST
            if hostname is None
            else hostname
        )

        self.username = (
            vars.VMWARE_USERNAME
            if username is None
            else username
        )

        self.password = (
            vars.VMWARE_PASSWORD
            if password is None
            else password
        )

        self.port = (
            vars.VMWARE_PORT
            if port is None
            else port
        )

        self.verify_ssl = (
            vars.VMWARE_VERIFY_SSL
            if verify_ssl is None
            else verify_ssl
        )

        self.base_url = (
            "https://{}:{}".format(
                self.hostname,
                self.port,
            )
        )

        self.session = requests.Session()
        self.session.verify = self.verify_ssl
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Connection": "close",
        })

        self.api_mode = None
        self.session_id = None


    def close(self):

        try:
            self.logout()
        finally:

            try:
                self.session.close()
            except Exception:
                pass


    def _timeout(self):

        return (
            vars.VMWARE_CONNECT_TIMEOUT_SECONDS,
            vars.VMWARE_READ_TIMEOUT_SECONDS,
        )


    def _request(
        self,
        method,
        path,
        auth=None,
        retry=True,
    ):

        url = (
            self.base_url
            + (
                path
                if path.startswith("/")
                else "/" + path
            )
        )

        attempts = (
            max(
                1,
                int(
                    vars.VMWARE_HTTP_RETRIES
                ),
            )
            if retry
            else 1
        )

        last_error = None
        last_response = None

        for attempt in range(
            1,
            attempts + 1,
        ):

            try:

                response = self.session.request(
                    method=method,
                    url=url,
                    auth=auth,
                    timeout=self._timeout(),
                )

                last_response = response

                if response.status_code in (
                    401,
                    403,
                ):

                    raise VCenterAuthenticationError(
                        "vCenter authentication failed "
                        "(HTTP {}).".format(
                            response.status_code
                        )
                    )

                if (
                    retry
                    and response.status_code in (
                        429,
                        500,
                        502,
                        503,
                        504,
                    )
                    and attempt < attempts
                ):

                    time.sleep(
                        vars
                        .VMWARE_HTTP_RETRY_DELAY_SECONDS
                    )

                    continue

                return response

            except VCenterAuthenticationError:

                raise

            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.SSLError,
            ) as exc:

                last_error = exc

                if attempt < attempts:

                    time.sleep(
                        vars
                        .VMWARE_HTTP_RETRY_DELAY_SECONDS
                    )

                    continue

                break

        if last_response is not None:

            return last_response

        raise VCenterError(
            "Unable to connect to vCenter {}: {}"
            .format(
                self.hostname,
                last_error,
            )
        )


    def _isolated_get(
        self,
        path,
        retry=True,
    ):
        """
        Thread-safe GET using a new requests.Session per call.

        Guest-IP discovery runs in parallel, so worker threads do not share the
        main requests.Session object.
        """

        if not self.session_id:

            raise VCenterError(
                "vCenter session is not authenticated."
            )

        url = (
            self.base_url
            + (
                path
                if path.startswith("/")
                else "/" + path
            )
        )

        attempts = (
            max(
                1,
                int(
                    vars.VMWARE_HTTP_RETRIES
                ),
            )
            if retry
            else 1
        )

        last_error = None
        last_response = None

        for attempt in range(
            1,
            attempts + 1,
        ):

            isolated = requests.Session()

            try:

                isolated.verify = self.verify_ssl
                isolated.headers.update({
                    "Accept":
                        "application/json",

                    "Content-Type":
                        "application/json",

                    "Connection":
                        "close",

                    "vmware-api-session-id":
                        self.session_id,
                })

                response = isolated.get(
                    url,
                    timeout=self._timeout(),
                )

                last_response = response

                if response.status_code in (
                    401,
                    403,
                ):

                    raise VCenterAuthenticationError(
                        "vCenter authentication failed "
                        "(HTTP {}).".format(
                            response.status_code
                        )
                    )

                if (
                    retry
                    and response.status_code in (
                        429,
                        500,
                        502,
                        504,
                    )
                    and attempt < attempts
                ):

                    time.sleep(
                        vars
                        .VMWARE_HTTP_RETRY_DELAY_SECONDS
                    )

                    continue

                # 503 is meaningful for guest APIs: VMware Tools may not be
                # running / may not have guest data, so return it to caller.
                return response

            except VCenterAuthenticationError:

                raise

            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.SSLError,
            ) as exc:

                last_error = exc

                if attempt < attempts:

                    time.sleep(
                        vars
                        .VMWARE_HTTP_RETRY_DELAY_SECONDS
                    )

                    continue

                break

            finally:

                try:
                    isolated.close()
                except Exception:
                    pass

        if last_response is not None:

            return last_response

        raise VCenterError(
            "vCenter guest-IP request failed: {}"
            .format(
                last_error
            )
        )


    @staticmethod
    def _safe_json(
        response,
    ):

        try:
            return response.json()
        except Exception:
            return None


    def login(self):
        """
        Authenticate once and keep the VMware API session ID in the session
        header for all subsequent calls.
        """

        response = self._request(
            "POST",
            "/api/session",
            auth=(
                self.username,
                self.password,
            ),
            retry=True,
        )

        if response.status_code in (
            200,
            201,
        ):

            payload = self._safe_json(
                response
            )

            if isinstance(
                payload,
                str,
            ):

                session_id = payload

            elif isinstance(
                payload,
                dict,
            ):

                session_id = (
                    payload.get(
                        "value"
                    )
                    or payload.get(
                        "session_id"
                    )
                )

            else:

                session_id = None

            if session_id:

                self.api_mode = "api"
                self.session_id = str(
                    session_id
                )

                self.session.headers.update({
                    "vmware-api-session-id":
                        self.session_id
                })

                return self.session_id

        if response.status_code not in (
            404,
            405,
            501,
        ):

            raise VCenterError(
                "vCenter /api/session login failed. "
                "HTTP {}: {}".format(
                    response.status_code,
                    response.text[:700],
                )
            )

        response = self._request(
            "POST",
            "/rest/com/vmware/cis/session",
            auth=(
                self.username,
                self.password,
            ),
            retry=True,
        )

        if response.status_code not in (
            200,
            201,
        ):

            raise VCenterError(
                "vCenter legacy session login failed. "
                "HTTP {}: {}".format(
                    response.status_code,
                    response.text[:700],
                )
            )

        payload = self._safe_json(
            response
        )

        session_id = None

        if isinstance(
            payload,
            dict,
        ):

            session_id = payload.get(
                "value"
            )

        if not session_id:

            raise VCenterError(
                "vCenter legacy session login succeeded, "
                "but no session ID was returned."
            )

        self.api_mode = "rest"
        self.session_id = str(
            session_id
        )

        self.session.headers.update({
            "vmware-api-session-id":
                self.session_id
        })

        return self.session_id


    def logout(self):

        if not self.session_id:

            return

        try:

            if self.api_mode == "api":

                self._request(
                    "DELETE",
                    "/api/session",
                    retry=False,
                )

            elif self.api_mode == "rest":

                self._request(
                    "DELETE",
                    "/rest/com/vmware/cis/session",
                    retry=False,
                )

        except Exception:

            pass

        finally:

            self.session_id = None
            self.api_mode = None

            try:
                self.session.headers.pop(
                    "vmware-api-session-id",
                    None,
                )
            except Exception:
                pass


    def list_vms(self):

        if not self.session_id:

            self.login()

        if self.api_mode == "api":

            response = self._request(
                "GET",
                "/api/vcenter/vm",
                retry=True,
            )

        else:

            response = self._request(
                "GET",
                "/rest/vcenter/vm",
                retry=True,
            )

        if response.status_code != 200:

            raise VCenterError(
                "Unable to retrieve vCenter VM inventory. "
                "HTTP {}: {}".format(
                    response.status_code,
                    response.text[:1000],
                )
            )

        payload = self._safe_json(
            response
        )

        if self.api_mode == "rest":

            if not isinstance(
                payload,
                dict,
            ):

                raise VCenterError(
                    "Legacy vCenter VM inventory returned "
                    "an unexpected JSON structure."
                )

            vm_list = payload.get(
                "value",
                [],
            )

        else:

            vm_list = payload

        if not isinstance(
            vm_list,
            list,
        ):

            raise VCenterError(
                "vCenter VM inventory returned an unexpected "
                "JSON structure."
            )

        return vm_list


    def get_vm_guest_ips(
        self,
        vm,
    ):
        """
        Return all guest IPs reported by vCenter for one VM.

        Preferred source:
          /guest/networking/interfaces
          - exposes all guest interface addresses when supported.

        Fallback:
          /guest/identity
          - exposes the guest's primary IP.

        VMware Tools / guest data may be unavailable. That is reported as an
        incomplete inventory result rather than silently claiming "no IP".
        """

        vm_id = _vm_id(
            vm
        )

        vm_name = str(
            vm.get(
                "name",
                "",
            )
            or ""
        )

        encoded_vm_id = quote(
            vm_id,
            safe="",
        )

        if self.api_mode == "api":

            interfaces_path = (
                "/api/vcenter/vm/{}/guest/networking/interfaces"
                .format(
                    encoded_vm_id
                )
            )

            identity_path = (
                "/api/vcenter/vm/{}/guest/identity"
                .format(
                    encoded_vm_id
                )
            )

        else:

            interfaces_path = (
                "/rest/vcenter/vm/{}/guest/networking/interfaces"
                .format(
                    encoded_vm_id
                )
            )

            identity_path = (
                "/rest/vcenter/vm/{}/guest/identity"
                .format(
                    encoded_vm_id
                )
            )

        response = self._isolated_get(
            interfaces_path,
            retry=True,
        )

        if response.status_code == 200:

            payload = self._safe_json(
                response
            )

            if self.api_mode == "rest":

                if isinstance(
                    payload,
                    dict,
                ):

                    interfaces = payload.get(
                        "value",
                        [],
                    )

                else:

                    interfaces = []

            else:

                interfaces = payload

            if not isinstance(
                interfaces,
                list,
            ):

                interfaces = []

            addresses = set()

            for interface in interfaces:

                if not isinstance(
                    interface,
                    dict,
                ):

                    continue

                ip_data = (
                    interface.get(
                        "ip",
                        {},
                    )
                    or {}
                )

                ip_addresses = (
                    ip_data.get(
                        "ip_addresses",
                        [],
                    )
                    or []
                )

                for item in ip_addresses:

                    if isinstance(
                        item,
                        dict,
                    ):

                        raw_ip = item.get(
                            "ip_address"
                        )

                    else:

                        raw_ip = item

                    normalized = normalize_ip(
                        raw_ip
                    )

                    if normalized:

                        addresses.add(
                            normalized
                        )

            return {
                "vm_id":
                    vm_id,

                "vm_name":
                    vm_name,

                "power_state":
                    _vm_power_state(
                        vm
                    ),

                "available":
                    True,

                "source":
                    "guest_networking_interfaces",

                "ips":
                    sorted(
                        addresses
                    ),

                "details":
                    "",
            }

        # 404/405/501 can indicate an older vCenter where the interfaces API
        # is unavailable. 503 commonly means VMware Tools/guest data is not
        # available; identity may still provide a cached/primary address, so
        # try it before marking this VM unavailable.
        if response.status_code not in (
            404,
            405,
            501,
            503,
        ):

            return {
                "vm_id":
                    vm_id,

                "vm_name":
                    vm_name,

                "power_state":
                    _vm_power_state(
                        vm
                    ),

                "available":
                    False,

                "source":
                    "guest_networking_interfaces",

                "ips":
                    [],

                "details":
                    (
                        "Guest networking query failed "
                        "HTTP {}: {}"
                    ).format(
                        response.status_code,
                        response.text[:300],
                    ),
            }

        identity_response = self._isolated_get(
            identity_path,
            retry=True,
        )

        if identity_response.status_code == 200:

            payload = self._safe_json(
                identity_response
            )

            if (
                self.api_mode == "rest"
                and isinstance(
                    payload,
                    dict,
                )
            ):

                identity = (
                    payload.get(
                        "value",
                        {},
                    )
                    or {}
                )

            else:

                identity = (
                    payload
                    if isinstance(
                        payload,
                        dict,
                    )
                    else {}
                )

            primary_ip = normalize_ip(
                identity.get(
                    "ip_address"
                )
            )

            return {
                "vm_id":
                    vm_id,

                "vm_name":
                    vm_name,

                "power_state":
                    _vm_power_state(
                        vm
                    ),

                "available":
                    True,

                "source":
                    "guest_identity",

                "ips":
                    (
                        [primary_ip]
                        if primary_ip
                        else []
                    ),

                "details":
                    "",
            }

        return {
            "vm_id":
                vm_id,

            "vm_name":
                vm_name,

            "power_state":
                _vm_power_state(
                    vm
                ),

            "available":
                False,

            "source":
                "guest_identity",

            "ips":
                [],

            "details":
                (
                    "Guest IP data unavailable. "
                    "InterfacesHTTP={}; IdentityHTTP={}"
                ).format(
                    response.status_code,
                    identity_response.status_code,
                ),
        }


def normalize_name(
    value,
):

    if not is_valid(
        value
    ):

        return ""

    return str(
        value
    ).strip()


def normalize_ip(
    value,
):

    if not is_valid(
        value
    ):

        return ""

    text = str(
        value
    ).strip()

    if not text:

        return ""

    # Remove an IPv6 zone/scope suffix when present.
    if "%" in text:

        text = text.split(
            "%",
            1,
        )[0]

    try:

        return (
            ipaddress.ip_address(
                text
            )
            .compressed
            .lower()
        )

    except ValueError:

        return ""


def build_vm_name_index(
    vm_list,
):

    index = {}

    for vm in vm_list or []:

        if not isinstance(
            vm,
            dict,
        ):

            continue

        name = normalize_name(
            vm.get(
                "name"
            )
        )

        if not name:

            continue

        index.setdefault(
            name.lower(),
            [],
        ).append(
            vm
        )

    return index


def _vm_id(
    vm,
):

    return str(
        vm.get(
            "vm",
            vm.get(
                "vm_id",
                vm.get(
                    "id",
                    "Unknown",
                ),
            ),
        )
        or "Unknown"
    )


def _vm_power_state(
    vm,
):

    return str(
        vm.get(
            "power_state",
            vm.get(
                "powerState",
                "Unknown",
            ),
        )
        or "Unknown"
    )


def build_vm_ip_index(
    client,
    vm_list,
    max_workers,
):
    """
    Discover guest IPs in parallel and build:
        normalized_ip -> [VM metadata...]

    Returns:
        ip_index,
        scan_info
    """

    ip_index = {}

    results = []
    unavailable = []
    errors = []

    workers = max(
        1,
        int(
            max_workers
        ),
    )

    with ThreadPoolExecutor(
        max_workers=workers
    ) as executor:

        future_map = {
            executor.submit(
                client.get_vm_guest_ips,
                vm,
            ):
                vm
            for vm in (
                vm_list
                or []
            )
        }

        for future in as_completed(
            future_map
        ):

            vm = future_map[
                future
            ]

            try:

                result = future.result()
                results.append(
                    result
                )

                if not result.get(
                    "available"
                ):

                    unavailable.append(
                        result
                    )

                    continue

                for ip_value in (
                    result.get(
                        "ips",
                        [],
                    )
                    or []
                ):

                    ip_index.setdefault(
                        ip_value,
                        [],
                    ).append({
                        "vm_id":
                            result.get(
                                "vm_id",
                                _vm_id(
                                    vm
                                ),
                            ),

                        "vm_name":
                            result.get(
                                "vm_name",
                                str(
                                    vm.get(
                                        "name",
                                        "",
                                    )
                                    or ""
                                ),
                            ),

                        "power_state":
                            result.get(
                                "power_state",
                                _vm_power_state(
                                    vm
                                ),
                            ),

                        "source":
                            result.get(
                                "source",
                                "unknown",
                            ),
                    })

            except Exception as exc:

                error = {
                    "vm_id":
                        _vm_id(
                            vm
                        ),

                    "vm_name":
                        str(
                            vm.get(
                                "name",
                                "",
                            )
                            or ""
                        ),

                    "power_state":
                        _vm_power_state(
                            vm
                        ),

                    "details":
                        str(
                            exc
                        ),
                }

                errors.append(
                    error
                )

    scan_info = {
        "total_vms":
            len(
                vm_list
                or []
            ),

        "available_vms":
            len(
                results
            )
            - len(
                unavailable
            ),

        "unavailable_vms":
            len(
                unavailable
            ),

        "error_vms":
            len(
                errors
            ),

        "unique_ips":
            len(
                ip_index
            ),

        "complete":
            (
                not unavailable
                and not errors
            ),

        "unavailable":
            unavailable,

        "errors":
            errors,
    }

    return (
        ip_index,
        scan_info,
    )


def _format_vm_matches(
    matches,
):

    parts = []

    for match in matches or []:

        parts.append(
            "{} (VM={}, PowerState={})"
            .format(
                match.get(
                    "vm_name",
                    "Unknown",
                ),
                match.get(
                    "vm_id",
                    "Unknown",
                ),
                match.get(
                    "power_state",
                    "Unknown",
                ),
            )
        )

    return (
        ", ".join(
            parts
        )
        if parts
        else "none"
    )


def check_record(
    record,
    vm_name_index,
    vm_ip_index,
    ip_scan_info,
):
    """
    Check:
      - VM name against both hostname and logical_name.
      - reserved FE IP against every discoverable existing VM guest IP.
      - reserved ME IP when populated.

    fe_ip_address is mandatory.
    me_ip_address may be empty.
    """

    hostname = normalize_name(
        record.get(
            "hostname"
        )
    )

    logical_name = normalize_name(
        record.get(
            "logical_name"
        )
    )

    raw_fe_ip = record.get(
        "fe_ip_address"
    )

    raw_me_ip = record.get(
        "me_ip_address"
    )

    fe_ip = normalize_ip(
        raw_fe_ip
    )

    me_ip = normalize_ip(
        raw_me_ip
    )

    raw_fe_text = normalize_name(
        raw_fe_ip
    )

    raw_me_text = normalize_name(
        raw_me_ip
    )

    validation_errors = []

    if (
        vars.VMWARE_FE_IP_REQUIRED
        and not raw_fe_text
    ):

        validation_errors.append(
            "fe_ip_address is required"
        )

    elif (
        raw_fe_text
        and not fe_ip
    ):

        validation_errors.append(
            "fe_ip_address '{}' is not a valid IP"
            .format(
                raw_fe_text
            )
        )

    if (
        raw_me_text
        and not me_ip
    ):

        validation_errors.append(
            "me_ip_address '{}' is not a valid IP"
            .format(
                raw_me_text
            )
        )

    name_candidates = []

    if hostname:

        name_candidates.append(
            (
                "hostname",
                hostname,
            )
        )

    if logical_name:

        name_candidates.append(
            (
                "logical_name",
                logical_name,
            )
        )

    if not name_candidates:

        validation_errors.append(
            "hostname and logical_name are both empty/invalid"
        )

    if validation_errors:

        return {
            "checked":
                False,

            "valid":
                False,

            "name_exists":
                False,

            "fe_ip_conflict":
                False,

            "me_ip_conflict":
                False,

            "any_conflict":
                False,

            "details":
                (
                    "Validation=FAILED; {}"
                ).format(
                    "; ".join(
                        validation_errors
                    )
                ),
        }

    name_matches = []
    seen_name_matches = set()

    for field_name, candidate in name_candidates:

        for vm in (
            vm_name_index.get(
                candidate.lower(),
                [],
            )
            or []
        ):

            key = (
                "{}|{}|{}"
            ).format(
                field_name,
                candidate.lower(),
                _vm_id(
                    vm
                ),
            )

            if key in seen_name_matches:

                continue

            seen_name_matches.add(
                key
            )

            name_matches.append({
                "field":
                    field_name,

                "excel_name":
                    candidate,

                "vm_name":
                    str(
                        vm.get(
                            "name",
                            "",
                        )
                        or ""
                    ),

                "vm_id":
                    _vm_id(
                        vm
                    ),

                "power_state":
                    _vm_power_state(
                        vm
                    ),
            })

    fe_matches = (
        vm_ip_index.get(
            fe_ip,
            [],
        )
        or []
    )

    me_matches = (
        (
            vm_ip_index.get(
                me_ip,
                [],
            )
            or []
        )
        if me_ip
        else []
    )

    name_exists = bool(
        name_matches
    )

    fe_conflict = bool(
        fe_matches
    )

    me_conflict = bool(
        me_matches
    )

    any_conflict = (
        name_exists
        or fe_conflict
        or me_conflict
    )

    name_detail = (
        "NameExists=YES [{}]"
        .format(
            "; ".join(
                (
                    "{}={} -> {} "
                    "(VM={}, PowerState={})"
                ).format(
                    match[
                        "field"
                    ],
                    match[
                        "excel_name"
                    ],
                    match[
                        "vm_name"
                    ],
                    match[
                        "vm_id"
                    ],
                    match[
                        "power_state"
                    ],
                )
                for match in name_matches
            )
        )
        if name_exists
        else "NameExists=NO"
    )

    fe_detail = (
        "FE_IP={} Conflict={} [{}]"
        .format(
            fe_ip,
            (
                "YES"
                if fe_conflict
                else "NO"
            ),
            _format_vm_matches(
                fe_matches
            ),
        )
    )

    if me_ip:

        me_detail = (
            "ME_IP={} Conflict={} [{}]"
            .format(
                me_ip,
                (
                    "YES"
                    if me_conflict
                    else "NO"
                ),
                _format_vm_matches(
                    me_matches
                ),
            )
        )

    else:

        me_detail = (
            "ME_IP=EMPTY (allowed; not checked)"
        )

    scan_complete = bool(
        ip_scan_info.get(
            "complete"
        )
    )

    visibility_detail = (
        "IPInventory=COMPLETE"
        if scan_complete
        else (
            "IPInventory=INCOMPLETE "
            "(UnavailableVMs={}, ErrorVMs={})"
            .format(
                ip_scan_info.get(
                    "unavailable_vms",
                    0,
                ),
                ip_scan_info.get(
                    "error_vms",
                    0,
                ),
            )
        )
    )

    return {
        "checked":
            True,

        "valid":
            True,

        "name_exists":
            name_exists,

        "fe_ip_conflict":
            fe_conflict,

        "me_ip_conflict":
            me_conflict,

        "any_conflict":
            any_conflict,

        "ip_inventory_complete":
            scan_complete,

        "details":
            (
                "{}; {}; {}; {}; AnyConflict={}"
            ).format(
                name_detail,
                fe_detail,
                me_detail,
                visibility_detail,
                (
                    "YES"
                    if any_conflict
                    else "NO"
                ),
            ),
    }
