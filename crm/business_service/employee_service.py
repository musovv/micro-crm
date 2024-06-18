from crm.business_service.base import EntityBase
from crm.business_service.bases import EmployeeBase
from crm.repository.employee_repository import EmployeeRepository
from crm.repository.models import EmployeeModel


class EmployeeService:
    def __init__(self, employee_repository: EmployeeRepository):
        self.employee_repository = employee_repository

    def get_employee(self, employee_id) -> EmployeeBase|EntityBase:
        return self.employee_repository.get(employee_id)

    def get_all_employees(self, **filters):
        return self.employee_repository.list(**filters)

    def create_employee(self, **payload):
        employee = EmployeeBase(**payload)
        employee = self.employee_repository.add(**employee.dict(cls_map=EmployeeModel))
        return employee

    def update_employee(self, employee_id, **payload):
        return self.employee_repository.update(employee_id, **payload)

    def delete_employee(self, employee_id):
        self.employee_repository.delete(employee_id)