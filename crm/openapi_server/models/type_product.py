# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from enum import Enum
from typing import Any, Dict, List, Optional, Annotated, Set  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator, StringConstraints, conint, constr


class TypeProductEnum(Enum):
    Other = 'Other'
    FoodCommodities = 'FoodCommodities'
    NonFoodProducts = 'NonFoodProducts'
    Service = 'Service'
    Product = 'Product'


class TypeProduct(BaseModel):
    name: TypeProductEnum
    code: Annotated[int, conint(ge=0, le=4)]

    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True


TypeProduct.update_forward_refs()
