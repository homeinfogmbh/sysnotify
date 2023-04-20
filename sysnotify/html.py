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

    header = SubElement(body, 'h1')
    header.text = title
    table = SubElement(body, 'table')
    table_head = SubElement(table, 'tr')
    header_system_id = SubElement(table_head, 'th')
    header_system_id.text = 'System'
    header_os = SubElement(table_head, 'th')
    header_os.text = 'OS'
    header_deployment_id = SubElement(table_head, 'th')
    header_deployment_id.text = 'Deployment'
    header_address = SubElement(table_head, 'th')
    header_address.text = 'Address'
    header_timestamp = SubElement(table_head, 'th')
    header_timestamp.text = 'Timestamp'
    header_ip_address = SubElement(table_head, 'th')
    header_ip_address.text = 'IP address'

    for connection in connections:
        add_connection(table, connection)


def add_connection(table: Element, connection: SystemConnection) -> None:
    """Adds a system connection to the table."""

    row = SubElement(table, 'tr')
    system_id = SubElement(row, 'td')
    system_id.text = str(connection.system.id)
    system_os = SubElement(row, 'td')
    system_os.text = connection.system.operating_system.value
    deployment_id = SubElement(row, 'td')
    address = SubElement(row, 'td')

    if deployment := connection.system.deployment:
        deployment_id.text = str(deployment.id)
        address.text = str(connection.system.deployment.address)
    else:
        deployment_id.text = 'N/A'
        address.text = 'N/A'

    timestamp = SubElement(row, 'td')
    timestamp.text = connection.timestamp.isoformat()
    ip_address = SubElement(row, 'td')
    ip_address.text = str(connection.ip_address)
