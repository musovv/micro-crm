import datetime
import uuid
from abc import ABC, abstractmethod
from typing import List

from crm.business_service.base import EntityBase
from crm.business_service.bases import InvoiceBase
from crm.repository.models import InvoiceModel, SettingModel, HistoryModel, SubscriptionModel
from crm.repository.repository import Repository


class InvoiceRepository(Repository, ABC):
    def __init__(self, session):
        self.session = session

    def add(self, org_id, user_id, **payload: dict) -> InvoiceBase:
        subs = payload.pop('subscriptions', [])  # PaySubscription
        invoice = InvoiceModel(**payload)
        invoice.invoice_number = f'INV-{datetime.date.today().strftime("%Y%m%d")}-1' # TODO link to settings
        invoice.invoice_date = datetime.date.today()
        invoice.link_invoice = f'https://t.ly/{uuid.uuid4()}'  # TODO: generate link to invoice
        # company name:
        setting = self.session.query(SettingModel).filter(SettingModel.organization_id == org_id).first()
        invoice.buyer_name = setting.company_name
        # organization id:
        invoice.organization_id = org_id
        for s in subs:
            # s = self.session.guery(SubscriptionModel).filter(SubscriptionModel.id == s['subscription_id']).first()
            history = HistoryModel()
            history.subscription_id = s['subscription_id']
            history.currency = s['price']['currency']
            history.price = s['price']['price']
            history.discount = s['price']['discount']
            history.date_start = s['date_start']
            history.date_end = s['date_end']
            invoice.subscriptions.append(history)

        self.session.add(invoice)
        return InvoiceBase(**invoice.dict(), invoice_=invoice)

    def get(self, id_, org_id, user_id) -> EntityBase:
        pass

    def list(self, org_id, user_id, limit=None, **filters) -> List[EntityBase]:
        pass

    def update(self, id_, org_id, user_id, **payload) -> EntityBase:
        pass

    def delete(self, id_, org_id, user_id) -> None:
        pass

