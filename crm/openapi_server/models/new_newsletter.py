# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator  # noqa: F401
from crm.openapi_server.models.connection import Connection


class NewNewsletter(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    NewNewsletter - a model defined in OpenAPI

        id: The id of this NewNewsletter [Optional].
        name: The name of this NewNewsletter.
        connection: The connection of this NewNewsletter.
        text: The text of this NewNewsletter.
        date_run: The date_run of this NewNewsletter.
        client_ids: The client_ids of this NewNewsletter [Optional].
        tag_ids: The tag_ids of this NewNewsletter [Optional].
    """

    id: Optional[object] = Field(alias="id", default=None)
    name: object = Field(alias="name")
    connection: Connection = Field(alias="connection")
    text: object = Field(alias="text")
    date_run: object = Field(alias="date_run")
    client_ids: Optional[object] = Field(alias="clientIds", default=None)
    tag_ids: Optional[object] = Field(alias="tagIds", default=None)

    class Config:
        arbitrary_types_allowed = True

    @validator("text")
    def text_max_length(cls, value):
        assert len(value) <= 4096
        return value

NewNewsletter.update_forward_refs()