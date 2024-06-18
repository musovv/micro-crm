# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re
from typing import Any, Dict, List, Optional, Annotated  # noqa: F401
from uuid import UUID

from annotated_types import Gt
from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator, StringConstraints  # noqa: F401

from crm.openapi_server.models.image import Image
from crm.openapi_server.models.catalog import Catalog
from crm.openapi_server.models.type_product import TypeProduct


class NewProduct(BaseModel):
    """
    NewProduct - a model defined in OpenAPI

        id: The id of this NewProduct [Optional].
        name: The name of this NewProduct.
        description: The description of this NewProduct [Optional].
        product_type: The product_type of this NewProduct.
        price: The price of this NewProduct.
        currency: The currency of this NewProduct.
        vat: The vat of this NewProduct [Optional].
        code_product: The code_product of this NewProduct [Optional].
        catalogs: The catalogs of this NewProduct [Optional].
        images: The images of this NewProduct [Optional].
    """

    # id: Optional[Annotated[str, StringConstraints(min_length=36, max_length=36, pattern='')]] = None
    id: Optional[UUID] = None  # check if it is correct FIXME
    name: Annotated[str, StringConstraints(min_length=1, max_length=64)]
    description: Optional[Annotated[str, StringConstraints(min_length=1, max_length=512)]] = None
    product_type: TypeProduct
    price: Annotated[float, Gt(0)]
    currency: Annotated[str, StringConstraints(min_length=3, max_length=3)]
    vat:  Optional[Annotated[str, StringConstraints(min_length=1, max_length=8)]] = None
    code_product: Optional[Annotated[str, StringConstraints(min_length=10, max_length=16)]] = None
    catalogs: List[Catalog]
    images: List[Image]

    class Config:
        arbitrary_types_allowed = True


NewProduct.update_forward_refs()
