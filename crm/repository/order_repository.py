import datetime
from abc import ABC

from crm.business_service.bases import OrderBase
from crm.openapi_server.models.order import StatusEnum
from crm.repository.models import OrderModel, OrderItemModel, TerminalModel, NoteModel, CustomerModel
from crm.repository.products_repository import ProductsRepository
from crm.repository.repository import Repository


class OrderRepository(Repository, ABC):
    def __init__(self, session):
        self.session = session

    def list(self, user_id, limit=None, **filters):
        orders = []
        client_id = filters.pop('client_id', None)
        if client_id is None:
            raise ValueError('Client id is required')
        query = self.session.query(OrderModel)
        query = query.join(OrderModel.items).filter(CustomerModel.owner_id == user_id,  # TODO check permissions
                                                    OrderModel.client_id == client_id)

        if limit:
            orders = query.limit(limit).all()
        else:
            orders = query.all()
        return [OrderBase(**order.dict()) for order in orders]

    def _get(self, id, user_id):
        # TODO think about check permissions for user to access order and for others entities
        order = (self.session.query(OrderModel)
                 .join(OrderModel.items)
                 .filter(OrderModel.id == id, CustomerModel.owner_id == user_id)
                 .first())
        if not order:
            raise ValueError('Order not found')
        return order

    def get(self, id, user_id):
        order = self._get(id, user_id)
        return OrderBase(**order.dict(), order_=order)

    def add(self, **payload: dict) -> OrderBase:

        # generate new number for order
        from crm.utils import Utils as u
        number = u.generate_short_guid()

        order = OrderModel()  # or OrderModel(**payload) but then required using additional transform for dict into business layer
        order.number = number
        order.date = datetime.datetime.utcnow()
        order.status = StatusEnum.CREATED.to_int()

        items = payload.get('items', [])
        order.amount = self._calculate_amount(items)

        order.client_id = payload['client_id']
        for item in payload.get('items', []):
            item = OrderItemModel(**item)
            order.items.append(item)
        terminal = payload.get('terminal')
        if terminal:
            order.terminal = TerminalModel(**payload.get('terminal'))
        order.link_pay = payload.get('link_pay', None)
        order.comment = payload.get('comment', None)
        for note in payload.get('notes', []):
            order.notes.append(NoteModel(**note))

        self.session.add(order)
        return OrderBase(**order.dict(), order_=order)

    def _calculate_amount(self, items: list) -> float:
        amount = 0
        currency = set()
        for item in items:
            if type(item) is dict:
                product = ProductsRepository(self.session).get(item['product_id'])
                quantity = item['quantity']
            else:
                product = item.product
                quantity = item.quantity
            if not product:
                raise ValueError('Product not found')
            currency.add(product.currency)
            amount += product.price * quantity
        if len(currency) > 1:
            raise ValueError('Currency mismatch')  # FIXME move on logic to business layer
        return amount

    def update(self, order_id, user_id, **payload) -> OrderBase:
        items = payload.pop('items', [])
        notes = payload.pop('notes', [])
        # terminal = payload.pop('terminal', None)

        order = self._get(order_id, user_id)
        existing_items = [item.id for item in order.items]  # FIXME create utility method for this that will be used in all repositories
        existing_notes = [note.id for note in order.notes]
        existing_terminal = order.terminal
        for key, value in payload.items():
            setattr(order, key, value)

        # if not (existing_terminal and existing_terminal.id == terminal['id']):
        #     order.terminal = TerminalModel(**terminal)

        for item in items:
            if item.get('id') in existing_items:
                continue
            item = OrderItemModel(**item)
            order.items.append(item)
        order.amount = self._calculate_amount(order.items)

        order.notes = []

        for note in notes:
            if note.get('id') in existing_notes:
                continue
            note = NoteModel(**note)
            order.notes.append(note)

        return OrderBase(**order.dict(), order_=order)

    def delete(self, id, user_id):
        order = self._get(id, user_id)
        self.session.delete(order)
