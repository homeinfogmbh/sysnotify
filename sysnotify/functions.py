"""Common functions."""

from collections import defaultdict
from datetime import datetime
from ipaddress import IPv4Address, IPv6Address, ip_address
from re import fullmatch
from typing import Union

from hwdb import System

from sysnotify.journalctl import journalctl


IPAddress = Union[IPv4Address, IPv6Address]
OPENVPN_SERVER = 'openvpn-server@terminals.service'
REGEX = (
    r'(.+):\d+ VERIFY ERROR: depth=\d, error=certificate has expired: '
    r'CN=(.+), serial=\d+'
)


def systems_to_migrate_to_wg():
    """Selects systems to migrate to WireGuard."""

    System.select(cascade=True).where(System.pubkey >> None)


def failed_connection_ips(
        unit: str = OPENVPN_SERVER,
        since: datetime | str = 'today'
) -> dict[str, dict[datetime, IPAddress]]:
    """Returns a dict of OpenVPN keys that failed to connect
    with the respective date and IP address.
    """

    result = defaultdict(dict)

    for record in journalctl(unit, since=since, all=True):
        if match := fullmatch(REGEX, record['MESSAGE']):
            ip, key = match.groups()
            timestamp = datetime.fromtimestamp(
                record['__REALTIME_TIMESTAMP'] / 1_000_000
            )
            result[key][timestamp] = ip_address(ip)

    return dict(result)
