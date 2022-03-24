"""OpenVPN watchdog."""

from configparser import ConfigParser
from datetime import datetime
from typing import Iterable, Iterator

from peewee import Select

from emaillib import Mailer
from hwdb import System

from sysnotify.email import generate_emails
from sysnotify.filtering import failed_connections, successful_connections
from sysnotify.journalctl import journalctl
from sysnotify.typing import Connections, IPAddress, SystemConnection


__all__ = ['check_systems']


CONFIG_FILE = '/usr/local/etc/sysnotify.conf'
OPENVPN_SERVER = 'openvpn-server@terminals.service'


def check_systems() -> None:
    """Checks systems of interest."""

    config = ConfigParser()
    config.read(CONFIG_FILE)
    recipients = map(str.strip, config.get('email', 'recipients').split(','))
    records = list(journalctl(OPENVPN_SERVER, since='today', all=True))
    failures = failed_connections(records)
    connections = successful_connections(records)
    systems = systems_of_interest()
    interested_failures = match(systems, failures)
    interested_connections = match(systems, connections)
    emails = generate_emails(
        recipients,
        interested_failures,
        interested_connections
    )
    Mailer.from_config(config).send(emails)


def match(
        systems: Iterable[System],
        connections: Connections
) -> Iterator[SystemConnection]:
    """Yields system connections."""

    for system in systems:
        try:
            system_connections = connections[system.openvpn.filename]
        except KeyError:
            continue

        yield get_last_connection(system, system_connections)


def get_last_connection(
        system: System,
        connections: dict[datetime, IPAddress]
) -> SystemConnection:
    """Returns the last connection of the given system."""

    for timestamp in sorted(connections.items(), reverse=True):
        return SystemConnection(system, timestamp, connections[timestamp])

    raise KeyError('No system connection found.')


def systems_of_interest() -> Select:
    """Selects systems to migrate to WireGuard."""

    return System.select(cascade=True).where(
        (System.pubkey >> None)
        & (~(System.openvpn >> None))
    )
