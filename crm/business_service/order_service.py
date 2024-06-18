import json

from crm.repository.models import TerminalModel
from crm.repository.order_repository import OrderRepository


class OrderService:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def list_orders(self, user_id, limit=None, **filters):
        return self.order_repository.list(user_id, limit, **filters)

    def get_order(self, id, user_id):
        return self.order_repository.get(id, user_id)

    def create_order(self, **payload):
        return self.order_repository.add(**payload)

    def create_payment(self, order_id, user_id, **payload):
        # TODO for all methods change param id to entity_id to avoid confusion + pass org_id
        # update only terminal if it is changed:
        new_payload = {}
        link_pay = None
        if 'terminal' in payload and payload['terminal']['id']:
            terminal = payload.pop('terminal')
            # create payment link:
            if terminal['connection_json']:
                link_pay = terminal['connection_url'].rstrip('?') + '?'
                params = json.loads(terminal['connection_json'])
                for item in params:
                    if item[0] == 'amount':
                        item[1] = payload['amount']
                    if link_pay[-1] != '?':
                        link_pay += f'&{item[0]}={item[1]}'
                    else:
                        link_pay += f'{item[0]}={item[1]}'
            new_payload['link_pay'] = link_pay
            new_payload['terminal_id'] = terminal['id']

            return self.order_repository.update(order_id, user_id, **new_payload)
        else:
            raise ValueError('Terminal not found')
