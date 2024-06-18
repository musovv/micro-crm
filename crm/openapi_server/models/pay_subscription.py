from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field

from crm.openapi_server.models.pricing import Pricing
from crm.openapi_server.models.setting import CurrencyEnum


class PaySubscription(BaseModel):
    """Model definition for PaySubscription."""

    subscription_id: str = Field(alias="subscription_id")
    price: Pricing = Field(alias="price")
    date_start: date = Field(alias="date_start")
    date_end: date = Field(alias="date_end")

    class Config:
        arbitrary_types_allowed = True


PaySubscription.update_forward_refs()


class PaySubscriptions(BaseModel):
    """Model definition for PaySubscription."""
    subscriptions: list[PaySubscription] = Field(alias="subscriptions")
    total_amount: float = Field(alias="total_amount", gt=0)

    class Config:
        arbitrary_types_allowed = True


PaySubscriptions.update_forward_refs()
