"""Common type hints."""

from datetime import datetime
from ipaddress import IPv4Address, IPv6Address
from typing import Union


__all__ = ['Connections', 'IPAddress']


IPAddress = Union[IPv4Address, IPv6Address]
Connections = dict[str, dict[datetime, IPAddress]]
