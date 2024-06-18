from crm.repository.price_repository import PriceRepository


class PriceService:
    def __init__(self, price_repository: PriceRepository):
        self.price_repository = price_repository

    def list_prices(self, org_id, user_id, limit, **filters):
        return self.price_repository.list(org_id, user_id, limit, **filters)