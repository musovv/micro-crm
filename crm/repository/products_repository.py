from typing import List
from crm.utils import Utils as u


from crm.repository.repository import Repository
from crm.repository.models import ProductModel, ImageModel, ProductTypeModel, CatalogModel
from crm.business_service.products_service import ProductBase

class ProductsRepository(Repository):
    def __init__(self, session):
        self.session = session

    def add(self, product: dict) -> ProductBase:
        catalogs = product.pop('catalogs', [])
        images = product.pop('images', [])
        product = ProductModel(**product)
        product.product_type = (self.session.query(ProductTypeModel)
                                .filter(ProductTypeModel.code == product.product_type.code)
                                .first())

        for image in images:
            product.images.append(ImageModel(**image))

        for catalog in catalogs:
            catalog = self.session.query(CatalogModel).where(CatalogModel.id == catalog['id']).first()
            product.catalogs.append(catalog)

        self.session.add(product)
        return ProductBase(**product.dict(), product_=product)

    def _get(self, id_, **filters) -> ProductModel:
        return (
            self.session.query(ProductModel)
            .filter(ProductModel.id == str(id_)).filter_by(**filters)  # TODO Does filter_by redundant here?
            .first()
        )

    def get(self, id_, **filters) -> ProductBase:
        product = self._get(id_, **filters)
        if product is not None:
            # fill product_type
            product.product_type = (self.session.query(ProductTypeModel)
                                    .filter(ProductTypeModel.id == product.product_typeid)
                                    .first())
        return ProductBase(**product.dict())

    def list(self, limit=None, **filters) -> List[ProductBase]:
        products = self.session.query(ProductModel).limit(limit).all()
        for product in products:
            product.product_type = (self.session.query(ProductTypeModel)
                                    .filter(ProductTypeModel.id == product.product_typeid)
                                    .first())

        return [ProductBase(**product.dict()) for product in products]

    def update(self, id_, **payload) -> ProductBase:  # TODO full update or partial update?
        product = self._get(id_)
        # set product_type
        product_type = payload.pop('product_type', None)
        if product_type is None:
            raise ValueError('Product type not found')
        product.product_type = (self.session.query(ProductTypeModel)
                                .filter(ProductTypeModel.code == product_type['code'])
                                .first())

        # update catalogs through catalog ids
        # 1 delete all links catalogs:
        product.catalogs.clear()
        # 2 add new links catalogs:
        catalogs = payload.pop('catalogs', [])
        for catalog in catalogs:
            catalog = self.session.query(CatalogModel).where(CatalogModel.id == catalog['id']).first()
            product.catalogs.append(catalog)

        # update images
        images = payload.pop('images', [])
        for image in images:
            im = next((im for im in product.images if im.id == image['id']), None)
            if im:
                # update fields in image
                for key, value in image.items():
                    setattr(im, key, value)
            else:
                product.images.append(ImageModel(**image))

        # update fields in product
        for key, value in payload.items():
            setattr(product, key, value)

        return ProductBase(**product.dict())

    def delete(self, id_):
        product = self._get(id_)
        if product is None:
            raise ValueError(f'Product {id_} not found')
        self.session.delete(product)
        return None
