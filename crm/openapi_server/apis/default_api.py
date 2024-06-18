# coding: utf-8
import json
import os
from typing import Dict, List, Union, TYPE_CHECKING, Optional
import importlib
import pkgutil


from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    Path,
    Query,
    Response,
    Security,
    status, FastAPI,
)
from pydantic import BaseModel

from crm.business_service.bases import DialogBase
from crm.business_service.catalogs_service import CatalogService
from crm.business_service.connection_service import ConnectionService
from crm.business_service.customer_service import CustomerService
from crm.business_service.dialog_service import DialogService
from crm.business_service.employee_service import EmployeeService
from crm.business_service.order_service import OrderService
from crm.business_service.organization_service import OrganizationService
from crm.business_service.price_service import PriceService
from crm.business_service.role_service import RoleService
from crm.business_service.subscription_service import SubscriptionService
from crm.business_service.template_service import TemplateService
from crm.business_service.terminal_service import TerminalService
from crm.openapi_server.models.extra_models import TokenModel  # noqa: F401
from crm.openapi_server.models.catalog import Catalog
from crm.openapi_server.models.connection import Connection
from crm.openapi_server.models.customer import Customer
from crm.openapi_server.models.dialog import Dialog
from crm.openapi_server.models.dialog_message import DialogMessage
from crm.openapi_server.models.employee import Employee
from crm.openapi_server.models.employee_role import EmployeeRole
from crm.openapi_server.models.history import History
from crm.openapi_server.models.interactive_msg import InteractiveMsg
from crm.openapi_server.models.invoice import Invoice
from crm.openapi_server.models.menu import Menu
from crm.openapi_server.models.new_catalog import NewCatalog
from crm.openapi_server.models.new_connection import NewConnection
from crm.openapi_server.models.new_dialog import NewDialog
from crm.openapi_server.models.new_employee import NewEmployee
from crm.openapi_server.models.new_newsletter import NewNewsletter
from crm.openapi_server.models.new_product import NewProduct
from crm.openapi_server.models.newsletter import Newsletter
from crm.openapi_server.models.notification import Notification
from crm.openapi_server.models.order import Order
from crm.openapi_server.models.patch_users_user_id_request import PatchUsersUserIdRequest
from crm.openapi_server.models.pay_subscription import PaySubscriptions
from crm.openapi_server.models.post_user_request import PostUserRequest
from crm.openapi_server.models.pricing import Pricing
from crm.openapi_server.models.product import Product
from crm.openapi_server.models.role import Role
from crm.openapi_server.models.setting import Setting
from crm.openapi_server.models.shop import Shop
from crm.openapi_server.models.subscription import Subscription
from crm.openapi_server.models.tag import Tag
from crm.openapi_server.models.template import Template
from crm.openapi_server.models.terminal import Terminal
from crm.openapi_server.models.user import User
from crm.repository.catalog_repository import CatalogRepository
from crm.repository.connection_repository import ConnectionRepository
from crm.repository.customer_repository import CustomerRepository
from crm.repository.dialog_repository import DialogRepository
from crm.repository.employee_repository import EmployeeRepository
from crm.repository.order_repository import OrderRepository
from crm.repository.organization_repository import OrganizationRepository
from crm.repository.price_repository import PriceRepository
from crm.repository.role_repository import RoleRepository
from crm.repository.subscription_repository import SubscriptionRepository
from crm.repository.template_repository import TemplateRepository
from crm.repository.terminal_repository import TerminalRepository
from crm.repository.unit_of_work import UnitOfWork

# if TYPE_CHECKING:
from crm.business_service.products_service import ProductsService
from crm.repository.products_repository import ProductsRepository

from starlette.requests import Request

router = APIRouter()

# ns_pkg = crm.openapi_server.impl
# for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
#     importlib.import_module(name)


@router.delete(
    "/catalog/{ID}/",
    responses={
        200: {"description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def delete_catalog_id(
    ID: str = Path(description=""),
) -> None:
    with UnitOfWork() as unit:
        repo = CatalogRepository(unit.session)
        service = CatalogService(repo)
        service.delete_catalog(ID)
        unit.commit()



@router.delete(
    "/{org_id}/connection/{id}/",
    responses={
        200: {"description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def delete_connection_id(
    request: Request,
    org_id: str = Path(description="Organization ID"),
    id: str = Path(description=""),
) -> None:
    with UnitOfWork() as unit:
        repo = ConnectionRepository(unit.session)
        service = ConnectionService(repo)
        service.delete_connection(id, org_id, request.state.user_id)
        unit.commit()


@router.delete(
    "/dialog/{ID}/",
    responses={
        200: {"description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def delete_dialog_id(
    request: Request,
    ID: str = Path(description=""),
) -> None:
    """Delete the selected chat. Only the owner of the   \&quot;company\&quot;/admin can \&quot;delete\&quot; a chat."""

    with UnitOfWork() as unit:
        repo = DialogRepository(unit.session)
        service = DialogService(repo)
        service.delete_dialog(ID, request.state.user_id)
        unit.commit()


@router.delete('/customer/{ID}/')
async def delete_customer_id(
    ID: str = Path(description=""),
) -> None:
    pass  # We can delete a customer through the dialog object


@router.delete(
    "/employee/{ID}",
    responses={
        200: {"description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def delete_employee(
    ID: str = Path(description=""),
) -> None:
    """The owner can delete an employee 'Delete'."""
    with UnitOfWork() as unit:
        repo = EmployeeRepository(unit.session)
        service = EmployeeService(repo)
        service.delete_employee(ID)
        unit.commit()



@router.delete(
    "/notification/{ID}",
    responses={
        200: {"description": "OK"},
    },
    tags=["default"],
    summary="Delete a notification",
    response_model_by_alias=True,
)
async def delete_notification_id(
    ID: str = Path(description=""),
) -> None:
    ...


@router.delete(
    "/product/{ID}",
    responses={
        200: {"description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def delete_product_id(
    ID: str = Path(description=""),
) -> None:
    with UnitOfWork() as unit:
        repo = ProductsRepository(unit.session)
        service = ProductsService(repo)
        service.delete_product(ID)
        unit.commit()


@router.delete(
    "/role/{ID}/",
    responses={
        200: {"description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def delete_role_id(
    ID: str = Path(description=""),
) -> None:
    with UnitOfWork() as unit:
        repo = RoleRepository(unit.session)
        service = RoleService(repo)
        service.delete_role(ID)
        unit.commit()


@router.delete(
    "/shop/{ID}",
    responses={
        200: {"description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def delete_shop_id(
    ID: str = Path(description=""),
) -> None:
    ...


@router.delete(
    "/tag",
    responses={
        200: {"description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def delete_tag(
) -> None:
    ...


@router.delete(
    "/template/{ID}",
    responses={
        200: {"description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def delete_template(
    ID: str = Path(description=""),
) -> None:
    """The user can \&quot;delete\&quot; the template."""
    with UnitOfWork() as unit:
        repo = TemplateRepository(unit.session)
        service = TemplateService(repo)
        service.delete_template(ID)
        unit.commit()


@router.get(
    "/organization/",
    responses={
        200: {"model": Setting, "description": "OK"},
    },
    tags=["default"],
    summary="Get organization",
    response_model_by_alias=True
)
async def get_organization(
        request: Request,
) -> List[Setting]:
    with UnitOfWork() as unit:
        repo = OrganizationRepository(unit.session)
        service = OrganizationService(repo)
        orgs = service.list_organizations(request.state.user_id)
        return [org.dict() for org in orgs]


@router.get(
    "/catalog/",
    responses={
        200: {"model": List[Catalog], "description": "OK"},
    },
    tags=["default"],
    summary="Get list catalogs",
    response_model_by_alias=True,
)
async def get_catalog(
) -> List[Catalog]:

    with UnitOfWork() as unit:
        repo = CatalogRepository(unit.session)
        service = CatalogService(repo)
        catalogs = service.list_catalogs()
        return catalogs


@router.get(
    "/catalog/{ID}/",
    responses={
        200: {"model": NewCatalog, "description": "OK"},
    },
    tags=["default"],
    summary="Get a catalog",
    response_model_by_alias=True,
)
async def get_catalog_id(
    ID: str = Path(description=""),
) -> NewCatalog:
    with UnitOfWork() as unit:
        repo = CatalogRepository(unit.session)
        service = CatalogService(repo)
        return service.get_catalog(ID)



@router.get(
    "/client/findByTags/",
    responses={
        200: {"model": List[Customer], "description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def get_customer_find_by_tags(
    request: Request,
    tags: List[str] = Query(None, description="", alias="tags"),
    search: str = Query(None, description="", alias="search"),
) -> List[Customer]:
    """Return the contact list."""
    with UnitOfWork() as unit:
        repo = CustomerRepository(unit.session)
        service = CustomerService(repo)
        filters = {'tags': tags, 'search': search}
        results = service.get_all_customers(request.state.user_id, **filters)
        return [result.dict() for result in results]


@router.get(
    "/client/{ID}/",
    responses={
        200: {"model": Customer, "description": "OK"},
    },
    tags=["default"],
    summary="Get a client",
    response_model_by_alias=True,
)
async def get_customer_id(
    request: Request,
    ID: str = Path(description=""),
) -> Customer:
    with UnitOfWork() as unit:
        repo = CustomerRepository(unit.session)
        service = CustomerService(repo)
        result = service.get_customer(ID, request.state.user_id)
        return result.dict()


@router.get(
    "/{org_id}/connection/",
    responses={
        200: {"model": List[Connection], "description": "OK"},
    },
    tags=["default"],
    summary="Get list connections",
    response_model_by_alias=True,
)
async def get_connection(
        request: Request,
        org_id: str = Path(description="Organization ID"),
        limit: int = 10,
) -> List[Connection]:
    with UnitOfWork() as unit:
        repo = ConnectionRepository(unit.session)
        service = ConnectionService(repo)
        results = service.list_connections(org_id, request.state.user_id, **{'limit': limit})
        return [result.dict(cls_map=Connection) for result in results]


@router.get(
    "/{org_id}/connection/{id}/",
    responses={
        200: {"model": NewConnection, "description": "OK"},
    },
    tags=["default"],
    summary="Get the connection",
    response_model_by_alias=True,
)
async def get_connection_id(
    request: Request,
    org_id: str = Path(description=""),
    id: str = Path(description=""),
) -> NewConnection:
    with UnitOfWork() as unit:
        repo = ConnectionRepository(unit.session)
        service = ConnectionService(repo)
        result = service.get_connection(id, org_id, request.state.user_id)
        return result.dict(cls_map=NewConnection)


@router.get(
    "/client/",
    responses={
        200: {"model": List[Customer], "description": "OK"},
    },
    tags=["default"],
    summary="Get list clients",
    response_model_by_alias=True,
)
async def get_customer(
    # owner_id: str = Query(None, description="", alias="owner_id"),
    request: Request,
    serch: str = Query(None, description="", alias="serch"),
) -> List[Customer]:
    """Return the contact list."""
    with UnitOfWork() as unit:
        repo = CustomerRepository(unit.session)
        service = CustomerService(repo)
        user_id = request.state.user_id
        results = service.get_all_customers(**{"user_id": user_id})
        return [result.dict() for result in results]


@router.get(
    "/dialog/",
    responses={
        200: {"model": List[Dialog], "description": "OK"},
    },
    tags=["default"],
    summary="Get list of dialogs",
    response_model_by_alias=True,
)
async def get_dialog(
    request: Request,
    search: str = Query(None, description="search someone by word", alias="search"),
) -> List[Dialog]:
    """We return a list of chats with the ability to filter
    by telegram/instagram/whatsapp channels.
    In chats, contact numbers are not displayed, only nicknames,
    and you cannot write to the first client."""

    with UnitOfWork() as unit:
        repo = DialogRepository(unit.session)
        service = DialogService(repo)
        results = service.get_dialogs(user_id=request.state.user_id, **{})
        return [result.dict() for result in results]


@router.get(
    "/dialog/{ID}/",
    responses={
        200: {"model": DialogMessage, "description": "OK"},
    },
    tags=["default"],
    summary="Get the dialog",
    response_model_by_alias=True,
)
async def get_dialog_id(
    request: Request,
    ID: str = Path(description=""),
) -> DialogMessage:
    with UnitOfWork() as unit:
        repo = DialogRepository(unit.session)
        service = DialogService(repo)
        result = service.get_dialog(ID, request.state.user_id)
        return result.dict(cls_map=DialogMessage)


@router.get(
    "/employee/",
    responses={
        200: {"model": List[Employee], "description": "OK"},
    },
    tags=["default"],
    summary="Get list employees",
    response_model_by_alias=True,
)
async def get_employee(
) -> List[Employee]:
    """Return the list of the company&#39;s employees."""
    with UnitOfWork() as unit:
        repo = EmployeeRepository(unit.session)
        service = EmployeeService(repo)
        results = service.get_all_employees(**{})
        return [result.dict(cls_map=Employee) for result in results]


@router.get(
    "/employee/{ID}",
    responses={
        200: {"model": EmployeeRole, "description": "OK"},
    },
    tags=["default"],
    summary="Get an employee",
    response_model_by_alias=True,
)
async def get_employee_id(
    ID: str = Path(description="")
) -> EmployeeRole:
    with UnitOfWork() as unit:
        repo = EmployeeRepository(unit.session)
        service = EmployeeService(repo)
        result = service.get_employee(ID)
        return result.dict(cls_map=EmployeeRole)


@router.get(
    "/interactive_msg/",
    responses={
        200: {"model": List[InteractiveMsg], "description": "OK"},
    },
    tags=["default"],
    summary="Get list interactive msgs",
    response_model_by_alias=True,
)
async def get_interactive_msg(
    type_msg: str = Query(None, description="text, document, photo, video", alias="type_msg"),
) -> List[InteractiveMsg]:
    """Return a list of interactive messages with the ability to   filter by text/image/video/document channels."""
    return BaseDefaultApi.subclasses[0]().get_interactive_msg(type_msg)


@router.get(
    "/interactive_msg/{ID}/",
    responses={
        200: {"model": InteractiveMsg, "description": "OK"},
    },
    tags=["default"],
    summary="Get a interactive msg",
    response_model_by_alias=True,
)
async def get_interactive_msg_id(
    ID: str = Path(description=""),
    type_msg: str = Query(None, description="text, document, photo, video", alias="type_msg"),
) -> InteractiveMsg:
    ...


@router.get(
    "/menu/",
    responses={
        200: {"model": List[Menu], "description": "OK"},
    },
    tags=["default"],
    summary="Get a menu",
    response_model_by_alias=True,
)
async def get_menu(
    employee: str = Query(None, description="", alias="employee"),
) -> List[Menu]:
    """After the first stage of authorization on the site,   we proceed to the stage of loading the dashboard,   i.e. loading the central menu.   The list of menu items is loaded through   the user&#39;s permissions by passing the ID of the authorized user."""
    return BaseDefaultApi.subclasses[0]().get_menu(employee)


@router.get(
    "/newsletter/",
    responses={
        200: {"model": object, "description": "OK"},
    },
    tags=["default"],
    summary="Get list newsletter",
    response_model_by_alias=True,
)
async def get_newsletter(
) -> object:
    ...


@router.get(
    "/Newsletter/{ID}.",
    responses={
        200: {"model": Newsletter, "description": "OK"},
    },
    tags=["default"],
    summary="Get a newsletter",
    response_model_by_alias=True,
)
async def get_newsletter_id_(
    ID: str = Path(description=""),
) -> Newsletter:
    ...


@router.get(
    "/notification",
    responses={
        200: {"model": object, "description": "OK"},
    },
    tags=["default"],
    summary="Get list notifications",
    response_model_by_alias=True,
)
async def get_notification(
    setting_id: str = Query(None, description="", alias="SETTING_ID"),
) -> object:
    ...


@router.get(
    "/order/",
    responses={
        200: {"model": List[Order], "description": "OK"},
    },
    tags=["default"],
    summary="Get list of orders",
    response_model_by_alias=True,
)
async def get_order(
    request: Request,
    client_id: str = Query(None, description="filter by client", alias="client_id"),
) -> List[Order]:

    with UnitOfWork() as unit:
        repo = OrderRepository(unit.session)
        service = OrderService(repo)
        results = service.list_orders(**{'user_id': request.state.user_id, 'client_id': client_id})
        return [result.dict() for result in results]


@router.get(
    "/order/{ID}/",
    responses={
        200: {"model": Order, "description": "OK"},
    },
    tags=["default"],
    summary="Get Order",
    response_model_by_alias=True,
)
async def get_order_id(
    request: Request,
    ID: str = Path(description=""),
) -> Order:
    with UnitOfWork() as unit:
        repo = OrderRepository(unit.session)
        service = OrderService(repo)
        result = service.get_order(ID, request.state.user_id)
        return result.dict()


@router.get(
    "/product",
    responses={
        200: {"model": object, "description": "OK"},
    },
    tags=["default"],
    summary="Get list products",
    response_model_by_alias=True,
)
async def get_product(
) -> List[Product]:
    with UnitOfWork() as unit:
        repo = ProductsRepository(unit.session)
        service = ProductsService(repo)
        results = service.list_products(**{})  #FIXME pass filters
        return results


@router.get(
    "/product/{ID}",
    responses={
        200: {"model": NewProduct, "description": "OK"},
    },
    tags=["default"],
    summary="Get a product",
    response_model_by_alias=True,
)
async def get_product_id(
    ID: str = Path(description=""),
) -> NewProduct:
    with UnitOfWork() as unit:
        repo = ProductsRepository(unit.session)
        service = ProductsService(repo)
        result = service.get_product(ID)
        return result.dict(cls_map=NewProduct)


@router.get(
    "/role/",
    responses={
        200: {"model": List[Role], "description": "OK"},
    },
    tags=["default"],
    summary="Get list roles",
    response_model_by_alias=True,
)
async def get_role(limit: Optional[int] = None) -> List[Role]:
    with UnitOfWork() as unit:
        repo = RoleRepository(unit.session)
        service = RoleService(repo)
        results = service.list_roles(**{'limit': limit})
        return [result.dict() for result in results]


@router.get(
    "/role/{ID}/",
    responses={
        200: {"model": Role, "description": "OK"},
    },
    tags=["default"],
    summary="Get a role",
    response_model_by_alias=True,
)
async def get_role_id(
    ID: str = Path(description=""),
) -> Role:
    with UnitOfWork() as unit:
        repo = RoleRepository(unit.session)
        service = RoleService(repo)
        result = service.get_role_by_id(ID)
        return result.dict()


@router.get(
    "/setting/{ID}",
    responses={
        200: {"model": Setting, "description": "OK"},
    },
    tags=["default"],
    summary="Get a setting",
    response_model_by_alias=True,
)
async def get_setting_id(
    ID: str = Path(description=""),
) -> Setting:
    ...


@router.get(
    "/shop",
    responses={
        200: {"model": object, "description": "OK"},
    },
    tags=["default"],
    summary="Get list shops",
    response_model_by_alias=True,
)
async def get_shop(
) -> object:
    ...


@router.get(
    "/shop/{ID}",
    responses={
        200: {"model": Shop, "description": "OK"},
    },
    tags=["default"],
    summary="Get a shop",
    response_model_by_alias=True,
)
async def get_shop_id(
    ID: str = Path(description=""),
) -> Shop:
    ...


@router.get(
    "/{org_id}/subscription/",
    responses={
        200: {"model": object, "description": "OK"},
    },
    tags=["default"],
    summary="Get list subscription",
    response_model_by_alias=True,
)
async def get_subscription(
        request: Request,
        org_id: str = Path(description="Organization ID"),
        limit: int = 10,
) -> List[Subscription]:
    with UnitOfWork() as unit:
        repo = SubscriptionRepository(unit.session)
        service = SubscriptionService(repo)
        results = service.list_subscriptions(org_id, request.state.user_id, **{'limit': limit})
        return [result.dict() for result in results]


@router.get(
    "/subscription/{ID}",
    responses={
        200: {"model": Subscription, "description": "OK"},
    },
    tags=["default"],
    summary="Get a subscription",
    response_model_by_alias=True,
)
async def get_subscription_id(
    ID: str = Path(description=""),
) -> Subscription:
    ...


@router.get(
    "/{org_id}/charge/",
    responses={
        200: {"model": Pricing, "description": "OK"},
    },
    tags=["default"],
    summary="Get list prices",
    response_model_by_alias=True,
)
async def get_prices(
    request: Request,
    org_id: str = Path(description="Organization ID"),
    limit=10
) -> List[Pricing]:
    with UnitOfWork() as unit:
        repo = PriceRepository(unit.session)
        service = PriceService(repo)
        results = service.list_prices(org_id, request.state.user_id, limit=limit, **{})
        return [result.dict() for result in results]


@router.get(
    "/tag",
    responses={
        200: {"model": object, "description": "OK"},
    },
    tags=["default"],
    summary="Get list tags",
    response_model_by_alias=True,
)
async def get_tag(
) -> object:
    ...


@router.get(
    "/tag/{ID}",
    responses={
        200: {"model": Tag, "description": "OK"},
    },
    tags=["default"],
    summary="Get a tag",
    response_model_by_alias=True,
)
async def get_tag_id(
    ID: str = Path(description=""),
) -> Tag:
    ...


@router.get(
    "/{org_id}/terminal/",
    responses={
        200: {"model": List[Terminal], "description": "OK"},
    },
    tags=["default"],
    summary="Get list terminals",
    response_model_by_alias=True,
)
async def get_terminal(
    request: Request,
    org_id: str = Path(description="Organization ID"),

) -> List[Terminal]:
    with UnitOfWork() as unit:
        repo = TerminalRepository(unit.session)
        service = TerminalService(repo)
        results = service.list_terminal(org_id, request.state.user_id, **{})
        return [result.dict() for result in results]


@router.get(
    "/template/",
    responses={
        200: {"model": List[Template], "description": "OK"},
    },
    tags=["default"],
    summary="Get list templates",
    response_model_by_alias=True,
)
async def get_template(
) -> List[Template]:
    """Return a list of templates."""
    with UnitOfWork() as unit:
        repo = TemplateRepository(unit.session)
        service = TemplateService(repo)
        results = service.list_templates(**{})
        return [result.dict() for result in results]


@router.get(
    "/template/{ID}/",
    responses={
        200: {"model": Template, "description": "OK"},
    },
    tags=["default"],
    summary="Get a template",
    response_model_by_alias=True,
)
async def get_template_id(
    ID: str = Path(description=""),
) -> Template:
    with UnitOfWork() as unit:
        repo = TemplateRepository(unit.session)
        service = TemplateService(repo)
        result = service.get_template(ID)
        return result.dict()


@router.get(
    "/users/{userId}",
    responses={
        200: {"model": User, "description": "User Found"},
        404: {"description": "User Not Found"},
    },
    tags=["default"],
    summary="Get User Info by User ID",
    response_model_by_alias=True,
)
async def get_users_user_id(
    userId: int = Path(description="Id of an existing user."),
) -> User:
    """Retrieve the information of the user with the matching user ID."""
    return BaseDefaultApi.subclasses[0]().get_users_user_id(userId)


@router.delete(
    "/{org_id}/terminal/{id}/",
    responses={
        200: {"description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def delete_terminal_id(
    request: Request,
    org_id: str = Path(description="Organization ID"),
    id: str = Path(description="Terminal ID"),
) -> None:
    with UnitOfWork() as unit:
        repo = TerminalRepository(unit.session)
        service = TerminalService(repo)
        service.delete_terminal(id, org_id, user_id=request.state.user_id)
        unit.commit()


@router.delete(
    "/interactive_msg/{ID}/",
    responses={
    },
    tags=["default"],
    response_model_by_alias=True,
)
async def interactive_msg_id_delete(
    ID: str = Path(description=""),
) -> None:
    """"""
    return BaseDefaultApi.subclasses[0]().interactive_msg_id_delete(ID)


@router.patch(
    "/users/{userId}",
    responses={
        200: {"model": User, "description": "User Updated"},
        404: {"description": "User Not Found"},
        409: {"description": "Email Already Taken"},
    },
    tags=["default"],
    summary="Update User Information",
    response_model_by_alias=True,
)
async def patch_users_user_id(
    userId: int = Path(description="Id of an existing user."),
    patch_users_user_id_request: PatchUsersUserIdRequest = Body(None, description="Patch user properties to update."),
) -> User:
    """Update the information of an existing user."""
    return BaseDefaultApi.subclasses[0]().patch_users_user_id(userId, patch_users_user_id_request)


@router.post(
    "/organization/",
    responses={
        200: {"model": Setting, "description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def post_organization(
    setting: Setting = Body(None, description=""),
) -> Setting:
    """First initialization of organization"""

    with UnitOfWork() as unit:
        repo = OrganizationRepository(unit.session)
        service = OrganizationService(repo)
        result = service.create_organization(**setting.dict())
        Setting.validate(result.dict())
        unit.commit()
        return result.dict()


@router.post(
    "/{ORG_ID}/terminal/",
    responses={
        200: {"model": Terminal, "description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def post_terminal(
    request: Request,
    ORG_ID: str = Path(description="Organization ID"),
    terminal: Terminal = Body(None, description=""),
) -> Terminal:
    with UnitOfWork() as unit:
        repo = TerminalRepository(unit.session)
        service = TerminalService(repo)
        result = service.create_terminal(org_id=ORG_ID, **terminal.dict())
        Terminal.validate(result.dict())
        unit.commit()
        return result.dict()


@router.post(
    "/catalog/",
    responses={
        200: {"model": NewCatalog, "description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def post_catalog(
    new_catalog: NewCatalog = Body(None, description=""),
) -> NewCatalog:
    """The user can create a catalog,   add a catalog name and products."""

    with UnitOfWork() as unit:
        repo = CatalogRepository(unit.session)
        service = CatalogService(repo)
        result = service.create_catalog(**new_catalog.dict())
        result = NewCatalog(**result.dict(NewCatalog))
        unit.commit()
        return result


@router.post(
    "/{org_id}/connection/",
    responses={
        200: {"model": NewConnection, "description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def post_connection(
    request: Request,
    org_id: str = Path(description="Organization ID"),
    new_connection: NewConnection = Body(None, description="обьект \&quot;Создать подключение\&quot;"),
) -> NewConnection:
    """When creating a new connection,   the user selects a connection channel from the existing ones,   falls into it, and selects \&quot;Add bot\&quot; or \&quot;Phone number\&quot;."""

    with UnitOfWork() as unit:
        repo = ConnectionRepository(unit.session)
        service = ConnectionService(repo)
        entity = service.create_connection(org_id, request.state.user_id, **new_connection.dict())
        d = entity.dict(cls_map=NewConnection)
        NewConnection.validate(d)
        unit.commit()
        return NewConnection(**entity.dict(cls_map=NewConnection))


@router.post(
    "/client/",
    responses={
        200: {"model": Customer, "description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def post_customer(
    request: Request,
    customer: Customer = Body(None, description="  ")
) -> Customer:

    with UnitOfWork() as unit:
        repo = CustomerRepository(unit.session)
        service = CustomerService(repo)
        result = service.create_customer(user_id=request.state.user_id, **customer.dict())
        Customer.validate(result.dict())
        unit.commit()
        return Customer(**result.dict())


@router.post(
    "/dialog/",
    responses={
        200: {"model": Dialog, "description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def post_dialog(
    request: Request,
    dialog: NewDialog = Body(None, description=""),
) -> Dialog:
    """When creating a new chat"""

    with UnitOfWork() as unit:
        repo = DialogRepository(unit.session)
        service = DialogService(repo)
        # dialog = DialogBase(**dialog.dict())
        # result = service.create_dialog(**dialog.dict(cls_map=NewDialog))
        result = await service.create_dialog(request.state.user_id, **dialog.dict())
        Dialog.validate(result.dict())
        unit.commit()
        return Dialog(**result.dict())



@router.post(
    "/dialog/{id}/no_answer/",
    responses={
        200: {"description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def post_dialog_id_no_answer(
    requist: Request,
    id: str = Path(description=""),
    value: int = Query(0, description="0,1"),
) -> None:
    """The user can specify in a specific   chat whether or not a response is required."""

    with UnitOfWork() as unit:
        repo = DialogRepository(unit.session)
        service = DialogService(repo)
        service.set_no_reply(id, requist.state.user_id, value)
        unit.commit()


@router.post(
    "/dialog/{id}/reply/",
    responses={
        200: {"description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def post_dialog_id_reply(
    request: Request,
    id: str = Path(description=""),
    # message: str = Query(None, description="A message to send", alias="message"),
    message: str = Body(None, description="A message to send", alias="body"),
) -> None:
    """Send a message."""
    with UnitOfWork() as unit:
        repo = DialogRepository(unit.session)
        service = DialogService(repo)
        service.reply_to_dialog(id, request.state.user_id, message)
        unit.commit()


@router.post(
    "/employee/{org}/",
    responses={
        200: {"model": NewEmployee, "description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def post_employee(
    org: str = Path(description=""),
    new_employee: NewEmployee = Body(None, description=""),
) -> EmployeeRole:
    """Only the owner can 'add an employee' and assign an 'employee role'.
    The owner is automatically established when the system is connected and the company&#39;s email   address is specified when connecting.
    When an employee is added, the owner copies the link and sends it to the email of the employee who needs to be added.
    After clicking on the link, the employee registers in the system to gain access."""

    with UnitOfWork() as unit:
        repo = EmployeeRepository(unit.session)
        service = EmployeeService(repo)
        result = service.create_employee(organization_id=org, **new_employee.dict())
        EmployeeRole.validate(result.dict(cls_map=EmployeeRole))
        unit.commit()
        return EmployeeRole(**result.dict(cls_map=EmployeeRole))


@router.post(
    "/employee/CreateNewEmployee",
    responses={
        200: {"model": str, "description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def post_employee_create_new_employee(
    email: str = Query(None, description="An email for registration", alias="email"),
) -> str:
    ...


@router.post(
    "/interactive_msg/",
    responses={
        200: {"model": InteractiveMsg, "description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def post_interactive_msg(
    interactive_msg: InteractiveMsg = Body(None, description=""),
) -> InteractiveMsg:
    """The user can \&quot;create\&quot; an actionable message,   enter the name of the template, select the type   of template title, fill in the text, and optionally the footer."""
    return BaseDefaultApi.subclasses[0]().post_interactive_msg(interactive_msg)


@router.post(
    "/newsletter/",
    responses={
        200: {"model": Newsletter, "description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def post_newsletter(
    new_newsletter: NewNewsletter = Body(None, description=""),
) -> Newsletter:
    """The user can send messages via WABA, WhatsApp (Unofficial integration),  Telegram, Telegram Bot. Access to the \&quot;Campaigns\&quot; section is available   only to users with \&quot;administrator\&quot;, \&quot;owner\&quot; rights and those employees    who have these access rights in the \&quot;Settings\&quot; - \&quot;Employees\&quot; section Important:    When sending messages through the unofficial integration of WhatsApp and Telegram,   be careful, as the number may be blocked. Refunds for the subscription, in case of   blocking (banning) of the number, are not carried out. We recommend that you familiarize   yourself with the recommendations for mailings so as not to get banned:   Recommendation for WhatsApp Recommendation for Telegram."""
    return BaseDefaultApi.subclasses[0]().post_newsletter(new_newsletter)


@router.post(
    "/Newsletter/{ID}/cancel/",
    responses={
        200: {"model": Newsletter, "description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def post_newsletter_id_cancel(
    ID: str = Path(description="ID of the newsletter to cancel."),
) -> Newsletter:
    """Unsubscribe."""
    return BaseDefaultApi.subclasses[0]().post_newsletter_id_cancel(ID)


@router.post(
    "/notification",
    responses={
        200: {"model": Notification, "description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def post_notification(
    notification: Notification = Body(None, description=""),
) -> Notification:
    ...


@router.post(
    "/order/",
    responses={
        200: {"model": Order, "description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def post_order(
    order: Order = Body(None, description=""),
) -> Order:
    with UnitOfWork() as unit:
        repo = OrderRepository(unit.session)
        service = OrderService(repo)
        result = service.create_order(**order.dict())
        Order.validate(result.dict())
        unit.commit()
        return Order(**result.dict())


@router.post(
    "/order/{id}/payment",
    responses={
        200: {"model": str, "description": "OK"},
    },
    tags=["default"],
    summary="Generate a link for payment",
    response_model_by_alias=True,
)
async def post_order_payment_link(
    request: Request,
    id: str = Path(description=""),
    payload: Order = Body(None, description=""),
) -> Order:
    # TODO pass Termial and return URL, but at first we need to implement the adding of terminal configuration(Terminal)

    with UnitOfWork() as unit:
        repo = OrderRepository(unit.session)
        service = OrderService(repo)
        order = service.create_payment(id, request.state.user_id, **payload.dict())
        Order.validate(order.dict())
        unit.commit()
        return order.dict()

    #https://my.click.uz/services/pay?service_id={service_id}&merchant_id={merchant_id}&amount={amount}&transaction_param={transaction_param}&return_url={return_url}&card_type={card_type}

@router.post(
    "/product",
    responses={
        200: {"model": NewProduct, "description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def post_product(
    new_product: NewProduct = Body(None, description=""),
) -> NewProduct:
    with UnitOfWork() as unit:
        repo = ProductsRepository(unit.session)
        service = ProductsService(repo)
        result = service.create_product(**new_product.dict())
        unit.commit()
        return NewProduct(**result.dict(cls_map=NewProduct))


@router.post(
    "/role/",
    responses={
        200: {"model": Role, "description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def post_role(
    role: Role = Body(None, description=""),
) -> Role:
    with UnitOfWork() as unit:
        repo = RoleRepository(unit.session)
        service = RoleService(repo)
        result = service.create_role(**role.dict())
        Role.validate(result.dict())
        unit.commit()
        return Role(**result.dict())


@router.post(
    "/shop",
    responses={
        200: {"model": Shop, "description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def post_shop(
    shop: Shop = Body(None, description=""),
) -> Shop:
    ...


@router.post(
    "/{org_id}/subscription/pay/",
    responses={
        200: {"model": str, "description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def post_subscription_pay(
    request: Request,
    org_id: str = Path(description="Organization ID"),
    subscriptions: PaySubscriptions = Body(None, description=""),
) -> Invoice:
    """Pay subscription"""
    with UnitOfWork() as unit:
        repo = SubscriptionRepository(unit.session)
        service = SubscriptionService(repo)
        result = service.pay_subscription(org_id, request.state.user_id, **subscriptions.dict())
        Invoice.validate(result.dict())
        unit.commit()
        return result.dict()


@router.post(
    "/tag",
    responses={
        200: {"model": Tag, "description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def post_tag(
    tag: Tag = Body(None, description=""),
) -> Tag:
    ...


@router.post(
    "/template/",
    responses={
        200: {"model": Template, "description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def post_template(
    template: Template = Body(None, description=""),
) -> Template:
    """A user can 'Create' a template by adding a template title and its text.
    There is also  an option to insert an image/video/emoticon."""

    with UnitOfWork() as unit:
        repo = TemplateRepository(unit.session)
        service = TemplateService(repo)
        template = service.create_template(**template.dict())
        Template.validate(template.dict())
        unit.commit()
        return Template(**template.dict())


@router.post(
    "/user",
    responses={
        200: {"model": User, "description": "User Created"},
        400: {"description": "Missing Required Information"},
        409: {"description": "Email Already Taken"},
    },
    tags=["default"],
    summary="Create New User",
    response_model_by_alias=True,
)
async def post_user(
    post_user_request: PostUserRequest = Body(None, description="Post the necessary fields for the API to create a new user."),
) -> User:
    """Create a new user."""
    return BaseDefaultApi.subclasses[0]().post_user(post_user_request)


@router.put(
    "/{org_id}/terminal/",
    responses={
        200: {"model": Setting, "description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def put_terminal(
    request: Request,
    org_id: str = Path(description=""),
    setting: Terminal = Body(None, description=""),
) -> Terminal:
    with UnitOfWork() as unit:
        repo = TerminalRepository(unit.session)
        service = TerminalService(repo)
        result = service.update_terminal(setting.id, org_id, request.state.user_id, **setting.dict())
        Terminal.validate(result.dict())
        unit.commit()
        return result.dict()


@router.put(
    "/catalog/",
    responses={
        200: {"model": NewCatalog, "description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def put_catalog(
    new_catalog: NewCatalog = Body(None, description=""),
) -> NewCatalog:
    """The user can Edit an already created catalog,
    change the Name, Add or vice versa Remove the product."""

    with UnitOfWork() as unit:
        repo = CatalogRepository(unit.session)
        service = CatalogService(repo)
        result = service.update_catalog(id_=new_catalog.id, **new_catalog.dict())
        new_catalog = NewCatalog(**result.dict(NewCatalog))
        unit.commit()
        return new_catalog



@router.put(
    "/client/",
    responses={
        200: {"model": Customer, "description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def put_customer(
    request: Request,
    customer: Customer = Body(None, description=""),
) -> Customer:
    """The user can make changes to an already created
    contact: change the first and last name, add a tag, add a note, add a phone number, add an e-mail."""

    with UnitOfWork() as unit:
        repo = CustomerRepository(unit.session)
        service = CustomerService(repo)
        result = service.update_customer(customer.id, request.state.user_id, **customer.dict())
        Customer.validate(result.dict())
        unit.commit()
        return Customer(**result.dict())


@router.put(
    "/{org_id}/connection/",
    responses={
        200: {"model": NewConnection, "description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def put_connection(
    request: Request,
    org_id: str = Path(description="Organization ID"),
    new_connection: NewConnection = Body(None, description=""),
) -> NewConnection:
    """The user can make changes to the \&quot;Edit\&quot; connection   channel and change the \&quot;Connection Name\&quot;."""
    with UnitOfWork() as unit:
        repo = ConnectionRepository(unit.session)
        service = ConnectionService(repo)
        entity = service.update_connection(new_connection.id, org_id, request.state.user_id, **new_connection.dict())
        d = entity.dict(cls_map=NewConnection)
        NewConnection.validate(d)
        unit.commit()
        return NewConnection(**entity.dict(cls_map=NewConnection))



@router.put(
    "/employee/",
    responses={
        200: {"model": List[EmployeeRole], "description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def put_employee(
    employee_role: EmployeeRole = Body(None, description=""),
) -> EmployeeRole:
    """The user can make changes to the 'Edit' employee and change the 'Employee role',
    as well as grant or restrict 'Access rights'."""
    with UnitOfWork() as unit:
        repo = EmployeeRepository(unit.session)
        service = EmployeeService(repo)
        employee_role = service.update_employee(employee_role.id, **employee_role.dict())
        EmployeeRole.validate(employee_role.dict(cls_map=EmployeeRole))
        unit.commit()
        return EmployeeRole(**employee_role.dict(cls_map=EmployeeRole))



@router.put(
    "/interactive_msg/",
    responses={
        200: {"model": InteractiveMsg, "description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def put_interactive_msg(
    interactive_msg: InteractiveMsg = Body(None, description=""),
) -> InteractiveMsg:
    """The user can \&quot;edit\&quot; an interactive message   by making changes to the text, image,   video, document, header, footer, button."""
    return BaseDefaultApi.subclasses[0]().put_interactive_msg(interactive_msg)


@router.put(
    "/newsletter/",
    responses={
        200: {"model": Newsletter, "description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def put_newsletter(
    new_newsletter: NewNewsletter = Body(None, description=""),
) -> Newsletter:
    """In case the mailing has not yet been sent and   has the status \&quot;scheduled\&quot;, then we can update the   text and the list of clients and change the time of sending."""
    return BaseDefaultApi.subclasses[0]().put_newsletter(new_newsletter)


@router.put(
    "/notification",
    responses={
        200: {"model": Notification, "description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def put_notification(
    notification: Notification = Body(None, description=""),
) -> Notification:
    ...


@router.put(
    "/product",
    responses={
        200: {"model": NewProduct, "description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def put_product(
    new_product: NewProduct = Body(None, description=""),
) -> NewProduct:
    with UnitOfWork() as unit:
        repo = ProductsRepository(unit.session)
        service = ProductsService(repo)
        result = service.update_product(new_product.id, **new_product.dict())
        unit.commit()
        return NewProduct(**result.dict(cls_map=NewProduct))


@router.put(
    "/role/",
    responses={
        200: {"model": Role, "description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def put_role(
    role: Role = Body(None, description=""),
) -> Role:
    with UnitOfWork() as unit:
        repo = RoleRepository(unit.session)
        service = RoleService(repo)
        result = service.update_role(role.id, **role.dict())
        Role.validate(result.dict())
        unit.commit()
        return Role(**result.dict())


@router.put(
    "/setting",
    responses={
        200: {"model": Setting, "description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def put_setting(
    setting: Setting = Body(None, description=""),
) -> Setting:
    ...


@router.put(
    "/shop",
    responses={
        200: {"model": Shop, "description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def put_shop(
    shop: Shop = Body(None, description=""),
) -> Shop:
    ...


@router.put(
    "/{org_id}/subscription/",
    responses={
        200: {"model": object, "description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def put_subscription(
    request: Request,
    org_id: str = Path(description="Organization ID"),
    body: List[Subscription] = Body(None, description=""),
) -> object:
    """Update only 'included_subscribe'"""
    with UnitOfWork() as unit:
        repo = SubscriptionRepository(unit.session)
        service = SubscriptionService(repo)
        results = service.update_subscriptions(org_id, request.state.user_id, body)
        unit.commit()
        return results


@router.put(
    "/tag",
    responses={
        200: {"model": Tag, "description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def put_tag(
    tag: Tag = Body(None, description=""),
) -> Tag:
    ...


@router.put(
    "/template/",
    responses={
        200: {"model": Template, "description": "OK"},
    },
    tags=["default"],
    summary="",
    response_model_by_alias=True,
)
async def put_template(
    template: Template = Body(None, description=""),
) -> Template:
    """The user can 'Edit' the template by changing the title and text (along with the content of the text)."""

    with UnitOfWork() as unit:
        repo = TemplateRepository(unit.session)
        service = TemplateService(repo)
        result = service.update_template(template.id, **template.dict())
        Template.validate(result.dict())
        unit.commit()
        return Template(**result.dict())

