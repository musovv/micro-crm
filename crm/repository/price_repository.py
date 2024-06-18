from abc import ABC

from crm.business_service.bases import PricingBase
from crm.repository.models import PricingModel
from crm.repository.repository import Repository


class PriceRepository(Repository, ABC):
    def __init__(self, session):
        self.session = session

    def add(self, org_id, user_id, **payload: dict):
        pass

    def get(self, id_, org_id, user_id):
        pass

    def list(self, org_id, user_id, limit=10, **filters):
        # miss the org_id and user_id in the query
        prices = self.session.query(PricingModel).limit(limit).all()
        return [PricingBase(**p.dict()) for p in prices]

    def update(self, id_, org_id, user_id, **payload):
        pass

    def delete(self, id_, org_id, user_id):
        pass