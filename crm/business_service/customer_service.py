from crm.business_service.base import EntityBase
from crm.business_service.bases import CustomerBase
from crm.repository.customer_repository import CustomerRepository
from crm.repository.repository import Repository


class CustomerService:
    def __init__(self, customer_repository):
        self.customer_repository: CustomerRepository = customer_repository

    def get_customer(self, customer_id, user_id) -> EntityBase:

        return self.customer_repository.get(customer_id, user_id)

    def get_all_customers(self, user_id,  **filters):
        return self.customer_repository.list(user_id, **filters)

    def create_customer(self, user_id=None, **payload):
        payload['owner_id'] = user_id
        customer = CustomerBase(**payload)
        customer = self.customer_repository.add(**customer.dict())
        return customer

    def update_customer(self, customer_id, user_id, **payload):
        return self.customer_repository.update(customer_id, user_id, **payload)

    def delete_customer(self, customer_id):
        self.customer_repository.delete(customer_id)
        return None
