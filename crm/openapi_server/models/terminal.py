# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator  # noqa: F401


class Terminal(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    Terminal - a model defined in OpenAPI

        id: The id of this Terminal [Optional].
        type_terminal: The type_terminal of this Terminal [Optional].
        name: The name of this Terminal [Optional].

    """

    id: Optional[object] = Field(alias="id", default=None)
    terminal_type: Optional[object] = Field(alias="terminal_type", default=None)
    name: Optional[object] = Field(alias="name", default=None)
    connection_url: str = Field(alias="connection_url")
    connection_json: object = Field(alias="connection_json")

    class Config:
        arbitrary_types_allowed = True

Terminal.update_forward_refs()