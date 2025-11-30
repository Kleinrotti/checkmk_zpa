#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2025 Kleinrotti

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

# Sample agent output
# <name>|<enabled>|<status>|<upgradeStatus>|<currentVersion>
# <<<zpa_connector:sep(124)>>>
# test123|True|ZPN_STATUS_AUTHENTICATED|COMPLETE|24.692.3

from dataclasses import dataclass

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Result,
    Service,
    State,
)


@dataclass(frozen=True)
class Connector():
    name: str
    enabled: bool
    status: str
    upgradeStatus: str
    currentVersion: str


control_state_mapping = {
    "UNKNOWN": (State.CRIT, "Unknown"),
    "ZPN_STATUS_AUTHENTICATED": (State.OK, "Authenticated"),
    "ZPN_STATUS_DISCONNECTED": (State.CRIT, "Disconnected")
}

upgrade_state_mapping = {
    "UNKNOWN": State.UNKNOWN,
    "COMPLETE": State.OK,
    "IN_PROGRESS": State.WARN,
    "FAILED": State.CRIT,
    "PARTIAL_FAILURE": State.CRIT,
    "RESTARTING": State.WARN,
    "REMOVAL_IN_PROGRESS": State.WARN
}


def parse_zpa_connector(string_table):
    return [
        Connector(name, enabled, status, upgradeStatus, currentVersion) for
        name, enabled, status, upgradeStatus, currentVersion in string_table
    ]


def discovery_zpa_connector(section) -> DiscoveryResult:
    for service in section:
        if service.enabled:
            yield Service(item=service.name)


def check_zpa_connector(item, section) -> CheckResult:
    service = next((sec for sec in section if item == sec.name), None)
    if not service:
        return
    yield Result(
        state=control_state_mapping.get(service.status, State.UNKNOWN)[0],
        summary=f"Enabled: {service.enabled}, Status: {control_state_mapping.get(service.status, 'UNKNOWN')[1]}",
    )
    yield Result(
        state=upgrade_state_mapping.get(service.upgradeStatus, State.UNKNOWN),
        notice=f"Version: {service.currentVersion}, Upgrade status: {service.upgradeStatus}"
    )


agent_section_zpa_connector = AgentSection(
    name="zpa_connector",
    parse_function=parse_zpa_connector,
    parsed_section_name="zpa_connector",
)

check_plugin_zpa_connector = CheckPlugin(
    name="zpa_connector",
    service_name="App Connector %s",
    discovery_function=discovery_zpa_connector,
    check_function=check_zpa_connector,
)
