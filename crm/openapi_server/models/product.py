# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional, Annotated  # noqa: F401
from uuid import UUID

from annotated_types import Gt
from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator, StringConstraints  # noqa: F401
from crm.openapi_server.models.image import Image
from crm.openapi_server.models.type_product import TypeProduct


class Product(BaseModel):
    """
    Product - a model defined in OpenAPI

        id: The id of this Product [Optional].
        name: The name of this Product.
        description: The description of this Product [Optional].
        product_type: The product_type of this Product.
        price: The price of this Product.
        currency: The currency of this Product.
        vat: The vat of this Product [Optional].
        code_product: The code_product of this Product [Optional].
        image: The image of this Product [Optional].
    """

    id: Optional[UUID] = None
    name: Annotated[str, StringConstraints(min_length=1, max_length=64)]
    description: Optional[Annotated[str, StringConstraints(min_length=1, max_length=512)]] = None
    product_type: TypeProduct
    price: Annotated[float, Gt(0)]
    currency: Annotated[str, StringConstraints(min_length=3, max_length=3)]
    vat: Optional[Annotated[str, StringConstraints(min_length=1, max_length=8)]] = None
    code_product: Optional[Annotated[str, StringConstraints(min_length=10, max_length=16)]] = None
    image: Image


Product.update_forward_refs()
