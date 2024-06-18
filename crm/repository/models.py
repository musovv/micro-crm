import uuid
from typing import List, Set

from sqlalchemy import Table, Column, String, Integer, BigInteger, Float, ForeignKey, DateTime, Boolean, inspect, BLOB, \
    CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, mapped_column, Mapped

from crm.decorators import break_circular, break_circular2

Base = declarative_base()


def generate_uuid():  # TODO add additional checks for id in database before saving, ensure that id at least 36 symbols and look like uuid
    return str(uuid.uuid4())


### N:N relationships ###
product_catalog = Table('product_catalog',
    Base.metadata,
    Column('product_id', String(36), ForeignKey('product.id')),
    Column('catalog_id', String(36), ForeignKey('catalog.id'))
)
image_product = Table('image_product',
    Base.metadata,
Column('image_id', String(36), ForeignKey('image.id')),
    Column('product_id', String(36), ForeignKey('product.id'))
)
employee_role = Table('employee_role',
    Base.metadata,
    Column('employee_id', String(36), ForeignKey('employee.id')),
    Column('role_id', String(36), ForeignKey('role.id'))
)
tag_customer = Table('tag_customer',
    Base.metadata,
    Column('tag_id', String(36), ForeignKey('tag.id')),
    Column('customer_id', String(36), ForeignKey('customer.id'))
)
# history = Table('history',
#     Base.metadata,
#     Column('subscription_id', String(36), ForeignKey('subscription.id')),
#     Column('invoice_id', String(36), ForeignKey('invoice.id')),
#     Column('price', Float, nullable=False),
#     Column('discount', Integer, nullable=False),
#     Column('currency', String(3), nullable=False),
#     Column('date_start', DateTime, nullable=False),
#     Column('date_end', DateTime, nullable=False)
# )



### IMAGE ###
class ImageModel(Base):
    __tablename__ = 'image'
    id = Column(String(36), primary_key=True, default=generate_uuid)
    filename = Column(String(256), nullable=True)
    body = Column(String(4000000), nullable=True)
    format = Column(String(24), nullable=True)
    date = Column(DateTime, nullable=True)
    main = Column(Boolean, nullable=True)
    products: Mapped[List['ProductModel']] = relationship(secondary=image_product, back_populates='images')

    def dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'body': self.body,
            'format': self.format,
            'date': self.date,
            'main': self.main
        }



### CATALOG ###
class CatalogModel(Base):
    __tablename__ = 'catalog'
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(32), nullable=False)
    products: Mapped[List['ProductModel']] = relationship(secondary=product_catalog, back_populates='catalogs')

    @break_circular2
    def dict(self, counter=None):
        return {
            'id': self.id,
            'name': self.name,
            'products': [p.dict(counter) for p in self.products if p.dict(counter) is not None]
            # 'products': [] if 'products' in breaker else [p.dict(*breaker) for p in self.products]
        }



### PRODUCT ###
class ProductTypeModel(Base):
    __tablename__ = 'product_type'
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(32), nullable=False)
    code = Column(Integer, nullable=False)

    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code
        }


class ProductModel(Base):
    __tablename__ = 'product'
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(64), nullable=False)
    description = Column(String(512), nullable=True)
    product_typeid = mapped_column(ForeignKey('product_type.id'), nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String(3), nullable=False)
    vat = Column(String(8), nullable=True)
    code_product = Column(String(16), nullable=True)
    images: Mapped[List["ImageModel"]] = relationship(secondary=image_product, back_populates='products')
    catalogs: Mapped[List["CatalogModel"]] = relationship(secondary=product_catalog, back_populates='products')


    ## LOOKUPs ##
    _product_type = None

    @property
    def product_type(self):
        if self._product_type:
            return self._product_type
        else:
            return ProductTypeModel(id= self.product_typeid)

    @product_type.setter
    def product_type(self, product_type):
        if isinstance(product_type, ProductTypeModel):
            self._product_type = product_type

        elif isinstance(product_type, dict):
            self._product_type = ProductTypeModel(**product_type)

        else:
            raise ValueError('product_type must be ProductTypeModel or dict')

        self.product_typeid = self._product_type.id

    @break_circular2
    def dict(self, counter=None):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'product_typeid': self.product_typeid,
            'product_type': self.product_type.dict(),
            'price': self.price,
            'currency': self.currency,
            'vat': self.vat,
            'code_product': self.code_product,
            'images': [im.dict() for im in self.images],
            'catalogs': [c.dict(counter) for c in self.catalogs if c.dict(counter) is not None]
        }


class OrganizationModel(Base):
    __tablename__ = 'organization'
    id = Column(String(36), primary_key=True, default=generate_uuid)
    date_created = Column(DateTime, nullable=False)
    setting: Mapped['SettingModel'] = relationship("SettingModel", uselist=False, back_populates="organization")
    employees: Mapped[List['EmployeeModel']] = relationship()


class SettingModel(Base):
    __tablename__ = 'setting'
    id = Column(String(36), primary_key=True, default=generate_uuid)
    organization_id = mapped_column(ForeignKey('organization.id', name='fk_organization_id'),  nullable=False)
    organization: Mapped['OrganizationModel'] = relationship()
    company_name = Column(String(64), nullable=False)
    currency = Column(String(3), nullable=False)
    timezone = Column(String(36), nullable=False)
    language = Column(String(2), nullable=False)
    notification:  Mapped['NotificationModel'] = relationship("NotificationModel", uselist=False, back_populates="setting")

    def dict(self):
        return {
            'id': self.id,
            'organization_id': self.organization_id,
            'company_name': self.company_name,
            'currency': self.currency,
            'timezone': self.timezone,
            'language': self.language,
            'notification': self.notification.dict() if self.notification else None
        }


class ConnectionTypeModel(Base):
    __tablename__ = 'connection_type'
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(32), nullable=False)
    code = Column(String, nullable=False)

    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code
        }


class ConnectionModel(Base):
    __tablename__ = 'connection'
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(32), nullable=False)
    connection_typeid = mapped_column(ForeignKey('connection_type.id'), nullable=False)
    connection_type: Mapped["ConnectionTypeModel"] = relationship()
    phone_number = Column(String(16), nullable=False)
    token = Column(String(256), nullable=True)
    is_bot = Column(Boolean, nullable=False)
    date_created = Column(DateTime, nullable=False)  # backends
    date_updated = Column(DateTime, nullable=False)  # backends
    # 1:1 relationship
    subscription_id = mapped_column(ForeignKey('subscription.id'), nullable=False)  # single_parent=True
    subscription: Mapped['SubscriptionModel'] = relationship()

    organization_id = mapped_column(ForeignKey('organization.id', name='fk_connection_organization'), nullable=False)
    organization: Mapped['OrganizationModel'] = relationship()

    # FIXME: add relationship with 'Settings connection' table

    @break_circular2
    def dict(self, counter=None):
        return {
            'id': self.id,
            'name': self.name,
            'connection_type': self.connection_type.dict(),
            'phone_number': self.phone_number,
            'token': self.token,
            'is_bot': self.is_bot,
            'date_created': self.date_created,
            'date_updated': self.date_updated,
            'subscription': self.subscription.dict(counter) if self.subscription else None,
            'organization_id': self.organization_id
        }


class SubscriptionStatusModel(Base):
    __tablename__ = 'subscription_status'
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(32), nullable=False)
    code = Column(String(16), nullable=False)

    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code
        }


class SubscriptionModel(Base):
    __tablename__ = 'subscription'
    id = Column(String(36), primary_key=True, default=generate_uuid)
    status_id = mapped_column(ForeignKey('subscription_status.id'), nullable=False)
    status: Mapped["SubscriptionStatusModel"] = relationship(viewonly=True)
    connection: Mapped["ConnectionModel"] = relationship(viewonly=True, )
    date_start = Column(DateTime, nullable=False)
    date_end = Column(DateTime, nullable=False)
    subscription_included = Column(Boolean, nullable=False)

    @break_circular2
    def dict(self, counter=None):
        return {
            'id': self.id,
            'status': self.status.code,
            'date_start': self.date_start,
            'date_end': self.date_end,
            'subscription_included': self.subscription_included,
            'connection': self.connection.dict(counter)
        }


class VideoModel(Base):
    __tablename__ = 'video'
    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(256), nullable=False)
    storage_reference = Column(String(1024), nullable=False) # FIXME: think about CDN storage and how to send by telegram
    date = Column(DateTime, nullable=True)

    def dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'storage_reference': self.storage_reference,
            'date': self.date
        }

    def __repr__(self):
        return f'<Video {self.title}>'

class TagModel(Base):
    __tablename__ = 'tag'
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(64), nullable=False)
    description = Column(String(256), nullable=True)
    color = Column(String(7), nullable=False)

    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'color': self.color
        }

    def __repr__(self):
        return f'<Tag {self.name}>'


class TemplateModel(Base):
    __tablename__ = 'template'
    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(64), nullable=False)
    text = Column(String(256), nullable=True)
    owner_id = mapped_column(ForeignKey('employee.id'), nullable=False)
    owner: Mapped['EmployeeModel'] = relationship()

    def dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'owner_id': self.owner_id
        }


class TypeResourceModel(Base):
    __tablename__ = 'type_resource'
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(64), nullable=True)
    code = Column(String(16), nullable=False)

    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code
        }


class PermissionModel(Base):
    __tablename__ = 'permission'
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(64), nullable=False)
    description = Column(String(256), nullable=True)
    type_resource_id = mapped_column(ForeignKey('type_resource.id'), nullable=False)
    type_resource: Mapped['TypeResourceModel'] = relationship()
    access = Column(Integer, nullable=False)
    privilege = Column(String(16), nullable=False)
    access_level = Column(String(16), nullable=False)
    role_id = mapped_column(ForeignKey('role.id'), nullable=False)

    __table_args__ = (
        CheckConstraint('access IN (0, 1)', name='access_value'),
        CheckConstraint('privilege IN ("create", "read", "write", "delete")', name='check_privilege'),
        CheckConstraint('access_level IN ("user", "organization")', name='check_access_level')
    )

    @break_circular2
    def dict(self, counter=None):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'type_resource': self.type_resource.dict(),
            'access': self.access,
            'privilege': self.privilege,
            'access_level': self.access_level,
        }


class RoleModel(Base):
    __tablename__ = 'role'
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(64), nullable=False)
    description = Column(String(256), nullable=True)
    permissions: Mapped[List['PermissionModel']] = relationship(cascade='all, delete')

    @break_circular2
    def dict(self, counter=None):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'permissions': [p.dict(counter) for p in self.permissions]
        }


class EmployeeModel(Base):
    __tablename__ = 'employee'
    id = Column(String(36), primary_key=True, default=generate_uuid)
    login = Column(String(64), nullable=False)
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(64), nullable=False)
    password = Column(String(64), nullable=False)
    status = Column(Integer, nullable=False)
    type_employee = Column(String(16), nullable=False)
    date_created = Column(DateTime, nullable=False)
    organization_id = mapped_column(ForeignKey('organization.id'), nullable=False)
    organization: Mapped['OrganizationModel'] = relationship()
    roles: Mapped[List['RoleModel']] = relationship(secondary=employee_role)

    def dict(self):
        return {
            'id': self.id,
            'login': self.login,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'status': self.status,
            'type_employee': self.type_employee,
            'organization_id': self.organization_id,
            'password': self.password,
            'roles': [r.dict() for r in self.roles]
        }


class NoteModel(Base):
    __tablename__ = 'note'
    id = Column(String(36), primary_key=True, default=generate_uuid)
    note = Column(String(256), nullable=False)
    created_date = Column(DateTime, nullable=False)
    customer_id = mapped_column(ForeignKey('customer.id'), nullable=True)
    customer: Mapped['CustomerModel'] = relationship()
    order_id = mapped_column(ForeignKey('order.id', name='order_id_fk'), nullable=True)
    order: Mapped['OrderModel'] = relationship()

    def dict(self):
        return {
            'id': self.id,
            'note': self.note,
            'date': self.created_date,
            'customer_id': self.customer_id
        }


class CustomerModel(Base):
    __tablename__ = 'customer'
    # _table_args__ = (UniqueConstraint("mobile_number1", name="customer_mobile_number1_key"),)
    id = Column(String(36), primary_key=True, default=generate_uuid)
    tg_login = Column(String(64), nullable=True)
    tg_user_id = Column(BigInteger, nullable=True)
    fullname = Column(String(510), nullable=False)
    # first_name = Column(String(64), nullable=False) # FIXME: hone logic of splitting fullname when we will use telegrams client
    # last_name = Column(String(64), nullable=False)
    mobile_number1 = Column(BigInteger, nullable=False)
    mobile_number2 = Column(BigInteger, nullable=True)
    phone_number = Column(BigInteger, nullable=True)
    email = Column(String(255), nullable=True)
    photo_id = mapped_column(ForeignKey('image.id'), nullable=True)
    photo: Mapped['ImageModel'] = relationship()
    status = Column(Integer, nullable=False)
    owner_id = mapped_column(ForeignKey('employee.id'), nullable=False)
    owner: Mapped['EmployeeModel'] = relationship()
    tags: Mapped[List['TagModel']] = relationship(secondary=tag_customer, cascade='all, delete')
    notes: Mapped[List['NoteModel']] = relationship()
    date_created = Column(DateTime, nullable=False)  # for inner purposes


    def dict(self):
        return {
            'id': self.id,
            'tg_login': self.tg_login,
            'tg_user_id': self.tg_user_id,
            'fullname': self.fullname,
            'mobile_number1': self.mobile_number1,
            'mobile_number2': self.mobile_number2,
            'phone_number': self.phone_number,
            'email': self.email,
            'photo': self.photo.dict() if self.photo else None,
            'status': self.status,
            'owner_id': self.owner_id,
            'tags': [t.dict() for t in self.tags],
            'notes': [n.dict() for n in self.notes]
        }


class MessageModel(Base):
    __tablename__ = 'message'
    id = Column(String(36), primary_key=True, default=generate_uuid)
    text = Column(String(4096), nullable=False)  # FIXME: think about parent message that divided by small parts of text
    date = Column(DateTime, nullable=False)
    dialog_id = mapped_column(ForeignKey('dialog.id'), nullable=False)
    dialog: Mapped['DialogModel'] = relationship()

    def dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'date': self.date,
            'dialog_id': self.dialog_id
        }


class DialogModel(Base):
    __tablename__ = 'dialog'
    id = Column(String(36), primary_key=True, default=generate_uuid)
    client_id = mapped_column(ForeignKey('customer.id'), nullable=False)
    client: Mapped['CustomerModel'] = relationship(cascade='delete')
    connection_id = mapped_column(ForeignKey('connection.id'), nullable=False)
    connection: Mapped['ConnectionModel'] = relationship()
    messages: Mapped[List['MessageModel']] = relationship(cascade='delete')
    last_activity = Column(DateTime, nullable=True)
    no_reply = Column(Boolean, nullable=True)
    amount_unread_msgs = Column(Integer, nullable=True)

    def dict(self):
        return {
            'id': self.id,
            'client': self.client.dict(),
            'connection_id': self.connection_id,
            'messages': [m.dict() for m in self.messages],
            'last_activity': self.last_activity,
            'no_reply': self.no_reply,
            'amount_unread_msgs': self.amount_unread_msgs
        }


class TerminalTypeModel(Base):
    __tablename__ = 'terminal_type'
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(32), nullable=False)
    code = Column(String(16), nullable=False)
    configuration_json = Column(String(1024), nullable=False)

    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'configuration_json': self.configuration_json
        }


class TerminalModel(Base):
    __tablename__ = 'terminal'
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(64), nullable=False)
    terminal_typeid = mapped_column(ForeignKey('terminal_type.id'), nullable=False)
    terminal_type: Mapped['TerminalTypeModel'] = relationship()
    date_created = Column(DateTime, nullable=False)
    connection_url = Column(String(256), nullable=False)
    connection_json = Column(String(1024), nullable=False)
    setting_id = mapped_column(ForeignKey('setting.id', name='setting_id_fk'), nullable=False)
    setting: Mapped['SettingModel'] = relationship()

    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'terminal_type': self.terminal_type.dict(),
            'date_created': self.date_created,
            'connection_url': self.connection_url,
            'connection_json': self.connection_json
        }


class OrderItemModel(Base):
    __tablename__ = 'order_item'
    id = Column(String(36), primary_key=True, default=generate_uuid)
    quantity = Column(Integer, nullable=False)
    product_id = mapped_column(ForeignKey('product.id'), nullable=False)
    product: Mapped['ProductModel'] = relationship()
    order_id = mapped_column(ForeignKey('order.id'), nullable=False)
    order: Mapped['OrderModel'] = relationship()
    def dict(self):
        return {
            'id': self.id,
            'quantity': self.quantity,
            'product_id': self.product_id,
        }


class OrderModel(Base):
    __tablename__ = 'order'
    # currency is already in ProductModel
    id = Column(String(36), primary_key=True, default=generate_uuid)
    number = Column(String(128), nullable=True)
    date = Column(DateTime, nullable=False)
    status = Column(Integer, nullable=False)
    amount = Column(Float, nullable=True)
    link_pay = Column(String(256), nullable=True)
    terminal_id = Column(String(36), ForeignKey('terminal.id'), nullable=True)
    terminal: Mapped['TerminalModel'] = relationship()
    client_id = Column(String(36), ForeignKey('customer.id'), nullable=False)
    client: Mapped['CustomerModel'] = relationship()
    items: Mapped[List['OrderItemModel']] = relationship()
    comment = Column(String(1024), nullable=True)
    notes: Mapped[List['NoteModel']] = relationship()

    def dict(self):
        return {
            'id': self.id,
            'number': self.number,
            'date': self.date,
            'status': self.status,
            'amount': self.amount,
            'link_pay': self.link_pay,
            'terminal': self.terminal.dict() if self.terminal else None,
            'client_id': self.client_id,
            'items': [i.dict() for i in self.items],
            'comment': self.comment,
            'notes': [n.dict() for n in self.notes]
        }


class NotificationModel(Base):
    __tablename__ = 'notification'
    id = Column(String(36), primary_key=True, default=generate_uuid)
    setting_id = mapped_column(ForeignKey('setting.id'), nullable=False)
    setting: Mapped['SettingModel'] = relationship()
    date_created = Column(DateTime, nullable=False)
    phone_number = Column(BigInteger, nullable=False)
    notify_trouble_integrations = Column(Boolean, nullable=False)
    notify_payments = Column(Boolean, nullable=False)
    notify_newsletters = Column(Boolean, nullable=False)

    def dict(self):
        return {
            'id': self.id,
            'setting_id': self.setting_id,
            'date_created': self.date_created,
            'phone_number': self.phone_number,
            'notify_trouble_integrations': self.notify_trouble_integrations,
            'notify_payments': self.notify_payments,
            'notify_newsletters': self.notify_newsletters
        }


class PricingModel(Base):
    __tablename__ = 'pricing'
    id = Column(String(36), primary_key=True, default=generate_uuid)
    connection_type_id = mapped_column(ForeignKey('connection_type.id', name='fk_connection_type_id'), nullable=False)
    connection_type: Mapped['ConnectionTypeModel'] = relationship(viewonly=True)
    price = Column(Float, nullable=False)
    discount_type = Column(String(16), nullable=False)
    discount = Column(Integer, nullable=False, default=0)
    currency = Column(String(3), nullable=False)

    def dict(self):
        return {
            'id': self.id,
            'connection_type': self.connection_type.dict(),
            'price': self.price,
            'discount_type': self.discount_type,
            'discount': self.discount,
            'currency': self.currency
        }


class InvoiceModel(Base):
    __tablename__ = 'invoice'
    id = Column(String(36), primary_key=True, default=generate_uuid)
    invoice_number = Column(String(256), nullable=False)
    invoice_date = Column(DateTime, nullable=False)  # like created_date
    total_amount = Column(Integer, nullable=False)
    currency = Column(String(3), nullable=False)
    discount = Column(Integer, nullable=False)  # in percentage 0-100
    start_date_subscription = Column(DateTime, nullable=False)
    end_date_subscription = Column(DateTime, nullable=False)

    buyer_name = Column(String(64), nullable=True)  # company name

    organization_id = mapped_column(ForeignKey('organization.id', name='fk_organization_id'), nullable=False)
    organization: Mapped['OrganizationModel'] = relationship(viewonly=True)
    link_invoice = Column(String(256), nullable=True)
    # invoces: Mapped[List['InvoiceModel']] = relationship(secondary=history)
    subscriptions: Mapped[List['HistoryModel']] = relationship()

    def dict(self):
        return {
            'id': self.id,
            'invoice_number': self.invoice_number,
            'invoice_date': self.invoice_date,
            'total_amount': self.total_amount,
            'currency': self.currency,
            'discount': self.discount,
            'start_date_subscription': self.start_date_subscription,
            'end_date_subscription': self.end_date_subscription,
            'buyer_name': self.buyer_name,
            'organization_id': self.organization_id,
            'link_invoice': self.link_invoice,
            'subscriptions': [s.dict() for s in self.subscriptions]
        }


class HistoryModel(Base):
    __tablename__ = 'history'
    id = Column(String(36), primary_key=True, default=generate_uuid)
    subscription_id = mapped_column(ForeignKey('subscription.id', name='fk_subscription_id'), nullable=False)
    invoice_id = mapped_column(ForeignKey('invoice.id', name='fk_invoice_id'), nullable=False)
    price = Column(Float, name='price', nullable=False)
    discount = Column(Integer, name='discount', nullable=False)
    currency = Column(String(3), nullable=False)
    date_start = Column(DateTime, nullable=False)
    date_end = Column(DateTime, nullable=False)

    def dict(self):
        return {
            'id': self.id,
            'subscription_id': self.subscription_id,
            'invoice_id': self.invoice_id,
            'price': self.price,
            'discount': self.discount,
            'currency': self.currency,
            'date_start': self.date_start,
            'date_end': self.date_end
        }

    def __repr__(self):
        return f'<History {self.id}, price: {self.price}, currency: {self.currency}>'