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

from cmk.rulesets.v1 import Title, Help
from cmk.rulesets.v1.form_specs import (
    DictElement,
    Dictionary,
    Password,
    String,
)
from cmk.rulesets.v1.rule_specs import Topic, SpecialAgent


def _valuespec_special_agents_zpa():
    return Dictionary(
        title=Title("Zscaler Private Access via WebAPI"),
        help_text=Help("Monitor ZPA with special agent."),
        elements={
            "clientid": DictElement(
                parameter_form=String(
                    title=Title("Client ID"),
                ),
                required=True,
            ),
            "clientsecret": DictElement(
                parameter_form=Password(
                    title=Title("Client Secret"),
                ),
                required=True,
            ),
            "customerid": DictElement(
                parameter_form=String(
                    title=Title("Customer ID"),
                ),
                required=True,
            ),
        }
    )


rule_spec_zpa_datasource_programs = SpecialAgent(
    name="zpa",
    title=Title("Zscaler Private Access via WebAPI"),
    topic=Topic.CLOUD,
    parameter_form=_valuespec_special_agents_zpa,
    help_text=(
        "This rule selects the ZPA agent instead of the normal Check_MK Agent "
        "which collects the data through the Zscaler Private Access REST API"
    ),
)
