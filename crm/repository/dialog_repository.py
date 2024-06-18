
from abc import ABC
from datetime import datetime

from crm.business_service.bases import DialogBase
from crm.openapi_server.models.dialog_message import DialogMessage
from crm.repository.models import DialogModel, CustomerModel
from crm.repository.repository import Repository


class DialogRepository(Repository, ABC):
    def __init__(self, session):
        self.session = session

    def list(self, user_id=None, limit=None, **filters):

        phone = filters.pop('phone', None)

        query = self.session.query(DialogModel).join(DialogModel.client)
        if phone:
            query = query.filter(CustomerModel.mobile_number1 == phone)

        if user_id:
            query = query.filter(CustomerModel.owner_id == user_id)

        if limit:
            dialogs = query.limit(limit).all()
        else:
            dialogs = query.all()
        return [DialogBase(**dialog.dict()) for dialog in dialogs]

    def _get(self, id, user_id):
        # TODO admin check for user_id
        dialog = (self.session.query(DialogModel).join(DialogModel.client)
                  .filter(DialogModel.id == id, CustomerModel.owner_id == user_id)
                  .first())
        if not dialog:
            raise ValueError('Dialog not found')
        return dialog

    def get(self, id, user_id) -> DialogBase:
        dialog = self._get(id, user_id)
        return DialogBase(**dialog.dict(), dialog_=dialog)

    def add(self, **payload: dict) -> DialogBase:
        customer = payload.pop('customer', None)
        if not customer:
            raise ValueError('Customer data is missed')

        # Add client to db
        customer = CustomerModel(**customer)
        customer.status = 1  # active
        customer.date_created = datetime.utcnow()
        self.session.add(customer)

        # Add dialog to db
        dialog = DialogModel(**payload)
        dialog.client = customer
        self.session.add(dialog)
        return DialogBase(**dialog.dict(), dialog_=dialog)

    def update(self, id, user_id, **payload) -> DialogBase:
        payload.pop('messages', None)

        dialog = self._get(id, user_id)
        for key, value in payload.items():
            setattr(dialog, key, value)
        return DialogBase(**dialog.dict(), dialog_=dialog)

    def delete(self, id, user_id):
        dialog = self._get(id, user_id)
        self.session.delete(dialog)
        return None