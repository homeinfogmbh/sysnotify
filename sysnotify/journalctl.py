"""Functions around journalctl."""

from datetime import datetime
from json import loads
from os import linesep
from subprocess import PIPE, run
from typing import Any, Iterator, Optional, Union


__all__ = ['journalctl']


JOURNALCTL = '/usr/bin/journalctl'


def journalctl(
        unit: Optional[str] = None,
        since: Optional[Union[datetime, str]] = None,
        all: bool = False
) -> Iterator[dict[str, Any]]:
    """Yields lines from the journal."""

    command = [JOURNALCTL, '--no-pager', '--output', 'json']

    if unit is not None:
        command.extend(['-u', unit])

    if since is not None:
        if isinstance(since, datetime):
            since = since.isoformat()

        command.extend(['--since', since])

    if all:
        command.append('-a')

    completed_process = run(command, stdout=PIPE, stderr=PIPE, text=True)

    for line in filter(None, completed_process.stdout.split(linesep)):
        yield loads(line)
