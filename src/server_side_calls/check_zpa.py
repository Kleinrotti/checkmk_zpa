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


from collections.abc import Iterator
from pydantic import BaseModel

from cmk.server_side_calls.v1 import (
    HostConfig,
    Secret,
    SpecialAgentCommand,
    SpecialAgentConfig,
)


class Params(BaseModel):
    """Params validator"""
    clientid: str | None = None
    clientsecret: Secret | None = None
    customerid: str | None = None


def _agent_zpa_arguments(
    params: Params, host_config: HostConfig
) -> Iterator[SpecialAgentCommand]:
    command_arguments: list[str | Secret] = []
    command_arguments += ["-i", params.clientid]
    command_arguments += ["-s", params.clientsecret.unsafe()]
    command_arguments += ["-c", params.customerid]
    yield SpecialAgentCommand(command_arguments=command_arguments)


special_agent_zpa = SpecialAgentConfig(
    name="zpa",
    parameter_parser=Params.model_validate,
    commands_function=_agent_zpa_arguments,
)
