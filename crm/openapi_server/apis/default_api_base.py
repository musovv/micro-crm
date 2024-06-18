# coding: utf-8
import json
from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from crm.openapi_server.models.catalog import Catalog
from crm.openapi_server.models.connection import Connection
from crm.openapi_server.models.customer import Customer
from crm.openapi_server.models.dialog import Dialog
from crm.openapi_server.models.dialog_message import DialogMessage
from crm.openapi_server.models.employee import Employee
from crm.openapi_server.models.employee_role import EmployeeRole
from crm.openapi_server.models.interactive_msg import InteractiveMsg
from crm.openapi_server.models.menu import Menu
from crm.openapi_server.models.new_catalog import NewCatalog
from crm.openapi_server.models.new_connection import NewConnection
from crm.openapi_server.models.new_employee import NewEmployee
from crm.openapi_server.models.new_newsletter import NewNewsletter
from crm.openapi_server.models.new_product import NewProduct
from crm.openapi_server.models.newsletter import Newsletter
from crm.openapi_server.models.notification import Notification
from crm.openapi_server.models.order import Order
from crm.openapi_server.models.patch_users_user_id_request import PatchUsersUserIdRequest
from crm.openapi_server.models.post_user_request import PostUserRequest
from crm.openapi_server.models.role import Role
from crm.openapi_server.models.setting import Setting
from crm.openapi_server.models.shop import Shop
from crm.openapi_server.models.subscription import Subscription
from crm.openapi_server.models.tag import Tag
from crm.openapi_server.models.template import Template
from crm.openapi_server.models.user import User


class BaseDefaultApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        print('>>>DEBUG: BaseDefaultApi.__init_subclass__')
        super().__init_subclass__(**kwargs)
        BaseDefaultApi.subclasses = BaseDefaultApi.subclasses + (cls,)

    def delete_catalog_id(
        self,
        ID: str,
    ) -> None:
        ...


    def delete_connection_id(
        self,
        ID: str,
    ) -> None:
        ...


    def delete_dialog_id(
        self,
        ID: str,
    ) -> None:
        """Delete the selected chat. Only the owner of the   \&quot;company\&quot;/admin can \&quot;delete\&quot; a chat."""
        ...


    def delete_employee(
        self,
    ) -> None:
        """The owner can delete an employee \&quot;Delete\&quot;."""
        ...


    def delete_notification_id(
        self,
        ID: str,
    ) -> None:
        ...


    def delete_product_id(
        self,
        ID: str,
    ) -> None:
        ...


    def delete_role_id(
        self,
        ID: str,
    ) -> None:
        ...


    def delete_shop_id(
        self,
        ID: str,
    ) -> None:
        ...


    def delete_tag(
        self,
    ) -> None:
        ...


    def delete_template(
        self,
    ) -> None:
        """The user can \&quot;delete\&quot; the template."""
        ...


    def get_catalog(
        self,
    ) -> List[Catalog]:
        """The user returns a list of directories."""

        payload = '[{"id": "b22815a1-c580-4661-bb49-d6ce4c3cdf93", "name": "catalog1", "product_ids": ["1","2","3"]}]'

        # convert json to list of Catalog objects:
        data = json.loads(payload)
        catalogs = []
        for item in data:
            catalogs.append(Catalog(**item))
        return catalogs

    def get_catalog_id(
        self,
        ID: str,
    ) -> NewCatalog:
        ...


    def get_client_find_by_tags(
        self,
        tags: str,
        owner_id: str,
        search: str,
    ) -> List[Customer]:
        ...


    def get_client_id(
        self,
        ID: str,
    ) -> Customer:
        ...


    def get_connection(
        self,
    ) -> List[Connection]:
        ...


    def get_connection_id(
        self,
        ID: str,
    ) -> NewConnection:
        ...


    def get_customer(
        self,
        owner_id: str,
        serch: str,
    ) -> List[Customer]:
        """Return the contact list."""
        ...


    def get_dialog(
        self,
        search: str,
    ) -> List[Dialog]:
        """We return a list of chats with the ability to filter   by telegram/instagram/whatsapp channels.   In chats, contact numbers are not displayed, only nicknames,   and you cannot write to the first client."""
        ...


    def get_dialog_id(
        self,
        ID: str,
    ) -> DialogMessage:
        ...


    def get_employee(
        self,
    ) -> List[Employee]:
        """Return the list of the company&#39;s employees."""
        ...


    def get_employee_id(
        self,
        ID: str,
    ) -> Employee:
        ...


    def get_interactive_msg(
        self,
        type_msg: str,
    ) -> List[InteractiveMsg]:
        """Return a list of interactive messages with the ability to   filter by text/image/video/document channels."""
        ...


    def get_interactive_msg_id(
        self,
        ID: str,
        type_msg: str,
    ) -> InteractiveMsg:
        ...


    def get_menu(
        self,
        employee: str,
    ) -> List[Menu]:
        """After the first stage of authorization on the site,   we proceed to the stage of loading the dashboard,   i.e. loading the central menu.   The list of menu items is loaded through   the user&#39;s permissions by passing the ID of the authorized user."""
        ...


    def get_newsletter(
        self,
    ) -> object:
        ...


    def get_newsletter_id_(
        self,
        ID: str,
    ) -> Newsletter:
        ...


    def get_notification(
        self,
        setting_id: str,
    ) -> object:
        ...


    def get_order(
        self,
        client_id: str,
    ) -> List[Order]:
        ...


    def get_order_id(
        self,
        ID: str,
    ) -> Order:
        ...


    def get_product(
        self,
    ) -> object:
        ...


    def get_product_id(
        self,
        ID: str,
    ) -> NewProduct:
        ...


    def get_role(
        self,
    ) -> List[Role]:
        ...


    def get_role_id(
        self,
        ID: str,
    ) -> Role:
        ...


    def get_setting_id(
        self,
        ID: str,
    ) -> Setting:
        ...


    def get_shop(
        self,
    ) -> object:
        ...


    def get_shop_id(
        self,
        ID: str,
    ) -> Shop:
        ...


    def get_subscription(
        self,
    ) -> object:
        ...


    def get_subscription_id(
        self,
        ID: str,
    ) -> Subscription:
        ...


    def get_tag(
        self,
    ) -> object:
        ...


    def get_tag_id(
        self,
        ID: str,
    ) -> Tag:
        ...


    def get_template(
        self,
    ) -> List[Template]:
        """Return a list of templates."""
        ...


    def get_template_id(
        self,
        ID: str,
    ) -> Template:
        ...


    def get_users_user_id(
        self,
        userId: int,
    ) -> User:
        """Retrieve the information of the user with the matching user ID."""
        ...


    def interactive_msg_id_delete(
        self,
        ID: str,
    ) -> None:
        """"""
        ...


    def patch_users_user_id(
        self,
        userId: int,
        patch_users_user_id_request: PatchUsersUserIdRequest,
    ) -> User:
        """Update the information of an existing user."""
        ...


    def post_catalog(
        self,
        new_catalog: NewCatalog,
    ) -> NewCatalog:
        """The user can create a catalog,   add a catalog name and products."""
        ...


    def post_connection(
        self,
        new_connection: NewConnection,
    ) -> NewConnection:
        """When creating a new connection,   the user selects a connection channel from the existing ones,   falls into it, and selects \&quot;Add bot\&quot; or \&quot;Phone number\&quot;."""
        ...


    def post_customer(
        self,
        customer: Customer,
    ) -> Customer:
        """A customer can \&quot;Create\&quot; a new contact.   Add First Name/Last Name, phone number   (you can choose a country code), e-mail, tags.   You can add multiple phone numbers or e-mails   to each contact. ! The employee&#39;s photo is set    during the first correspondence with the client.   When you create a photo, it is not transferred."""
        ...


    def post_dialog(
        self,
        dialog: Dialog,
    ) -> Dialog:
        """When creating a new chat, the user specifies the   \&quot;Where to write\&quot; bot and the \&quot;Where to write\&quot; phone number,   or selects a number `from `the contact list,   if one has been created."""
        ...


    def post_dialog_id_no_answer(
        self,
        id: str,
        is_reply: int,
    ) -> None:
        """The user can specify in a specific   chat whether or not a response is required."""
        ...


    def post_dialog_id_reply(
        self,
        id: str,
        message: str,
        message2: str,
    ) -> None:
        """Send a message."""
        ...


    def post_employee(
        self,
        new_employee: NewEmployee,
    ) -> NewEmployee:
        """Only the owner can \&quot;add an employee\&quot; and assign an \&quot;employee role\&quot;.   The owner is automatically established when the system is connected and the company&#39;s email   address is specified when connecting.   When an employee is added, the owner copies the link and sends it to the email   of the employee who needs to be added.   After clicking on the link, the employee registers in the system to gain access."""
        ...


    def post_employee_create_new_employee(
        self,
        email: str,
    ) -> str:
        ...


    def post_interactive_msg(
        self,
        interactive_msg: InteractiveMsg,
    ) -> InteractiveMsg:
        """The user can \&quot;create\&quot; an actionable message,   enter the name of the template, select the type   of template title, fill in the text, and optionally the footer."""
        ...


    def post_newsletter(
        self,
        new_newsletter: NewNewsletter,
    ) -> Newsletter:
        """The user can send messages via WABA, WhatsApp (Unofficial integration),  Telegram, Telegram Bot. Access to the \&quot;Campaigns\&quot; section is available   only to users with \&quot;administrator\&quot;, \&quot;owner\&quot; rights and those employees    who have these access rights in the \&quot;Settings\&quot; - \&quot;Employees\&quot; section Important:    When sending messages through the unofficial integration of WhatsApp and Telegram,   be careful, as the number may be blocked. Refunds for the subscription, in case of   blocking (banning) of the number, are not carried out. We recommend that you familiarize   yourself with the recommendations for mailings so as not to get banned:   Recommendation for WhatsApp Recommendation for Telegram."""
        ...


    def post_newsletter_id_cancel(
        self,
        ID: str,
    ) -> Newsletter:
        """Unsubscribe."""
        ...


    def post_notification(
        self,
        notification: Notification,
    ) -> Notification:
        ...


    def post_order(
        self,
        order: Order,
    ) -> Order:
        ...


    def post_product(
        self,
        new_product: NewProduct,
    ) -> NewProduct:
        ...


    def post_role(
        self,
        role: Role,
    ) -> Role:
        ...


    def post_shop(
        self,
        shop: Shop,
    ) -> Shop:
        ...


    def post_subscription_pay(
        self,
    ) -> str:
        """Cancel of subscription"""
        ...


    def post_tag(
        self,
        tag: Tag,
    ) -> Tag:
        ...


    def post_template(
        self,
        template: Template,
    ) -> Template:
        """A user can \&quot;Create\&quot; a template by adding a template title and its text. There is also   an option to insert an image/video/emoticon."""
        ...


    def post_user(
        self,
        post_user_request: PostUserRequest,
    ) -> User:
        """Create a new user."""
        ...


    def put_catalog(
        self,
        new_catalog: NewCatalog,
    ) -> NewCatalog:
        """The user can \&quot;Edit\&quot; an already created catalog,   change the \&quot;Name\&quot;, \&quot;Add\&quot; or vice versa \&quot;Remove\&quot; the product."""
        ...


    def put_client(
        self,
        customer: Customer,
    ) -> Customer:
        """The user can make changes to an already created   contact: change the first and last name,  add a tag, add a note, add a phone number, add an e-mail."""
        ...


    def put_connection(
        self,
        new_connection: NewConnection,
    ) -> NewConnection:
        """The user can make changes to the \&quot;Edit\&quot; connection   channel and change the \&quot;Connection Name\&quot;."""
        ...


    def put_employee(
        self,
        employee_role: List[EmployeeRole],
    ) -> List[EmployeeRole]:
        """The user can make changes to the \&quot;Edit\&quot; employee and change the \&quot;Employee role\&quot;,   as well as grant or restrict \&quot;Access rights\&quot;."""
        ...


    def put_interactive_msg(
        self,
        interactive_msg: InteractiveMsg,
    ) -> InteractiveMsg:
        """The user can \&quot;edit\&quot; an interactive message   by making changes to the text, image,   video, document, header, footer, button."""
        ...


    def put_newsletter(
        self,
        new_newsletter: NewNewsletter,
    ) -> Newsletter:
        """In case the mailing has not yet been sent and   has the status \&quot;scheduled\&quot;, then we can update the   text and the list of clients and change the time of sending."""
        ...


    def put_notification(
        self,
        notification: Notification,
    ) -> Notification:
        ...


    def put_product(
        self,
        new_product: NewProduct,
    ) -> NewProduct:
        ...


    def put_role(
        self,
        role: Role,
    ) -> Role:
        ...


    def put_setting(
        self,
        setting: Setting,
    ) -> Setting:
        ...


    def put_shop(
        self,
        shop: Shop,
    ) -> Shop:
        ...


    def put_subscription(
        self,
        body: List[Subscription],
    ) -> object:
        """Update only \&quot;included_subscribe\&quot;"""
        ...


    def put_tag(
        self,
        tag: Tag,
    ) -> Tag:
        ...


    def put_template(
        self,
        template: Template,
    ) -> Template:
        """The user can \&quot;Edit\&quot; the template by changing the title and text   (along with the content of the text)."""
        ...
