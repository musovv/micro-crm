from crm.business_service.bases import InvoiceBase
from crm.openapi_server.models.pay_subscription import PaySubscriptions
from crm.openapi_server.models.subscription import Subscription
from crm.repository.invoice_repository import InvoiceRepository
from crm.repository.models import PricingModel, ConnectionModel, ConnectionTypeModel
from crm.repository.price_repository import PriceRepository
from crm.repository.subscription_repository import SubscriptionRepository


class SubscriptionService:
    def __init__(self, subscription_repository: SubscriptionRepository):
        self.subscription_repository = subscription_repository

    def create_subscription(self, org_id, user_id, **payload):
        return self.subscription_repository.add(org_id, user_id, **payload)

    def get_subscription(self, subscription_id):
        return self.subscription_repository.get(subscription_id)

    def list_subscriptions(self, org_id, user_id, limit=None, **filters):
        return self.subscription_repository.list(org_id, user_id, limit, **filters)

    def update_subscriptions(self, org_id, user_id, subscriptions):
        results = []
        for subscription in subscriptions:
            payload = {'subscription_included': subscription.included_subscribe}
            sub = self.subscription_repository.update(subscription.id, org_id, user_id, **payload)
            sub = sub.dict()
            Subscription.validate(sub)
            results.append(sub)

        return results

    def delete_subscription(self, subscription_id):
        return self.subscription_repository.delete(subscription_id)

    def pay_subscription(self, org_id, user_id, **payload) -> InvoiceBase:
        check_total_amount = payload.pop('total_amount', 0)
        subscriptions = payload.pop('subscriptions', [])
        total_amount = 0

        set_date_start = set()
        set_date_end = set()
        set_discount = set()
        for subscription in subscriptions:
            subscription_id = str(subscription['subscription_id'])
            set_date_start.add(subscription['date_start'])
            set_date_end.add(subscription['date_end'])
            set_discount.add(subscription['price']['discount'])
            # get subscription by id
            p = (self.subscription_repository.session
                .query(PricingModel).join(PricingModel.connection_type)
                .filter(PricingModel.id == str(subscription['price']['id']),
                        ConnectionTypeModel.code == str(subscription['price']['connection_type']['code']))
                .first())
            if p is None:
                raise ValueError(f'Price with id {subscription.price.id} not found')

            # update actual until date in subscription:
            sub_entity = self.subscription_repository.get(subscription_id, org_id, user_id)
            sub_entity.actual_until = subscription['date_end']

            total_amount += p.price

        if total_amount != check_total_amount:
            raise ValueError('Total amount is not correct')

        if len(set_date_start) != 1 or len(set_date_end) != 1:
            raise ValueError('Date start or date end is not correct')

        if len(set_discount) != 1:
            raise ValueError('Discount is not correct')


        invoice_payload = {"subscriptions": subscriptions, "total_amount": total_amount, "currency": subscriptions[0]['price']['currency'],
                           "discount": set_discount.pop(), "start_date_subscription": set_date_start.pop(),
                            "end_date_subscription": set_date_end.pop()}
        invoice = InvoiceRepository(self.subscription_repository.session).add(org_id, user_id, **invoice_payload)

        return invoice