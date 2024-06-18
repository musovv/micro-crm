# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from enum import Enum
from typing import Any, Dict, List, Optional, Annotated  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator, StringConstraints  # noqa: F401


class ConnectionTypeEnum(str, Enum):
    telegramBot = 'telegramBot'
    telegramPersonal = 'telegramPersonal'
    whatsapp = 'whatsapp'
    instagram = 'instagram'


class ConnectionType(BaseModel):
    name: Annotated[str, StringConstraints(min_length=1, max_length=64)]
    code: ConnectionTypeEnum

    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True
