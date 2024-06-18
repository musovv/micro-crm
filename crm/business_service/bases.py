from crm.business_service.base import EntityBase
from uuid import UUID
from typing import List, Dict

from crm.decorators import remove_none
from crm.openapi_server.models.catalog import Catalog
from crm.openapi_server.models.connection import Connection
from crm.openapi_server.models.dialog import Dialog
from crm.openapi_server.models.dialog_message import DialogMessage
from crm.openapi_server.models.employee import Employee
from crm.openapi_server.models.employee_role import EmployeeRole
from crm.openapi_server.models.new_catalog import NewCatalog
from crm.openapi_server.models.new_connection import NewConnection
from crm.openapi_server.models.new_dialog import NewDialog
from crm.openapi_server.models.new_employee import NewEmployee
from crm.openapi_server.models.new_product import NewProduct
from crm.openapi_server.models.order import StatusEnum
from crm.openapi_server.models.product import Product
from crm.repository.models import CatalogModel, ProductModel, ConnectionModel, EmployeeModel, DialogModel
from crm.utils import Utils as u


class ImageBase:
    def __init__(self, id=None, filename=None, body=None, format=None, date=None, main=None, image_=None):
        self._id = id
        self._image = image_
        self.filename = filename
        self.body = body
        self.format = format
        self.date = date
        self.main = main

    @property
    def id(self):
        return self._id or self._image.id

    def dict(self):
        return {
            'id': str(self._id) if self._id is not None else None,
            'filename': self.filename,
            'body': self.body,
            'format': self.format,
            'date': self.date,
            'main': self.main,
        }


class CatalogBase(EntityBase):
    def __init__(self, name: str, id: UUID = None, product_ids: List[str] = None, products: List[Dict] = None,
                catalog_=None):
        self._id = id
        self._catalog = catalog_
        self.name = name
        self.product_ids = product_ids  # Catalog
        self.products = [ProductBase(**product) for product in products] if products else []  # NewCatalog

    @property
    def id(self):
        if self._id is None and self._catalog is None:
            return None
        return self._id or self._catalog.id

    # @remove_none - it makes confusion, not clear when you inspect the code,
    # better to use explicit mapping of fields depending on class
    def dict(self, cls_map=None):
        payload = {
            'id': str(self.id) if self.id is not None else None,
            'name': self.name,
        }
        if cls_map is Catalog:
            if self.products:
                payload['product_ids'] = []
                for product in self.products:
                    payload['product_ids'].append(product.id)
            else:
                payload['product_ids'] = self.product_ids
        elif cls_map is NewCatalog:
            payload['products'] = [product.dict(Product) for product in self.products]
        elif cls_map is CatalogModel:
            if self.product_ids and not self.products:
                payload['products'] = [dict(id=_id) for _id in self.product_ids]
            else:
                payload['products'] = [product.dict(ProductModel) for product in self.products]

        return payload


class ProductTypeBase(EntityBase):
    def __init__(self, name, code, id=None):
        self._id = id
        self.name = name
        self.code = code

    @property
    def id(self):
        return self._id

    def dict(self):
        return {
            'id': str(self.id) if self.id is not None else None,
            'name': self.name,
            'code': self.code,
        }


class ProductBase(EntityBase):
    def __init__(self, name, product_type, price, currency, id=None, product_=None, **kwargs):
        self._id = id
        self._product = product_
        self.name = name
        self.product_type = ProductTypeBase(**product_type)
        self.description = kwargs.pop('description', None)
        self.price = price
        self.currency = currency
        self.vat = kwargs.pop('vat', None)
        self.code_product = kwargs.pop('code_product', None)
        if self._product:
            self.images = self._product.images
        else:
            self.images = [ImageBase(**image) for image in kwargs.pop('images', [])]
        self.catalogs = [CatalogBase(**catalog) for catalog in kwargs.pop('catalogs', [])]

    @property
    def id(self):
        if self._id is None and self._product is None:
            return None
        return self._id or self._product.id

    @property
    def image(self):
        if self.images:
            for image in self.images:
                if image.main is True:
                    return image
        return None

    def dict(self, cls_map=None):
        payload = {
            'id': str(self.id) if self.id is not None else None,
            'name': self.name,
            'description': self.description,
            'product_type': self.product_type.dict(),
            'price': self.price,
            'currency': self.currency,
            'vat': self.vat,
            'code_product': self.code_product
        }

        if cls_map is Product:
            payload['image'] = self.image.dict() if self.image else None
        elif cls_map is NewProduct:
            payload['images'] = [image.dict() for image in self.images]
            payload['catalogs'] = [catalog.dict(Catalog) for catalog in self.catalogs]
        elif cls_map is ProductModel:
            payload['images'] = [image.dict() for image in self.images]
            payload['catalogs'] = [catalog.dict(CatalogModel) for catalog in self.catalogs]

        return payload


class ConnectionTypeBase:
    def __init__(self, name, code, id=None):
        self.id = None
        self.name = name
        self.code = code

    def dict(self):
        return {
            'name': self.name,
            'code': self.code
        }

class ConnectionBase:
    def __init__(self, id, organization_id, connection_type, name, phone_number, connection_=None, **kwargs):
        self._connection_id = id
        self._connection = connection_
        self.organization_id = organization_id
        self.connection_type = ConnectionTypeBase(**connection_type)
        self.name = name
        self.phone_number = phone_number
        self.is_bot = kwargs.pop('is_bot', None)
        self.token = kwargs.pop('token', None)

    @property
    def id(self):
        if self._connection_id is None and self._connection is None:
            return None
        return self._connection_id or self._connection.id

    def dict(self, cls_map=None):
        payload = {
            'id': str(self.id) if self.id is not None else None,
            'connection_type': self.connection_type.dict(),
            'name': self.name,
            'phone_number': self.phone_number,
        }

        if cls_map is NewConnection:
            payload['token'] = self.token
        elif cls_map is Connection:
            payload['is_bot'] = self.is_bot
        elif cls_map is ConnectionModel:
            payload['is_bot'] = self.is_bot
            payload['token'] = self.token
            payload['organization_id'] = self.organization_id

        return payload


class TypeResourceBase:
    def __init__(self, name, code, id=None):
        self._id = id
        self.name = name
        self.code = code

    @property
    def id(self):
        return self._id

    def dict(self):
        return {
            'id': str(self.id) if self.id is not None else None,
            'name': self.name,
            'code': self.code
        }


class PermissionBase:
    def __init__(self, name, description, type_resource, access, privilege, access_level, id=None, permission_=None):
        self._id = id
        self.name = name
        self.description = description
        self.type_resource = TypeResourceBase(**type_resource)
        self.access = access
        self.privilege = privilege
        self.access_level = access_level
        self.permission_ = permission_

    @property
    def id(self):
        if self._id is None and self.permission_ is None:
            return None
        return self._id or self.permission_.id

    def dict(self):
        return {
            'id': str(self.id) if self.id is not None else None,
            'name': self.name,
            'description': self.description,
            'type_resource': self.type_resource.dict(),
            'access': self.access,
            'privilege': self.privilege,
            'access_level': self.access_level,
        }


class RoleBase:
    def __init__(self, id, name, permissions, description=None, role_=None):
        self._id = id
        self.name = name
        self.description = description
        self._permissions = [PermissionBase(**permission) for permission in permissions]
        self.role_ = role_

    @property
    def id(self):
        if self._id is None and self.role_ is None:
            return None
        return self._id or self.role_.id

    @property
    def permissions(self):
        if self.role_ and self.role_.permissions:
            return [PermissionBase(**permission.dict(), permission_=permission) for permission in self.role_.permissions]
        return self._permissions

    def dict(self):
        return {
            'id': str(self.id) if self.id is not None else None,
            'name': self.name,
            'permissions': [permission.dict() for permission in self.permissions]
        }


class EmployeeBase(EntityBase):
    def __init__(self, login, first_name, last_name, id=None, organization_id=None, status=None, type_employee=None,
                 password=None, roles=None, employee_=None):
        self._id = id
        self.org_id = organization_id
        self.login = login
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.status = status
        self.type_employee = type_employee
        self.roles = [RoleBase(**r) for r in roles] if roles else []
        self.employee_ = employee_

    @property
    def id(self):
        if self._id is None and self.employee_ is None:
            return None
        return self._id or self.employee_.id

    def dict(self, cls_map=None):
        d = {
            'id': str(self.id) if self.id is not None else None,
            'login': self.login,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'type_employee': self.type_employee,
        }
        if cls_map is NewEmployee:
            d['password'] = self.password
        elif cls_map is Employee:
            d['status'] = self.status
        elif cls_map is EmployeeRole:
            d['roles'] = [role.dict() for role in self.roles]
        elif cls_map is EmployeeModel:
            d['password'] = self.password
            d['organization_id'] = self.org_id
        return d


class TemplateBase(EntityBase):
    def __init__(self, title, text, owner_id,  id=None, template_=None):
        self._id = id
        self._template = template_
        self.title = title
        self.text = text
        self.owner_id = owner_id

    @property
    def id(self):
        if self._id is None and self._template is None:
            return None
        return self._id or self._template.id

    def dict(self):
        return {
            'id': str(self.id) if self.id is not None else None,
            'title': self.title,
            'text': self.text,
            'owner_id': self.owner_id,
        }


class TagBase(EntityBase):
    def __init__(self, name, color, description, id=None, tag_=None):
        self._id = id
        self._tag = tag_
        self.name = name
        self.color = color
        self.description = description

    @property
    def id(self):
        if self._id is None and self._tag is None:
            return None
        return self._id or self._tag.id

    def dict(self):
        return {
            'id': str(self.id) if self.id is not None else None,
            'name': self.name,
            'color': self.color,
            'description': self.description,
        }


class NoteBase(EntityBase):
    def __init__(self, note, date, customer_id, id=None, note_=None):
        self._id = id
        self._note = note_
        self.note = note
        self.date = date
        self.customer_id = customer_id

    @property
    def id(self):
        if self._id is None and self._note is None:
            return None
        return self._id or self._note.id

    def dict(self):
        return {
            'id': str(self.id) if self.id is not None else None,
            'note': self.note,
            'date': self.date,
            'customer_id': self.customer_id,
        }


class CustomerBase(EntityBase):
    def __init__(self, fullname, mobile_number1, owner_id, id=None, customer_=None, **kwargs):
        self._id = id
        self._customer = customer_
        self.fullname = fullname
        self.mobile_number1 = mobile_number1
        self.owner_id = owner_id
        self.tg_login = kwargs.pop('tg_login', None)
        self.tg_user_id = kwargs.pop('tg_user_id', None)
        self.mobile_number2 = kwargs.pop('mobile_number2', None)
        self.phone_number = kwargs.pop('phone_number', None)
        self.email = kwargs.pop('email', None)
        self.status = kwargs.pop('status', None)
        self.photo = kwargs.pop('photo', None)
        if self.photo:
            self.photo = ImageBase(**self.photo)
        self.tags = [TagBase(**tag) for tag in kwargs.pop('tags', [])]
        self.notes = [NoteBase(**note) for note in kwargs.pop('notes', [])]
        self._customer = customer_

    @property
    def id(self):
        if self._id is None and self._customer is None:
            return None
        return self._id or self._customer.id

    def dict(self):

        d = {
            'id': str(self.id) if self.id is not None else None,
            'tg_login': self.tg_login,
            'tg_user_id': self.tg_user_id,
            'fullname': self.fullname,
            'mobile_number1': self.mobile_number1,
            'mobile_number2': self.mobile_number2,
            'phone_number': self.phone_number,
            'email': self.email,
            'status': self.status,
            'owner_id': self.owner_id,
            'tags': [tag.dict() for tag in self._customer.tags] if self._customer else [tag.dict() for tag in self.tags],
            'notes': [note.dict() for note in self._customer.notes] if self._customer else [note.dict() for note in self.notes],
        }
        if not self._customer and not self.photo:
            d['photo'] = None
        else:
            d['photo'] = self._customer.photo.dict() if self._customer else self.photo.dict()

        return d


class MessageBase(EntityBase):
    def __init__(self, dialog_id, text, date, id=None, message_=None):
        self._id = id
        self._message = message_
        self.dialog_id = dialog_id
        self.text = text
        self.date = date

    @property
    def id(self):
        if self._id is None and self._message is None:
            return None
        return self._id or self._message.id

    def dict(self):
        return {
            'id': str(self.id) if self.id is not None else None,
            'dialog_id': self.dialog_id,
            'text': self.text,
            'date': self.date,
        }


class DialogBase(EntityBase):
    def __init__(self, connection_id, id=None, dialog_=None, **kwargs):
        self._id = id
        self._dialog = dialog_
        self.connection_id = connection_id
        self.client = kwargs.pop('client', None)
        if self.client:
            self.client = CustomerBase(**self.client)

        self.messages = kwargs.pop('messages', [])
        self.messages = [MessageBase(**message) for message in self.messages]

        self.last_activity = kwargs.pop('last_activity', None)
        self.amount_unread_msgs = kwargs.pop('amount_unread_msgs', None)
        self.no_reply = kwargs.pop('no_reply', None)
        # for NewDialog:
        self.phone_number = kwargs.pop('phone_number', None)
        self.country_code = kwargs.pop('country_code', None)

    @property
    def id(self):
        if self._id is None and self._dialog is None:
            return None
        return self._id or self._dialog.id

    def dict(self, cls_map=None):
        d = {
            'id': str(self.id) if self.id is not None else None,
            'connection_id': self.connection_id,
            'client': self._dialog.client.dict() if self._dialog else self.client.dict(),
            'last_activity': self.last_activity,
            'amount_unread_msgs': self.amount_unread_msgs,
            'no_reply': self.no_reply,
        }
        if cls_map is DialogMessage:
            d['messages'] = [message.dict() for message in self.messages]
        # elif cls_map is DialogModel:
        #     d['messages'] = [message.dict() for message in self.messages]

        return d


class TerminalTypeBase(EntityBase):
    def __init__(self, name, code, configuration_json, id=None):
        self._id = id
        self.name = name
        self.code = code
        self.configuration_json = configuration_json

    @property
    def id(self):
        return self._id

    def dict(self):
        return {
            'name': self.name,
            'code': self.code,
            'configuration_json': self.configuration_json
        }


class TerminalBase(EntityBase):
    def __init__(self, name, terminal_type, id=None, terminal_=None, **payload):
        self._id = id
        self.terminal_ = terminal_
        self.name = name
        self.terminal_type = TerminalTypeBase(**terminal_type)
        self.connection_url = payload.pop('connection_url', None)
        self.connection_json = payload.pop('connection_json', None)

    @property
    def id(self):
        if self._id is None and self.terminal_ is None:
            return None
        return self._id or self.terminal_.id

    def dict(self):
        return {
            'id': str(self.id) if self.id is not None else None,
            'name': self.name,
            'terminal_type': self.terminal_type.dict(),
            'connection_url': self.connection_url,
            'connection_json': self.connection_json
        }


class OrderItemBase(EntityBase):
    def __init__(self, product_id, quantity, id=None, order_item_=None):
        self._id = id
        self._order_item = order_item_
        self.product_id = product_id
        self.quantity = quantity

    @property
    def id(self):
        if self._id is None and self._order_item is None:
            return None
        return self._id or self._order_item.id

    def dict(self):
        return {
            'id': str(self.id) if self.id is not None else None,
            'product_id': self.product_id,
            'quantity': self.quantity
        }


class OrderBase(EntityBase):
    def __init__(self, id, client_id, order_=None, **payload):
        self._id = id
        self.order_ = order_
        self.client_id = client_id
        self.number = payload.pop('number', None)
        self.date = payload.pop('date', None)
        self._status = payload.pop('status', None)
        self.amount = payload.pop('amount', None)
        self.link_pay = payload.pop('link_pay', None)
        self.terminal = payload.pop('terminal', None)
        if self.terminal:
            self.terminal = TerminalBase(**self.terminal)
        self.items = [OrderItemBase(**item) for item in payload.pop('items', [])]
        self.comment = payload.pop('comment', None)
        self.notes = [NoteBase(**note) for note in payload.pop('notes', [])]

    @property
    def id(self):
        if self._id is None and self.order_ is None:
            return None
        return self._id or self.order_.id

    @property
    def status(self):
        return StatusEnum.from_int(self._status).value

    def dict(self):
        t = None
        if self.order_ and self.order_.terminal:
            t = self.order_.terminal.dict()
        elif self.terminal:
            t = self.terminal.dict()

        return {
            'id': str(self.id) if self.id is not None else None,
            'client_id': self.client_id,
            'number': self.number,
            'date': self.date,
            'status': self.status,
            'amount': self.amount,
            'link_pay': self.link_pay,
            'terminal':  t,
            'items': [item.dict() for item in self.order_.items]
                if self.order_
                else [item.dict() for item in self.items],
            'comment': self.comment,
            'notes': [note.dict() for note in self.notes]
        }


class NotificationBase(EntityBase):
    def __init__(self, id, notification_=None, **payload):
        self._id = id
        self.notification_ = notification_
        self.setting_id = payload.pop('setting_id', None)
        self.phone_number = payload.pop('phone_number', None)
        self.notify_payments = payload.pop('notify_payments', None)
        self.notify_trouble_integrations = payload.pop('notify_trouble_integrations', None)
        self.notify_newsletters = payload.pop('notify_newsletters', None)

    @property
    def id(self):
        if self._id is None and self.notification_ is None:
            return None
        return self._id or self.notification_.id

    def dict(self):
        return {
            'id': str(self.id) if self.id is not None else None,
            'setting_id': self.setting_id,
            'phone_number': self.phone_number,
            'notify_payments': self.notify_payments,
            'notify_trouble_integrations': self.notify_trouble_integrations,
            'notify_newsletters': self.notify_newsletters
        }


class SettingBase(EntityBase):
    def __init__(self, id, setting_=None, **payload):
        self._id = id
        self.setting_ = setting_
        self.company_name = payload.pop('company_name', None)
        self.currency = payload.pop('currency', None)
        self.timezone = payload.pop('timezone', None)
        self.language = payload.pop('language', None)
        self.notification_ = payload.pop('notification', None)
        if self.notification_:
            self.notification_ = NotificationBase(**self.notification_)
        self.organization_id_ = payload.pop('organization_id', None)

    @property
    def id(self):
        if self._id is None and self.setting_ is None:
            return None
        return self._id or self.setting_.id

    @property
    def organization_id(self):
        if self.setting_ is None and self.organization_id_ is None:
            return None
        elif self.setting_:
            return self.setting_.organization_id
        else:
            return self.organization_id_

    @property
    def notification(self):
        if self.setting_ and self.setting_.notification:
            return NotificationBase(**self.setting_.notification.dict())
        return self.notification_

    def dict(self):
        return {
            'id': str(self.id) if self.id is not None else None,
            'company_name': self.company_name,
            'currency': self.currency,
            'timezone': self.timezone,
            'language': self.language,
            'notification': self.notification.dict() if self.notification else None,
            'organization_id': self.organization_id
        }


class SubscriptionBase(EntityBase):
    def __init__(self, connection, id=None, subscription_=None, **payload):
        self._id = id
        self.subscription_ = subscription_
        self.connection = ConnectionBase(**connection)
        self.status = payload.pop('status')
        self._until_valid = payload.pop('until_valid', None)
        self._date_end = payload.pop('date_end', None)
        # subscription_included or included_subscribe
        self._included_subscribe = payload.pop('included_subscribe', None)
        self._subscription_included = payload.pop('subscription_included', None)

    @property
    def id(self):
        if self._id is None and self.subscription_ is None:
            return None
        return self._id or self.subscription_.id

    @property
    def until_valid(self):
        return self._until_valid or self._date_end

    @property
    def included_subscribe(self):
        if self._subscription_included is not None:
            return self._subscription_included
        elif self._included_subscribe is not None:
            return self._included_subscribe

    def dict(self):
        return {
            'id': str(self.id) if self.id is not None else None,
            'connection': self.connection.dict(cls_map=Connection) if self.connection else None,
            'status': self.status,
            'until_valid': self.until_valid,
            'included_subscribe': self.included_subscribe
        }


class PricingBase(EntityBase):
    def __init__(self, connection_type, id=None, pricing_=None, **payload):
        self._id = id
        self.pricing_ = pricing_
        self.connection_type = ConnectionTypeBase(**connection_type)
        self.price = payload.pop('price')
        self.currency = payload.pop('currency')
        self.discount = payload.pop('discount')
        self.discount_type = payload.pop('discount_type')

    @property
    def id(self):
        if self._id is None and self.pricing_ is None:
            return None
        return self._id or self.pricing_.id

    def dict(self):
        return {
            'id': str(self.id) if self.id is not None else None,
            'connection_type': self.connection_type.dict(),
            'price': self.price,
            'currency': self.currency,
            'discount': self.discount,
            'discount_type': self.discount_type
        }


class HistoryBase(EntityBase):
    def __init__(self, id=None, **payload):
        self._id = id
        self.subscription_id = payload.pop('subscription_id')
        self.invoice_id = payload.pop('invoice_id')
        self.price = payload.pop('price')
        self.discount = payload.pop('discount')
        self.currency = payload.pop('currency')
        self.date_start = payload.pop('date_start')
        self.date_end = payload.pop('date_end')

    @property
    def id(self):
        return self._id
    def dict(self):
        return {
            'subscription_id': self.subscription_id,
            'invoice_id': self.invoice_id,
            'price': self.price,
            'discount': self.discount,
            'currency': self.currency,
            'date_start': self.date_start,
            'date_end': self.date_end
        }


class InvoiceBase(EntityBase):
    def __init__(self, id, invoice_=None, **payload):
        self._id = id
        self.invoice_ = invoice_

        self.invoice_number = payload.pop('invoice_number', None)
        self.invoice_date = payload.pop('invoice_date', None)
        self.total_amount = payload.pop('total_amount', None)
        self.currency = payload.pop('currency', None)
        self.discount = payload.pop('discount', None)
        self.start_date_subscription = payload.pop('start_date_subscription', None)
        self.end_date_subscription = payload.pop('end_date_subscription', None)

        self.buyer_name = payload.pop('buyer_name', None)
        self.organization_id = payload.pop('organization_id', None)
        self.link_invoice = payload.pop('link_invoice', None)
        self.subscriptions = [HistoryBase(**history) for history in payload.pop('subscriptions', [])]


    @property
    def id(self):
        if self._id is None and self.invoice_ is None:
            return None
        return self._id or self.invoice_.id

    def dict(self):
        return {
            'id': str(self.id) if self.id is not None else None,
            'invoice_number': self.invoice_number,
            'invoice_date': self.invoice_date,
            'total_amount': self.total_amount,
            'currency': self.currency,
            'discount': self.discount,
            'start_date_subscription': self.start_date_subscription,
            'end_date_subscription': self.end_date_subscription,
            'buyer_name': self.buyer_name,
            'link_invoice': self.link_invoice,
            'subscriptions': [history.dict() for history in self.subscriptions]
        }