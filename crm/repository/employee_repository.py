import time
from abc import ABC
from datetime import datetime

from crm.business_service.bases import EmployeeBase
from crm.repository.models import EmployeeModel, RoleModel, PermissionModel
from crm.repository.repository import Repository
from crm.repository.role_repository import RoleRepository


class EmployeeRepository(Repository, ABC):
    def __init__(self, session):
        self.session = session

    def list(self, limit=None, **filters):
        if limit:
            employees = self.session.query(EmployeeModel).limit(limit).all()
        else:
            employees = self.session.query(EmployeeModel).all()
        return [EmployeeBase(**employee.dict()) for employee in employees]


    def _get(self, id):
        employee = self.session.query(EmployeeModel).filter(EmployeeModel.id == id).first()
        if not employee:
            raise ValueError('Employee not found')
        return employee

    def get(self, id):
        employee = self._get(id)
        return EmployeeBase(**employee.dict(), employee_=employee)

    def add(self, **payload: dict) -> EmployeeBase:
        employee = EmployeeModel(**payload)
        employee.status = 1  # active
        employee.type_employee = 'manager'  # FIXME:  use lookup from <config> instead of hardcoded value
        employee.date_created = datetime.now()
        self.session.add(employee)

        # add default role
        role = self.session.query(RoleModel).filter(RoleModel.name == 'role for manager').first()
        # FIXME: change approach of filtering roles - use lookup instead of hardcoded name
        if not role:
            raise ValueError('Role not found')
        employee.roles.append(role)

        return EmployeeBase(**employee.dict(), employee_=employee)

    def update(self, employee_id, **payload: dict) -> EmployeeBase:
        roles = payload.pop('roles', [])
        employee = self._get(employee_id)

        # обновление прав доступа
        for r in roles:
            RoleRepository(session=self.session).update(r['id'], **r)

        # update employee properties:
        for key, value in payload.items():
            setattr(employee, key, value)

        return EmployeeBase(**employee.dict(), employee_=employee)

    def delete(self, id):
        employee = self._get(id)
        self.session.delete(employee)
