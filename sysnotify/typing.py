"""Common type hints."""

from datetime import datetime
from ipaddress import IPv4Address, IPv6Address
from typing import NamedTuple, Union

from hwdb import System


__all__ = ['Connections', 'IPAddress', 'SystemConnection']


IPAddress = Union[IPv4Address, IPv6Address]
Connections = dict[str, dict[datetime, IPAddress]]


class SystemConnection(NamedTuple):
    """A system connection."""

    system: System
    timestamp: datetime
    ip_address: IPAddress
