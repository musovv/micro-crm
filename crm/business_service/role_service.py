from crm.business_service.bases import RoleBase


class RoleService:
    def __init__(self, role_repository):
        self.role_repository = role_repository

    def list_roles(self, **filters) -> list[RoleBase]:
        # limit = filters.pop('limit', None)
        return self.role_repository.list(**filters)

    def get_role_by_id(self, role_id):
        return self.role_repository.get(role_id)

    def create_role(self, **payload) -> RoleBase:
        role = RoleBase(**payload)
        role = self.role_repository.add(**role.dict())
        return RoleBase(**role.dict(), role_=role)

    def update_role(self, id_,  **payload) -> RoleBase:
        role = RoleBase(**payload)
        role = self.role_repository.update(id_, **role.dict())
        return RoleBase(**role.dict())

    def delete_role(self, role_id):
        return self.role_repository.delete(role_id)

