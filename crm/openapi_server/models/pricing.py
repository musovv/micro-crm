from enum import Enum
from uuid import UUID

from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator, StringConstraints  # noqa: F401

from crm.openapi_server.models.connection import Connection
from crm.openapi_server.models.connection_type import ConnectionType
from crm.openapi_server.models.setting import CurrencyEnum


class DiscountTypeEnum(str, Enum):
    YEARLY = 'yearly'
    MONTHLY = 'monthly'
    HALF_YEARLY = 'half-yearly'


class Pricing(BaseModel):
    id: UUID = Field(alias="id")
    connection_type: ConnectionType = Field(alias="connection_type")
    price: float = Field(alias="price", gt=0)
    currency: CurrencyEnum = Field(alias="currency", default=CurrencyEnum.USD)
    discount: int = Field(alias="discount", ge=0, lt=80)
    discount_type: DiscountTypeEnum = Field(alias="discount_type")
