# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator, field_validator  # noqa: F401
from openapi_server.models.type_resource import TypeResource


class Permission(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    Permission - a model defined in OpenAPI

        id: The id of this Permission.
        name: The name of this Permission.
        resource_type: The resource_type of this Permission.
        value: The value of this Permission.
    """

    id: object = Field(alias="id")
    name: object = Field(alias="name")
    description: Optional[str] = Field(alias="description")
    type_resource: TypeResource = Field(alias="resource_type")
    access: object = Field(alias="value")
    access_level: object = Field(alias="access_level")
    privilege: object = Field(alias="privilege")


    @field_validator("name")
    def name_min_length(cls, value):
        assert len(value) >= 1
        return value

    @field_validator("name")
    def name_max_length(cls, value):
        assert len(value) <= 64
        return value

    @field_validator("description")
    def desc_max_length(cls, value):
        assert len(value) <= 256
        return value

    @field_validator("access")
    def value_max(cls, value):
        assert value <= 1
        return value

    @field_validator("access")
    def value_min(cls, value):
        assert value >= 0
        return value

Permission.update_forward_refs()
