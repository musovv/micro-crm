import json
from datetime import datetime

from crm.business_service.bases import CustomerBase
from crm.repository.customer_repository import CustomerRepository
from crm.repository.dialog_repository import DialogRepository
import httpx

from crm.repository.models import MessageModel


class DialogService:
    def __init__(self, dialog_repository: DialogRepository):
        self.dialog_repository = dialog_repository

    def get_dialog(self, dialog_id, user_id):
        return self.dialog_repository.get(dialog_id, user_id)

    def get_dialogs(self, user_id, limit=None, **filters):
        return self.dialog_repository.list(user_id, limit, **filters)

    async def create_dialog(self, user_id, **payload: dict):
        # find client/ client_id:
        country_code = payload.pop('country_code', None)
        if not country_code:
            raise ValueError('Country code of phone number is missed')

        phone_number = payload.pop('phone_number')
        if not phone_number:
            raise ValueError('Phone number is missed')

        # check exist in crm
        phone = str(country_code) + str(phone_number)  # temporary logic FIXME: add filter by country code
        phone = phone.replace('+', '')
        dialogs = self.dialog_repository.list(phone=phone, user_id=user_id)
        if dialogs:
            raise ValueError(f'Dialog with phone number: {phone} already exists in crm')

        # TDLIB:
        async with httpx.AsyncClient() as httpx_client:
            import tests.jwt_generator as t
            jwt_token = t.generate_jwt()
            headers = {"Authorization": 'Bearer ' + jwt_token}
            # Temporary service:
            response = await httpx_client.post('http://localhost:3000/webhook/create_contact',
                                               headers=headers,
                                               json={'contact_phone_number': phone})
        if response.status_code != 200:
            raise ValueError(f'Failed to create contact in TDLIB: {response.text}')

        response = json.loads(response.json())
        tg_user_id = response.get('user_id')
        tg_login = response.get('login', None)
        first_name = response.get('first_name')
        last_name = response.get('last_name')
        phone = response.get('phone')

        # add customer data to crm:
        customer = CustomerBase(
            fullname= ((first_name or '') + ' ' + (last_name or '')).strip(),
            mobile_number1=phone,
            owner_id=user_id,
            tg_user_id=tg_user_id,
            tg_login=tg_login
        )

        # create dialog and link to customer(client)
        # payload['client_id'] = customer.id It will never happened
        payload['customer'] = customer.dict()
        payload['last_activity'] = datetime.utcnow()
        payload['no_reply'] = False
        payload['amount_unread_msgs'] = 0

        return self.dialog_repository.add(**payload)

    def reply_to_dialog(self, dialog_id, user_id, message):
        dialog_base = self.dialog_repository.get(dialog_id, user_id)

        # add message into db
        msg = {
            "text": message,
            "date": datetime.utcnow(),
            "dialog_id": dialog_base.id,
        }
        message_model = MessageModel(**msg)
        self.dialog_repository.session.add(message_model)

        # update dialog:
        dialog = self.dialog_repository.get(dialog_id, user_id)
        payload = {
            "amount_unread_msgs": dialog.amount_unread_msgs + 1,
            "last_activity": datetime.utcnow()
        }
        self.dialog_repository.update(dialog.id, user_id=user_id,  **payload)

        # send message to TDLIB
        # TODO send message to TDLIB

    def set_no_reply(self, dialog_id, user_id, no_reply):
        dialog = self.dialog_repository.get(dialog_id, user_id)
        payload = {
            "no_reply": no_reply
        }
        self.dialog_repository.update(dialog.id, user_id=user_id, **payload)

    def delete_dialog(self, dialog_id, user_id):
        return self.dialog_repository.delete(dialog_id, user_id)