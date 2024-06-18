from abc import ABC
from datetime import datetime

from crm.business_service.bases import ConnectionBase
from crm.repository.models import CatalogModel, ProductModel, ProductTypeModel, ImageModel, ConnectionModel, \
    ConnectionTypeModel, SubscriptionModel, SubscriptionStatusModel
from crm.repository.repository import Repository


class ConnectionRepository(Repository, ABC):
    def __init__(self, session):
        self.session = session

    def add(self, org_id, user_id, **payload: dict) -> ConnectionBase:
        payload.pop('id', None)

        conn = ConnectionModel(**payload)
        # set connection type
        conn.connection_type = (self.session.query(ConnectionTypeModel)
                                .filter(ConnectionTypeModel.code == payload['connection_type']['code'])
                                .one())
        # set field is_bot
        if not conn.is_bot:
            conn.is_bot = False

        # date_created and date_updated
        if not conn.date_created:
            conn.date_created = conn.date_updated = datetime.now()

        # create subscription
        subscription = SubscriptionModel() # FIXME move data logic to business service due to calc dates and status
        subscription.status = (self.session.query(SubscriptionStatusModel)
                                .filter(SubscriptionStatusModel.code == 'trial')
                                .one())
        subscription.date_start = conn.date_created
        subscription.date_end = subscription.date_start.replace(month=subscription.date_start.month + 1)
        subscription.subscription_included = True

        conn.subscription = subscription
        conn.organization_id = org_id

        self.session.add(conn)
        return ConnectionBase(**conn.dict(), connection_=conn)

    def get(self, id_, org_id, user_id) -> ConnectionBase:
        conn = self._get(id_, org_id, user_id)
        return ConnectionBase(**conn.dict())

    def _get(self, id_, org_id, user_id) -> ConnectionModel:
        conn = (self.session.query(ConnectionModel)
                .filter(ConnectionModel.organization_id == org_id, ConnectionModel.id == id_).first())
        if conn is None:
            raise ValueError(f'Connection with id {id_} not found')
        return conn

    def list(self, org_id, user_id, limit=None, **filters) -> list[ConnectionBase]:
        conns = (self.session.query(ConnectionModel).filter(ConnectionModel.organization_id == org_id)
                 .filter_by(**filters).limit(limit).all())
        return [ConnectionBase(**conn.dict()) for conn in conns]

    def update(self, id_, org_id, user_id, **payload) -> ConnectionBase:
        conn = self._get(id_, org_id, user_id)

        # update connection
        conn_type = payload.pop('connection_type', None)
        if conn_type is not None:
            conn.connection_type = (self.session.query(ConnectionTypeModel)
                                    .filter(ConnectionTypeModel.code == conn_type['code'])
                                    .one())
        payload.pop('is_bot')  # FIXME: skip now, but need to implement how to update is_bot field
        conn.date_updated = datetime.now()

        # other fields:
        for key, value in payload.items():
            setattr(conn, key, value)

        return ConnectionBase(**conn.dict(), connection_=conn)

    def delete(self, id_, org_id, user_id,):
        conn = self._get(id_, org_id, user_id)
        self.session.delete(conn)
        return None