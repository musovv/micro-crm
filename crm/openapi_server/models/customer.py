# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator, field_validator, conlist  # noqa: F401
from crm.openapi_server.models.image import Image
from crm.openapi_server.models.note import Note
from crm.openapi_server.models.tag import Tag


class Customer(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    Customer - a model defined in OpenAPI

        id: The id of this Customer [Optional].
        tg_login: The login from telegrams Customer. [Optional]
        tg_user_id: The user_id from telegrams customer. [Optional]
        fullname: The fullname of this Customer.
        mobile_number1: The mobile_number1 of this Customer.
        mobile_number2: The mobile_number2 of this Customer [Optional].
        phone_number: The phone_number of this Customer [Optional].
        email: The email of this Customer [Optional].
        photo: The photo of this Customer [Optional].
        status: The status of this Customer [Optional].
        owner_id: The owner_id of this Customer [Optional].
        tags: The tags of this Customer [Optional].
        notes: The notes of this Customer [Optional].
    """

    id: Optional[object] = Field(alias="id", default=None)
    tg_login: Optional[object] = Field(alias="tg_login", default=None)
    tg_user_id: Optional[int] = Field(alias="tg_user_id", default=None)
    fullname: object = Field(alias="fullname")
    mobile_number1: int = Field(alias="mobile_number1")
    mobile_number2: Optional[int] = Field(alias="mobile_number2", default=None)
    phone_number: Optional[int] = Field(alias="phone_number", default=None)
    email: Optional[object] = Field(alias="email", default=None)
    photo: Optional[Image] = Field(alias="photo", default=None)
    status: Optional[int] = Field(alias="status", default=None)
    tags: Optional[List[Tag]] = Field(alias="tags", default=None)
    notes: Optional[List[Note]] = Field(alias="notes", default=None)

    # class Config:
    #     arbitrary_types_allowed = True

    @field_validator("tg_login")
    def login_min_length(cls, value):
        if value is None:
            return value
        assert len(value) >= 1
        return value

    @field_validator("tg_login")
    def login_max_length(cls, value):
        if value is None:
            return value
        assert len(value) <= 64
        return value

    @field_validator("tg_user_id")
    def tg_user_id_max(cls, value):
        if value is None:
            return value
        assert 0 < value <= 99999999999999999999
        return value

    @field_validator("fullname")
    def fullname_min_length(cls, value):
        assert len(value) >= 1
        return value

    @field_validator("fullname")
    def fullname_max_length(cls, value):
        assert len(value) <= 510
        return value

    @field_validator("mobile_number1")
    def mobile_number1_max(cls, value):
        assert value <= 999999999999999
        return value

    @field_validator("mobile_number1")
    def mobile_number1_min(cls, value):
        assert value >= 10000
        return value

    @field_validator("mobile_number2")
    def mobile_number2_max(cls, value):
        if value is None:
            return value
        assert value <= 999999999999999
        return value

    @field_validator("mobile_number2")
    def mobile_number2_min(cls, value):
        if value is None:
            return value
        assert value >= 10000
        return value

    @field_validator("phone_number")
    def phone_number_max(cls, value):
        if value is None:
            return value
        assert value <= 999999999999999
        return value

    @field_validator("phone_number")
    def phone_number_min(cls, value):
        if value is None:
            return value
        assert value >= 10000
        return value

    @field_validator("email")
    def email_max_length(cls, value):
        if value is None:
            return value
        assert len(value) <= 255
        return value

Customer.update_forward_refs()
