# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional, Annotated
from uuid import UUID

from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator, StringConstraints  # noqa: F401


class Image(BaseModel):
    """
    Image - a model defined in OpenAPI

        id: The id of this Image [Optional].
        filename: The filename of this Image [Optional].
        body: The body of this Image [Optional].
        format: The format of this Image [Optional].
        _date: The _date of this Image [Optional].
        main: The main of this Image [Optional].
    """

    id: Optional[UUID] = None
    filename: Optional[Annotated[str, StringConstraints(min_length=1, max_length=256)]] = None
    body: Optional[Annotated[str, StringConstraints(min_length=1, max_length=4000000)]] = None
    format:  Optional[Annotated[str, StringConstraints(min_length=2, max_length=24)]] = None
    date: Optional[datetime] = None
    main: Optional[bool] = None

    class Config:
        arbitrary_types_allowed = True


Image.update_forward_refs() # TODO what is this?
