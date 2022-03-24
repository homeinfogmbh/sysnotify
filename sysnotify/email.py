"""Email generation."""

from typing import Iterable, Iterator

from emaillib import EMail

from sysnotify.html import to_html
from sysnotify.typing import SystemConnection


__all__ = ['generate_emails']


def generate_emails(
        recipients: Iterable[str],
        failures: Iterable[SystemConnection],
        connections: Iterable[SystemConnection]
) -> Iterator[EMail]:
    """Generate emails."""

    html = to_html(failures, connections)

    for recipient in recipients:
        yield EMail(
            'OpenVPN systems update', 'noreply@homeinfo.de', recipient,
            html=html
        )
