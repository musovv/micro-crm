from typing import List, Dict
from crm.business_service.bases import CatalogBase
from crm.openapi_server.models.catalog import Catalog
from crm.openapi_server.models.new_catalog import NewCatalog
from crm.repository.models import CatalogModel
from crm.repository.repository import Repository


class CatalogService:

    def __init__(self, catalog_repository: Repository):
        self.catalog_repository = catalog_repository

    def get_catalog(self, id_) -> Catalog:
        catalog = self.catalog_repository.get(id_)
        return catalog.dict(cls_map=NewCatalog)

    def create_catalog(self, **payload) -> NewCatalog:  #**payload: Dict
        catalog = CatalogBase(**payload)
        res = self.catalog_repository.add(**catalog.dict(CatalogModel))
        return res

    def list_catalogs(self, **filters: Dict) -> List[Dict]:
        limit = filters.pop('limit', None)
        catalogs = self.catalog_repository.list(limit, **filters)
        return [catalog.dict(cls_map=Catalog) for catalog in catalogs]

    def update_catalog(self, id_, **payload) -> Catalog:
        catalog = CatalogBase(**payload)
        res = self.catalog_repository.update(id_, **catalog.dict(CatalogModel))
        return res

    def delete_catalog(self, id_):
        self.catalog_repository.delete(id_)
        return None

