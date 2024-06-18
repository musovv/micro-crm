from typing import List, Dict

from crm.business_service.base import EntityBase
from crm.business_service.bases import CatalogBase, ConnectionBase
from crm.openapi_server.models.connection import Connection
from crm.openapi_server.models.new_connection import NewConnection
from crm.repository.connection_repository import ConnectionRepository
from crm.repository.models import CatalogModel, ConnectionModel
from crm.repository.repository import Repository


class ConnectionService:
    def __init__(self, connection_repository: ConnectionRepository):
        self.connection_repository = connection_repository

    def get_connection(self, id_, org_id, user_id) -> EntityBase | ConnectionBase:  # NewConnection
        base = self.connection_repository.get(id_, org_id, user_id)
        return base

    def create_connection(self, org_id, user_id, **payload) -> EntityBase | ConnectionBase:  # NewConnection
        conn = ConnectionBase(organization_id=org_id, **payload)
        # FIXME: add logic to check success of sign in
        conn = self.connection_repository.add(org_id, user_id, **conn.dict(cls_map=ConnectionModel))
        return conn

    def list_connections(self, org_id, user_id, **filters: Dict) -> List[EntityBase]:  # Connection
        bases = self.connection_repository.list(org_id, user_id, **filters)
        return bases

    def update_connection(self, id_, org_id, user_id,  **payload) -> EntityBase:  # NewConnection
        base = ConnectionBase(organization_id=org_id, **payload)
        conn = self.connection_repository.update(id_, org_id, user_id, **base.dict(cls_map=ConnectionModel))
        return conn

    def delete_connection(self, id_, org_id, user_id):
        self.connection_repository.delete(id_, org_id, user_id)
