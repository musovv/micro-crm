from abc import ABC

from crm.business_service.catalogs_service import CatalogBase
from crm.openapi_server.models.new_catalog import NewCatalog
from crm.repository.models import CatalogModel, ProductModel, ProductTypeModel, ImageModel
from crm.repository.repository import Repository


class CatalogRepository(Repository, ABC):
    def __init__(self, session):
        self.session = session

    def add(self, **payload: dict) -> CatalogBase:
        if 'products' in payload:
            product_records = payload.pop('products')
        else:
            raise ValueError('Products are not provided')
        catalog = CatalogModel(**payload)

        # init products list
        # products just link them to catalog !
        product_records = (self.session.query(ProductModel).filter(ProductModel.id.in_([str(p['id']) for p in product_records]))
                           .all())
        # fill product_records with ProductTypeModel
        for product in product_records:
            product.product_type = (self.session.query(ProductTypeModel)
                                    .where(ProductTypeModel.id == product.product_typeid).first())

        catalog.products.extend(product_records)
        self.session.add(catalog)
        return CatalogBase(**catalog.dict('catalogs'), catalog_= catalog)

    def get(self, id_) -> CatalogBase:
        catalog = self._get(id_)
        for product in catalog.products:
            product.product_type = (self.session.query(ProductTypeModel)
                                    .where(ProductTypeModel.id == product.product_typeid).first())
        return CatalogBase(**catalog.dict('catalogs'))

    def _get(self, id_) -> CatalogModel:
        if not id_:
            raise ValueError('Catalog id is not provided')
        catalog = self.session.query(CatalogModel).filter(CatalogModel.id == str(id_)).first()
        if not catalog:
            raise ValueError('Catalog not found')
        return catalog

    def list(self, limit=None, **filters) -> list[CatalogBase]:
        query = self.session.query(CatalogModel)
        if limit:
            query = query.limit(limit)
        catalogs = query.all()
        for catalog in catalogs:
            for product in catalog.products:
                product.product_type = (self.session.query(ProductTypeModel)
                                        .where(ProductTypeModel.id == product.product_typeid).first())

        return [CatalogBase(**catalog.dict('catalogs')) for catalog in query.all()]

    def update(self, id_, **payload) -> CatalogBase:
        catalog = self._get(id_)

        if 'products' in payload:
            # for product in catalog.products:
            #     self.session.delete(product)
            product_records = payload.pop('products', [])
            product_records = [self.session.query(ProductModel).filter(ProductModel.id == product['id']).first()
                               for product in product_records]

            # fill lookup product_type and images
            for product in product_records:
                product.product_type = (self.session.query(ProductTypeModel)
                                        .filter(ProductTypeModel.id == product.product_typeid).first())
                if not product.product_type:
                    raise ValueError('Product type not found')

            catalog.products = product_records

        for key, value in payload.items():
            setattr(catalog, key, value)

        return CatalogBase(**catalog.dict('catalogs'))

    def delete(self, id_) -> None:
        catalog = self._get(id_)
        self.session.delete(catalog)
        return None
