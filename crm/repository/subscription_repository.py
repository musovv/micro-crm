from abc import ABC

from crm.business_service.bases import SubscriptionBase
from crm.repository.models import SubscriptionModel, ConnectionModel
from crm.repository.repository import Repository


class SubscriptionRepository(Repository, ABC):
    def __init__(self, session):
        self.session = session

    def add(self, org_id, user_id, **payload: dict):
        pass

    def _get(self, sub_id, org_id, user_id):
        sub = (self.session.query(SubscriptionModel).join(SubscriptionModel.connection)
         .filter(ConnectionModel.organization_id == org_id, SubscriptionModel.id == sub_id)
         .first())
        if sub is None:
            raise ValueError(f'Subscription with id {sub_id} not found')
        return sub

    def get(self, sub_id, org_id, user_id) -> SubscriptionBase:
        entity = self._get(sub_id, org_id, user_id)
        return SubscriptionBase(**entity.dict())

    def list(self, org_id, user_id, limit, **filters):
        res = (self.session.query(SubscriptionModel).join(ConnectionModel).filter(ConnectionModel.organization_id == org_id)
         .filter_by(**filters).limit(limit).all())
        return [SubscriptionBase(**sub.dict()) for sub in res]

    def update(self, sub_id, org_id, user_id, **payload) -> SubscriptionBase:
        payload.pop('id', None)  # TODO add decorator to remove id from payload for update/create methods

        entity = self._get(sub_id, org_id, user_id)
        for key, value in payload.items():
            setattr(entity, key, value)

        return SubscriptionBase(**entity.dict())

    def delete(self, sub_id, org_id, user_id):
        pass