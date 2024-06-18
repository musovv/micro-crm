from crm.business_service.base import EntityBase
from crm.business_service.bases import SettingBase
from crm.repository.organization_repository import OrganizationRepository


class OrganizationService:
    def __init__(self, organization_repository: OrganizationRepository):
        self.organization_repository = organization_repository

    def create_organization(self, **payload) -> SettingBase | EntityBase:
        # TODO create admin user for organization
        return self.organization_repository.add(**payload)

    def list_organizations(self, user_id, limit=None, **filters):
        return self.organization_repository.list(user_id, limit, **filters)


