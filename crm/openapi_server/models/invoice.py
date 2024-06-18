from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from crm.openapi_server.models.history import History
from crm.openapi_server.models.setting import CurrencyEnum


class Invoice(BaseModel):
    id: Optional[str] = Field(alias="id")
    invoice_number: str = Field(alias="invoice_number")
    invoice_date: date = Field(alias="invoice_date")
    total_amount: float = Field(alias="total_amount")
    currency: CurrencyEnum = Field(alias="currency")
    discount: int = Field(alias="discount", ge=0, le=80)
    start_date_subscription: date = Field(alias="start_date_subscription")
    end_date_subscription: date = Field(alias="end_date_subscription")
    buyer_name: str = Field(alias="buyer_name")
    link_invoice: str = Field(alias="link_invoice")
    subscriptions: list[History] = Field(alias="subscriptions")

    class Config:
        arbitrary_types_allowed = True


Invoice.update_forward_refs()