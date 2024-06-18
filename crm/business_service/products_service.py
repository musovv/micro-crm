from typing import List, Dict

from crm.business_service.base import EntityBase
from crm.business_service.catalogs_service import CatalogBase
from crm.business_service.exceptions import ProductNotFoundError
from crm.business_service.bases import ProductBase, ImageBase
from crm.openapi_server.models.product import Product
from crm.repository.models import ProductModel, ProductTypeModel
# from crm.repository.products_repository import ProductsRepository # !! lead to circular dependency
from crm.repository.repository import Repository


# Business logic layer
class ProductsService:
    def __init__(self, products_repository: Repository):  # !! I enhanced this class with Interface Repository
        self.products_repository = products_repository

    def list_products(self, **filters: Dict) -> List[Product]:
        limit = filters.pop('limit', None)
        products = self.products_repository.list(limit, **filters)
        return [product.dict(cls_map=Product) for product in products]

    def get_product(self, product_id: str) -> ProductBase | EntityBase:
        product = self.products_repository.get(product_id)
        if product is None:
            raise ProductNotFoundError(f'Product {product_id} not found')

        return product


    def create_product(self, **payload: Dict) -> ProductBase | EntityBase:
        product = ProductBase(**payload)
        product = self.products_repository.add(product.dict(cls_map=ProductModel))
        return product

    def update_product(self, product_id, **payload) -> ProductBase | EntityBase:  # TODO think about pass data as payload with id in one dictionary
        product = self.products_repository.get(product_id)
        if product is None:
            raise ProductNotFoundError(f'Product {product_id} not found')

        product = ProductBase(**payload)
        # check that one image is main and not more than one
        main_images = [image for image in product.images if image.main]
        if len(main_images) > 1:
            raise ValueError('Only one image can be main')
        return self.products_repository.update(product_id, **product.dict(cls_map=ProductModel))

    def delete_product(self, product_id) -> None:
        self.products_repository.delete(product_id)



# !! ProductBase is similar to Product from web adapters models.py, Product class is used for validation and serialization in web layer
# !! ProductBase use only in business logic layer and repository layer for return data. In DDD it is Domain Model/Object
# !! ProductModel is used for database operations in sessions and queries

