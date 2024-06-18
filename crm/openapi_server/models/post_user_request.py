# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator  # noqa: F401


class PostUserRequest(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    PostUserRequest - a model defined in OpenAPI

        first_name: The first_name of this PostUserRequest.
        last_name: The last_name of this PostUserRequest.
        email: The email of this PostUserRequest.
        date_of_birth: The date_of_birth of this PostUserRequest.
    """

    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    email: str = Field(alias="email")
    date_of_birth: date = Field(alias="dateOfBirth")

PostUserRequest.update_forward_refs()