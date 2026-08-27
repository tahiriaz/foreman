# BUILD_MARKER: FOREMAN_SERIAL_CREATE_V1_20260827

import threading
import time
from contextlib import contextmanager

import requests

from functions import vars
from functions.shared import is_valid


HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}

REQUEST_TIMEOUT = (
    vars.HTTP_CONNECT_TIMEOUT,
    vars.HTTP_READ_TIMEOUT,
)
POST_CREATE_VERIFY_ATTEMPTS = vars.FOREMAN_VERIFY_ATTEMPTS
POST_CREATE_VERIFY_DELAY = vars.FOREMAN_VERIFY_DELAY

_resource_cache = {}
_resource_cache_lock = threading.Lock()

_create_concurrency = max(
    1,
    int(vars.FOREMAN_CREATE_CONCURRENCY),
)

_foreman_create_semaphore = threading.BoundedSemaphore(
    _create_concurrency
)


def _api_url(endpoint):
    """Build a Foreman API URL."""
    return "{}/{}".format(
        vars.FOREMAN_URL.rstrip("/"),
        endpoint.lstrip("/"),
    )


@contextmanager
def host_creation_slot(label="Foreman host"):
    """
    Serialize the Foreman host-creation transaction.

    The slot intentionally remains held through:
      - final existence check
      - POST /api/hosts
      - post-create API verification
      - short settlement delay

    DNS runs after this context exits and therefore remains parallel.
    """
    print(
        "{} waiting for Foreman creation slot "
        "(concurrency={})...".format(
            label,
            _create_concurrency,
        )
    )

    _foreman_create_semaphore.acquire()

    try:
        print(
            "{} acquired Foreman creation slot.".format(
                label
            )
        )

        yield

    finally:
        settle_seconds = int(
            vars.FOREMAN_CREATE_SETTLE_SECONDS
        )

        if settle_seconds > 0:
            print(
                "{} waiting {} second(s) for Foreman "
                "post-create settlement...".format(
                    label,
                    settle_seconds,
                )
            )

            time.sleep(
                settle_seconds
            )

        _foreman_create_semaphore.release()

        print(
            "{} released Foreman creation slot.".format(
                label
            )
        )


def _response_host_data(response):
    """Extract the host dictionary from a Foreman response."""
    try:
        data = response.json()
    except (TypeError, ValueError):
        raise RuntimeError(
            "Foreman returned HTTP {}, but the response was not "
            "valid JSON: {}".format(
                response.status_code,
                response.text,
            )
        )

    if not isinstance(data, dict):
        raise RuntimeError(
            "Foreman returned HTTP {}, but the JSON response was "
            "not an object.".format(
                response.status_code
            )
        )

    if isinstance(
        data.get("host"),
        dict,
    ):
        data = data["host"]

    return data


def get_response_host_id(response):
    """Return the host ID contained in a Foreman response."""
    try:
        return _response_host_data(
            response
        ).get("id")
    except Exception:
        return None


def get_resource_id(endpoint, name, key="name"):
    """Return an exact Foreman resource ID."""
    if not is_valid(name):
        raise ValueError(
            "Cannot resolve Foreman resource ID for endpoint '{}': "
            "resource name is empty".format(
                endpoint
            )
        )

    try:
        response = requests.get(
            _api_url(endpoint),
            auth=(
                vars.USER,
                vars.PASSWORD,
            ),
            params={
                "search": '{} = "{}"'.format(
                    key,
                    str(name).strip(),
                )
            },
            headers=HEADERS,
            verify=vars.VERIFY_SSL,
            timeout=vars.RESOURCE_LOOKUP_TIMEOUT,
        )

        response.raise_for_status()
        data = response.json()

        if not isinstance(data, dict):
            raise RuntimeError(
                "Foreman resource lookup for endpoint '{}' "
                "returned unexpected JSON.".format(
                    endpoint
                )
            )

        results = data.get(
            "results",
            [],
        )

        if not results:
            raise LookupError(
                "Foreman resource not found: endpoint='{}', "
                "{}='{}'".format(
                    endpoint,
                    key,
                    name,
                )
            )

        return results[0]["id"]

    except requests.exceptions.ConnectionError as exc:
        raise ConnectionError(
            "Connection to Foreman failed: {}. Verify network/VPN "
            "connectivity and Foreman availability.".format(
                vars.FOREMAN_URL
            )
        ) from exc

    except requests.exceptions.Timeout as exc:
        raise TimeoutError(
            "Connection to Foreman timed out while resolving "
            "endpoint '{}': {}".format(
                endpoint,
                vars.FOREMAN_URL,
            )
        ) from exc

    except requests.exceptions.RequestException as exc:
        raise RuntimeError(
            "Foreman API request failed for endpoint '{}': {}".format(
                endpoint,
                exc,
            )
        ) from exc


def get_cached_resource_id(endpoint, name, key="name"):
    """Return a cached Foreman resource ID."""
    if not is_valid(name):
        raise ValueError(
            "Cannot resolve Foreman resource ID for endpoint '{}': "
            "resource name is empty".format(
                endpoint
            )
        )

    cache_key = (
        endpoint,
        key,
        str(name).strip().lower(),
    )

    with _resource_cache_lock:
        if cache_key in _resource_cache:
            return _resource_cache[
                cache_key
            ]

    resource_id = get_resource_id(
        endpoint,
        name,
        key,
    )

    with _resource_cache_lock:
        _resource_cache[
            cache_key
        ] = resource_id

    return resource_id


def clear_resource_cache():
    """Clear the resource-ID cache."""
    with _resource_cache_lock:
        _resource_cache.clear()


def get_host(*names):
    """
    Return an exact matching managed Foreman host or None.

    A Foreman search result is accepted only when its returned name or
    certname exactly matches one of the requested names.
    """
    candidates = []
    candidate_set = set()

    for name in names:
        if not is_valid(name):
            continue

        value = str(name).strip()
        normalized = value.lower()

        if normalized not in candidate_set:
            candidates.append(
                value
            )
            candidate_set.add(
                normalized
            )

    if not candidates:
        return None

    for candidate in candidates:
        try:
            response = requests.get(
                _api_url("api/hosts"),
                auth=(
                    vars.USER,
                    vars.PASSWORD,
                ),
                headers=HEADERS,
                params={
                    "search": 'name = "{}"'.format(
                        candidate
                    ),
                    "per_page": 100,
                },
                verify=vars.VERIFY_SSL,
                timeout=REQUEST_TIMEOUT,
            )

            response.raise_for_status()
            data = response.json()

            if not isinstance(data, dict):
                raise RuntimeError(
                    "Foreman host search for '{}' returned "
                    "unexpected JSON.".format(
                        candidate
                    )
                )

            results = data.get(
                "results",
                [],
            )

        except requests.exceptions.ConnectionError as exc:
            raise ConnectionError(
                "Connection to Foreman failed while looking up "
                "host '{}'".format(
                    candidate
                )
            ) from exc

        except requests.exceptions.Timeout as exc:
            raise TimeoutError(
                "Foreman host lookup timed out for '{}'".format(
                    candidate
                )
            ) from exc

        except requests.exceptions.RequestException as exc:
            raise RuntimeError(
                "Foreman host lookup failed for '{}': {}".format(
                    candidate,
                    exc,
                )
            ) from exc

        exact_matches = []

        for host in results:
            returned_names = {
                str(
                    host.get(
                        "name",
                        "",
                    )
                ).strip().lower(),
                str(
                    host.get(
                        "certname",
                        "",
                    )
                ).strip().lower(),
            }

            returned_names.discard(
                ""
            )

            if returned_names.intersection(
                candidate_set
            ):
                exact_matches.append(
                    host
                )

        if exact_matches:
            if len(exact_matches) > 1:
                print(
                    "WARNING: Foreman returned {} exact matches "
                    "for '{}'. Using host ID {}.".format(
                        len(exact_matches),
                        candidate,
                        exact_matches[0].get(
                            "id",
                            "Unknown",
                        ),
                    )
                )

            match = exact_matches[0]
            host_id = match.get(
                "id"
            )

            if not host_id:
                raise RuntimeError(
                    "Foreman returned an exact host match for '{}', "
                    "but the result contained no host ID.".format(
                        candidate
                    )
                )

            full_host = get_host_by_id(
                host_id
            )

            if (
                not is_valid(
                    full_host.get("type")
                )
                and is_valid(
                    match.get("type")
                )
            ):
                full_host["type"] = (
                    match.get("type")
                )

            return full_host

        if results:
            returned = [
                str(
                    item.get(
                        "name",
                        "Unknown",
                    )
                )
                for item in results
            ]

            print(
                "Foreman lookup for '{}' returned non-exact "
                "result(s): {}. Ignoring them.".format(
                    candidate,
                    ", ".join(returned),
                )
            )

    return None


def get_host_by_id(host_id):
    """
    Return a host through Foreman's normal managed-host API.

    A malformed Host::Base/type=nil database record is expected not to
    be available through this endpoint.
    """
    try:
        response = requests.get(
            _api_url(
                "api/hosts/{}".format(
                    host_id
                )
            ),
            auth=(
                vars.USER,
                vars.PASSWORD,
            ),
            headers=HEADERS,
            verify=vars.VERIFY_SSL,
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()
        data = response.json()

        if not isinstance(data, dict):
            raise RuntimeError(
                "Foreman host ID {} returned unexpected JSON.".format(
                    host_id
                )
            )

        if isinstance(
            data.get("host"),
            dict,
        ):
            data = data["host"]

        return data

    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError(
            "Connection failed while reading Foreman host ID "
            "{}: {}".format(
                host_id,
                exc,
            )
        ) from exc

    except requests.exceptions.Timeout as exc:
        raise RuntimeError(
            "Timeout while reading Foreman host ID {}: {}".format(
                host_id,
                exc,
            )
        ) from exc

    except requests.exceptions.RequestException as exc:
        raise RuntimeError(
            "Unable to retrieve Foreman host ID {} through "
            "/api/hosts/{}: {}".format(
                host_id,
                host_id,
                exc,
            )
        ) from exc


def verify_created_managed_host(
    response,
    expected_names,
    expected_organization_id=None,
    expected_location_id=None,
):
    """
    Verify that HTTP 201 produced a real managed Foreman host.

    A missing STI 'type' field in the API response is acceptable on this
    Foreman version. The decisive test is whether the newly created host
    can be retrieved through /api/hosts/<id> and has the expected managed
    state, name, organization, and location.
    """
    if response.status_code != 201:
        raise RuntimeError(
            "Cannot verify host creation because Foreman returned "
            "HTTP {} instead of 201.".format(
                response.status_code
            )
        )

    post_host = _response_host_data(
        response
    )

    host_id = post_host.get(
        "id"
    )
    post_type = post_host.get(
        "type"
    )

    if not host_id:
        raise RuntimeError(
            "Foreman returned HTTP 201 but the creation response "
            "contained no host ID."
        )

    print(
        "Foreman returned HTTP 201 for host ID {}.".format(
            host_id
        )
    )

    if (
        post_type is not None
        and post_type != "Host::Managed"
    ):
        raise RuntimeError(
            "Foreman created host ID {}, but POST returned "
            "type={!r}; expected 'Host::Managed'.".format(
                host_id,
                post_type,
            )
        )

    if post_type is None:
        print(
            "Foreman POST response for host ID {} did not include "
            "the STI type. Validating through /api/hosts/{}."
            .format(
                host_id,
                host_id,
            )
        )

    verified_host = None
    last_error = None

    for attempt in range(
        1,
        POST_CREATE_VERIFY_ATTEMPTS + 1,
    ):
        try:
            print(
                "Post-create verification attempt {}/{} for "
                "Foreman host ID {}...".format(
                    attempt,
                    POST_CREATE_VERIFY_ATTEMPTS,
                    host_id,
                )
            )

            verified_host = get_host_by_id(
                host_id
            )

            print(
                "Foreman host ID {} is visible through "
                "/api/hosts/{}.".format(
                    host_id,
                    host_id,
                )
            )

            break

        except Exception as exc:
            last_error = exc

            if attempt < POST_CREATE_VERIFY_ATTEMPTS:
                print(
                    "Post-create verification attempt {}/{} failed "
                    "for Foreman host ID {}: {}. Retrying in {} "
                    "second(s)...".format(
                        attempt,
                        POST_CREATE_VERIFY_ATTEMPTS,
                        host_id,
                        exc,
                        POST_CREATE_VERIFY_DELAY,
                    )
                )

                time.sleep(
                    POST_CREATE_VERIFY_DELAY
                )

    if verified_host is None:
        raise RuntimeError(
            "Foreman returned HTTP 201 and host ID {}, but the "
            "new host could not be retrieved through /api/hosts/{} "
            "after {} attempts. Last error: {}. This strongly "
            "indicates a hidden/malformed Foreman host record such "
            "as Host::Base with type=nil.".format(
                host_id,
                host_id,
                POST_CREATE_VERIFY_ATTEMPTS,
                last_error,
            )
        )

    candidate_set = set()

    for name in expected_names:
        if is_valid(name):
            candidate_set.add(
                str(name).strip().lower()
            )

    returned_names = {
        str(
            verified_host.get(
                "name",
                "",
            )
        ).strip().lower(),
        str(
            verified_host.get(
                "certname",
                "",
            )
        ).strip().lower(),
    }

    returned_names.discard(
        ""
    )

    if (
        candidate_set
        and not returned_names.intersection(
            candidate_set
        )
    ):
        raise RuntimeError(
            "Post-create verification for Foreman host ID {} "
            "failed: returned name/certname {} does not match "
            "expected name(s) {}.".format(
                host_id,
                sorted(returned_names),
                sorted(candidate_set),
            )
        )

    managed = verified_host.get(
        "managed"
    )

    if managed is not True:
        raise RuntimeError(
            "Post-create verification for Foreman host ID {} "
            "failed: managed={!r}; expected True.".format(
                host_id,
                managed,
            )
        )

    get_type = verified_host.get(
        "type"
    )

    if (
        get_type is not None
        and get_type != "Host::Managed"
    ):
        raise RuntimeError(
            "Post-create verification for Foreman host ID {} "
            "failed: GET returned type={!r}; expected "
            "'Host::Managed'.".format(
                host_id,
                get_type,
            )
        )

    if expected_organization_id is not None:
        actual_org = verified_host.get(
            "organization_id"
        )

        if str(actual_org) != str(
            expected_organization_id
        ):
            raise RuntimeError(
                "Post-create verification for Foreman host ID {} "
                "failed: organization_id={!r}; expected {!r}."
                .format(
                    host_id,
                    actual_org,
                    expected_organization_id,
                )
            )

    if expected_location_id is not None:
        actual_location = verified_host.get(
            "location_id"
        )

        if str(actual_location) != str(
            expected_location_id
        ):
            raise RuntimeError(
                "Post-create verification for Foreman host ID {} "
                "failed: location_id={!r}; expected {!r}."
                .format(
                    host_id,
                    actual_location,
                    expected_location_id,
                )
            )

    verified_host = dict(
        verified_host
    )

    verified_host["_post_type"] = post_type
    verified_host["_get_type"] = get_type
    verified_host["_api_visible"] = True
    verified_host["_post_create_verified"] = True

    return verified_host


def describe_host(host):
    """Return concise Foreman identity and verification information."""
    if not isinstance(
        host,
        dict,
    ):
        return "No Foreman host details available"

    organization = (
        host.get("organization_name")
        or _nested_name(
            host.get("organization")
        )
        or "Unknown"
    )

    location = (
        host.get("location_name")
        or _nested_name(
            host.get("location")
        )
        or "Unknown"
    )

    host_type = (
        host.get("type")
        or host.get("_get_type")
        or host.get("_post_type")
        or "Not returned by API"
    )

    managed = host.get(
        "managed",
        "Unknown",
    )

    api_visible = host.get(
        "_api_visible",
        True,
    )

    return (
        "ID={id}, Name={name}, Type={type}, Managed={managed}, "
        "APIVisible={api_visible}, Organization={org}, "
        "Location={location}".format(
            id=host.get(
                "id",
                "Unknown",
            ),
            name=host.get(
                "name",
                "Unknown",
            ),
            type=host_type,
            managed=managed,
            api_visible=api_visible,
            org=organization,
            location=location,
        )
    )


def _nested_name(value):
    """Return name from a nested Foreman API object."""
    if isinstance(
        value,
        dict,
    ):
        return value.get(
            "name"
        )

    return None


def is_duplicate_host_response(response):
    """Return True only for Foreman's duplicate-host-name HTTP 422."""
    if response.status_code != 422:
        return False

    messages = []

    try:
        data = response.json()

        if not isinstance(
            data,
            dict,
        ):
            data = {}

        error = data.get(
            "error",
            {},
        )

        if not isinstance(
            error,
            dict,
        ):
            error = {}

        errors = error.get(
            "errors",
            {},
        )

        if not isinstance(
            errors,
            dict,
        ):
            errors = {}

        name_errors = errors.get(
            "name",
            [],
        )

        full_messages = error.get(
            "full_messages",
            [],
        )

        if isinstance(
            name_errors,
            list,
        ):
            messages.extend(
                str(item)
                for item in name_errors
            )
        elif name_errors:
            messages.append(
                str(name_errors)
            )

        if isinstance(
            full_messages,
            list,
        ):
            messages.extend(
                str(item)
                for item in full_messages
            )
        elif full_messages:
            messages.append(
                str(full_messages)
            )

    except (
        TypeError,
        ValueError,
        AttributeError,
    ):
        pass

    messages.append(
        response.text or ""
    )

    combined = " ".join(
        messages
    ).lower()

    return (
        "name has already been taken" in combined
        or "has already been taken" in combined
    )


def create_host(payload):
    """POST one host to Foreman."""
    return requests.post(
        _api_url("api/hosts"),
        json=payload,
        auth=(
            vars.USER,
            vars.PASSWORD,
        ),
        headers=HEADERS,
        verify=vars.VERIFY_SSL,
        timeout=REQUEST_TIMEOUT,
    )


def post_job_invocation(payload):
    """Create a Foreman job invocation."""
    return requests.post(
        _api_url(
            "api/v2/job_invocations"
        ),
        json=payload,
        auth=(
            vars.USER,
            vars.PASSWORD,
        ),
        headers=HEADERS,
        verify=vars.VERIFY_SSL,
        timeout=REQUEST_TIMEOUT,
    )


def get_scope_ids():
    """Return configured organization and location IDs."""
    organization_id = get_cached_resource_id(
        "api/organizations",
        vars.ORG_NAME,
    )

    location_id = get_cached_resource_id(
        "api/locations",
        vars.LOCATION_NAME,
    )

    return (
        organization_id,
        location_id,
    )


def gethost_parameters(
    parameter,
    ntp1,
    ntp2,
):
    """Build Foreman host parameters."""
    result = []

    if is_valid(parameter):
        for item in str(
            parameter
        ).split(","):
            parts = item.split(
                "=",
                1,
            )

            if len(parts) == 2:
                result.append({
                    "name": parts[0].strip(),
                    "value": parts[1].strip(),
                })

    if is_valid(ntp1):
        result.append({
            "name": "ntp-server",
            "value": ntp1,
        })

    if is_valid(ntp2):
        result.append({
            "name": "ntp2",
            "value": ntp2,
        })

    return result


def gethostgroup(
    subsystems,
    function,
    variation,
):
    """Return mapped Foreman hostgroup name."""
    mapping = "{}{}{}".format(
        subsystems,
        function,
        variation,
    )

    return vars.hg_map.get(
        mapping
    )