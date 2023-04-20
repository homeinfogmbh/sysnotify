"""HTML text generation."""

from xml.etree.ElementTree import Element, SubElement, tostring

from typing import Iterable

from sysnotify.typing import SystemConnection


__all__ = ['to_html']


def to_html(
        failures: Iterable[SystemConnection],
        connections: Iterable[SystemConnection]
) -> str:
    """Returns the HTML body."""

    body = Element('body')
    add_table(body, 'Failed connections', failures)
    add_table(body, 'Successful connections', connections)
    return tostring(body, encoding='unicode', method='html')


def add_table(
        body: Element,
        title: str,
        connections: Iterable[SystemConnection]
) -> None:
    """Adds a header and table of system information to the body."""

    SubElement(body, 'h1').text = title
    table = SubElement(body, 'table')
    table_head = SubElement(table, 'tr')
    SubElement(table_head, 'th').text = 'System'
    SubElement(table_head, 'th').text = 'OS'
    SubElement(table_head, 'th').text = 'Deployment'
    SubElement(table_head, 'th').text = 'Address'
    SubElement(table_head, 'th').text = 'Timestamp'
    SubElement(table_head, 'th').text = 'IP address'

    for connection in connections:
        add_connection(table, connection)


def add_connection(table: Element, connection: SystemConnection) -> None:
    """Adds a system connection to the table."""

    row = SubElement(table, 'tr')
    SubElement(row, 'td').text = str(connection.system.id)
    SubElement(row, 'td').text = connection.system.operating_system.value
    deployment_id = SubElement(row, 'td')
    address = SubElement(row, 'td')

    if deployment := connection.system.deployment:
        deployment_id.text = str(deployment.id)
        address.text = str(deployment.address)
    else:
        deployment_id.text = 'N/A'
        address.text = 'N/A'

    SubElement(row, 'td').text = connection.timestamp.isoformat()
    SubElement(row, 'td').text = str(connection.ip_address)
