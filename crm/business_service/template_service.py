from typing import List

from crm.business_service.base import EntityBase
from crm.business_service.bases import TemplateBase
from crm.repository.template_repository import TemplateRepository


class TemplateService:
    def __init__(self, template_repository: TemplateRepository):
        self.template_repository = template_repository

    def create_template(self, **payload: dict) -> TemplateBase:
        template = TemplateBase(**payload)
        template = self.template_repository.add(**template.dict())
        return template

    def delete_template(self, template_id):
        self.template_repository.delete(template_id)

    def get_template(self, template_id) -> TemplateBase:
        return self.template_repository.get(template_id)

    def list_templates(self, **filters) -> List[TemplateBase|EntityBase]:
        limit = filters.pop('limit', None)
        return self.template_repository.list(limit, **filters)

    def update_template(self, template_id, **payload: dict) -> TemplateBase|EntityBase:
        template = self.template_repository.update(template_id, **payload)
        return template
