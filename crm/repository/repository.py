from abc import ABC, abstractmethod
from typing import List
from crm.business_service.base import EntityBase
from crm.business_service.bases import CatalogBase


class Repository(ABC):
    @abstractmethod
    def add(self, org_id, user_id, **payload: dict) -> EntityBase:
        pass

    @abstractmethod
    def get(self, id_, org_id, user_id) -> EntityBase:
        pass

    @abstractmethod
    def list(self, org_id, user_id, limit=None, **filters) -> List[EntityBase]:
        pass

    @abstractmethod
    def update(self, id_, org_id, user_id, **payload) -> EntityBase:
        pass

    @abstractmethod
    def delete(self, id_, org_id, user_id) -> None:
        pass