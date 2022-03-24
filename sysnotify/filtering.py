"""Common functions."""

from collections import defaultdict
from datetime import datetime
from ipaddress import ip_address
from re import fullmatch
from typing import Iterable

from sysnotify.typing import Connections


__all__ = ['failed_connections', 'successful_connections']


VERIFY_ERROR = r'(.+):\d+ VERIFY ERROR: .+ CN=([0-9.]+)(?:, .+|$)'
VERIFY_OK = r'(.+):\d+ VERIFY OK: .+ CN=([0-9.]+)(?:, .+|$)'


def filter_connections(regex: str, records: Iterable[dict]) -> Connections:
    """Returns a dict of OpenVPN keys that match the regular expression
    with the respective datetime and IP address.
    """

    result = defaultdict(dict)

    for record in records:
        if match := fullmatch(regex, record['MESSAGE']):
            ip, key = match.groups()
            timestamp = datetime.fromtimestamp(
                record['__REALTIME_TIMESTAMP'] / 1_000_000
            )
            result[key][timestamp] = ip_address(ip)

    return dict(result)


def failed_connections(records: Iterable[dict]) -> Connections:
    """Returns a dict of OpenVPN keys that failed to connect
    with the respective datetime and IP address.
    """

    return filter_connections(VERIFY_ERROR, records)


def successful_connections(records: Iterable[dict]) -> Connections:
    """Returns a dict of OpenVPN keys that successfully connected
    with the respective datetime and IP address.
    """

    return filter_connections(VERIFY_OK, records)
