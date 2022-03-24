"""Common functions."""

from collections import defaultdict
from datetime import datetime
from ipaddress import IPv4Address, IPv6Address, ip_address
from re import fullmatch
from typing import Union

from peewee import Select

from hwdb import System

from sysnotify.journalctl import journalctl


IPAddress = Union[IPv4Address, IPv6Address]
OPENVPN_SERVER = 'openvpn-server@terminals.service'
VERIFY_ERROR = r'(.+):\d+ VERIFY ERROR: .+ CN=([0-9.]+)(?:, .+|$)'
VERIFY_OK = r'(.+):\d+ VERIFY OK: .+ CN=([0-9.]+)(?:, .+|$)'


def systems_to_migrate_to_wg() -> Select:
    """Selects systems to migrate to WireGuard."""

    return System.select(cascade=True).where(System.pubkey >> None)


def filter_connections(
        regex: str,
        unit: str = OPENVPN_SERVER,
        since: Union[datetime, str] = 'today'
) -> dict[str, dict[datetime, IPAddress]]:
    """Returns a dict of OpenVPN keys that match the regular expression
    with the respective datetime and IP address.
    """

    result = defaultdict(dict)

    for record in journalctl(unit, since=since, all=True):
        if match := fullmatch(regex, record['MESSAGE']):
            ip, key = match.groups()
            timestamp = datetime.fromtimestamp(
                record['__REALTIME_TIMESTAMP'] / 1_000_000
            )
            result[key][timestamp] = ip_address(ip)

    return dict(result)


def failed_connections(
        unit: str = OPENVPN_SERVER,
        since: Union[datetime, str] = 'today'
) -> dict[str, dict[datetime, IPAddress]]:
    """Returns a dict of OpenVPN keys that failed to connect
    with the respective datetime and IP address.
    """

    return filter_connections(VERIFY_ERROR, unit, since)


def successful_connections(
        unit: str = OPENVPN_SERVER,
        since: Union[datetime, str] = 'today'
) -> dict[str, dict[datetime, IPAddress]]:
    """Returns a dict of OpenVPN keys that successfully connected
    with the respective datetime and IP address.
    """

    return filter_connections(VERIFY_OK, unit, since)
