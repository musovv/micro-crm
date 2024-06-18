from abc import ABC

from crm.business_service.bases import RoleBase
from crm.repository.models import RoleModel, PermissionModel, TypeResourceModel
from crm.repository.repository import Repository


class RoleRepository(Repository, ABC):
    def __init__(self, session):
        self.session = session

    def add(self, **payload: dict) -> RoleBase:

        payload.pop('permissions', [])
        role = RoleModel(**payload)
        # add default permissions to role
        ## Clients:
        dialog_type = self.session.query(TypeResourceModel).filter(TypeResourceModel.code == 'dialog').first()
        if not dialog_type:
            raise ValueError('Dialog type not found')
        # 1
        role.permissions.append(PermissionModel(name='Просмотр всех чатов', description='Просмотр всех чатов',
                               type_resource=dialog_type, access=0,
                               privilege='read', access_level='organization'))
        # 2
        role.permissions.append(PermissionModel(name='Просмотр собственных чатов', description='Просмотр собственных чатов',
                               type_resource=dialog_type, access=0,
                               privilege='read', access_level='user'))
        # 3
        role.permissions.append(PermissionModel(name='Создание', description='Создание чатов',
                               type_resource=dialog_type, access=0,
                               privilege='create', access_level='organization'))
        # 4
        role.permissions.append(PermissionModel(name='Удаление', description='Удаление чатов',
                               type_resource=dialog_type, access=0,
                               privilege='delete', access_level='organization'))

        ## Setting:
        setting_type = self.session.query(TypeResourceModel).filter(TypeResourceModel.code == 'setting').first()
        if not setting_type:
            raise ValueError('Setting type not found')
        # 5
        role.permissions.append(PermissionModel(name='Просмотр', description='Просмотр настроек',
                               type_resource=setting_type, access=0,
                               privilege='read', access_level='organization'))
        # 6
        role.permissions.append(PermissionModel(name='Изменение', description='Изменение настроек',
                               type_resource=setting_type, access=0,
                               privilege='write', access_level='organization'))


        self.session.add(role)
        return RoleBase(**role.dict(), role_=role)

    def get(self, id_) -> RoleBase:
        role = self._get(id_)
        return RoleBase(**role.dict())

    def _get(self, id_) -> RoleModel:
        if not id_:
            raise ValueError('Role id is not provided')
        role = self.session.query(RoleModel).filter(RoleModel.id == str(id_)).first()
        if not role:
            raise ValueError('Role not found')
        return role

    def list(self, limit=None, **filters) -> list[RoleBase]:
        query = self.session.query(RoleModel)
        if limit:
            query = query.limit(limit)
        return [RoleBase(**role.dict()) for role in query.all()]

    def update(self, id_, **payload) -> RoleBase:
        role = self._get(id_)
        # role.permissions = []

        # update access for permissions
        for perm in payload.pop('permissions', []):
            self.session.query(PermissionModel).filter(PermissionModel.id == perm['id']).update({'access': perm['access']})
            # permission = self.session.query(PermissionModel).filter(PermissionModel.id == perm['id']).first()
            # if permission:
            #     permission.access = perm['access']
            #     role.permissions.append(permission)
            # else:
            #     raise ValueError('Permission not found')

        for key, value in payload.items():
            setattr(role, key, value)

        return RoleBase(**role.dict())

    def delete(self, id_):
        role = self._get(id_)
        self.session.delete(role)