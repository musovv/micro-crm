from abc import ABC

from crm.business_service.bases import TemplateBase
from crm.repository.models import TemplateModel, EmployeeModel
from crm.repository.repository import Repository


class TemplateRepository:
    pass


class TemplateRepository(Repository, ABC):
    def __init__(self, session):
        self.session = session

    def add(self, **payload: dict) -> TemplateBase:
        template = TemplateModel(**payload)

        owner = (self.session.query(EmployeeModel)
                 .filter(EmployeeModel.id == template.owner_id).first())
        if not owner:
            raise ValueError('Owner not found')

        self.session.add(template)
        return TemplateBase(**template.dict(), template_=template)

    def list(self, limit=None, **filters):
        if limit:
            templates = self.session.query(TemplateModel).limit(limit).all()
        else:
            templates = self.session.query(TemplateModel).all()
        return [TemplateBase(**template.dict()) for template in templates]

    def get(self, template_id) -> TemplateBase:
        template = self.session.query(TemplateModel).filter(TemplateModel.id == template_id).first()
        if not template:
            raise ValueError('Template not found')
        return TemplateBase(**template.dict())

    def update(self, template_id, **payload: dict):
        template = self.session.query(TemplateModel).filter(TemplateModel.id == template_id).first()
        if not template:
            raise ValueError('Template not found')
        (self.session.query(TemplateModel).filter(TemplateModel.id == template_id)
         .update(payload))
        return TemplateBase(**payload)

    def delete(self, template_id):
        template = self.session.query(TemplateModel).filter(TemplateModel.id == template_id).first()
        if not template:
            raise ValueError('Template not found')
        self.session.delete(template)
