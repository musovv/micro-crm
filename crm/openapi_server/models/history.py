from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from crm.openapi_server.models.setting import CurrencyEnum


class History(BaseModel):
    subscription_id: Optional[str] = Field(alias="subscription_id")
    invoice_id: Optional[str] = Field(alias="invoice_id")
    price: float = Field(alias="price", gt=0)
    discount: int = Field(alias="discount", ge=0, lt=80)
    currency: CurrencyEnum = Field(alias="currency")
    date_start: date = Field(alias="date_start")
    date_end: date = Field(alias="date_end")

    class Config:
        arbitrary_types_allowed = True


History.update_forward_refs()
