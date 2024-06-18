# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator  # noqa: F401


class NewEmployee(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    NewEmployee - a model defined in OpenAPI

        id: The id of this NewEmployee [Optional].
        login: The login of this NewEmployee [Optional].
        first_name: The first_name of this NewEmployee [Optional].
        last_name: The last_name of this NewEmployee [Optional].
        password: The password of this NewEmployee [Optional].
    """

    id: Optional[object] = Field(alias="id", default=None)
    login: Optional[object] = Field(alias="login", default=None)
    first_name: Optional[object] = Field(alias="first_name", default=None)
    last_name: Optional[object] = Field(alias="last_name", default=None)
    password: Optional[object] = Field(alias="password", default=None)
    type_employee: Optional[object] = Field(alias="type_employee", default=None)

    class Config:
        arbitrary_types_allowed = True

    @validator("login")
    def login_min_length(cls, value):
        assert len(value) >= 5
        return value

    @validator("login")
    def login_max_length(cls, value):
        assert len(value) <= 64
        return value

    @validator("first_name")
    def first_name_min_length(cls, value):
        assert len(value) >= 1
        return value

    @validator("first_name")
    def first_name_max_length(cls, value):
        assert len(value) <= 64
        return value

    @validator("last_name")
    def last_name_min_length(cls, value):
        assert len(value) >= 1
        return value

    @validator("last_name")
    def last_name_max_length(cls, value):
        assert len(value) <= 64
        return value

    @validator("password")
    def password_min_length(cls, value):
        assert len(value) >= 12
        return value

    @validator("password")
    def password_max_length(cls, value):
        assert len(value) <= 64
        return value

NewEmployee.update_forward_refs()