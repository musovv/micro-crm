# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator  # noqa: F401


class Template(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    Template - a model defined in OpenAPI

        id: The id of this Template [Optional].
        title: The title of this Template [Optional].
        text: The text of this Template [Optional].
        owner_id: The owner_id of this Template [Optional].
    """

    id: Optional[object] = Field(alias="id", default=None)
    title: Optional[object] = Field(alias="title", default=None)
    text: Optional[object] = Field(alias="text", default=None)
    owner_id: Optional[object] = Field(alias="owner_id", default=None)

    class Config:
        arbitrary_types_allowed = True

    @validator("title")
    def title_min_length(cls, value):
        assert len(value) >= 1
        return value

    @validator("title")
    def title_max_length(cls, value):
        assert len(value) <= 128
        return value

    @validator("text")
    def text_min_length(cls, value):
        assert len(value) >= 1
        return value

    @validator("text")
    def text_max_length(cls, value):
        assert len(value) <= 1024
        return value

Template.update_forward_refs()