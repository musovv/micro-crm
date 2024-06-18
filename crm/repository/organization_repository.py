import datetime
from abc import ABC

from crm.business_service.bases import SettingBase
from crm.repository.models import OrganizationModel, SettingModel, NotificationModel, EmployeeModel
from crm.repository.repository import Repository



class OrganizationRepository(Repository, ABC):
    def __init__(self, session):
        self.session = session

    def add(self, **payload):
        payload.pop('id', None)
        payload.pop('organization_id', None)
        notification = payload.pop('notification', None)

        setting = SettingModel(**payload)  # !! we use setting instead of organization as prototype for now

        # At first we need to create organization
        organization = OrganizationModel()
        organization.date_created = datetime.datetime.utcnow()
        organization.setting = setting

        # Add notification if it exists
        if notification:
            notification.pop('id', None)  # to avoid mismatching id when returning the result
            notification = NotificationModel(**notification)
            notification.date_created = datetime.datetime.utcnow()
            if notification.notify_newsletters is None:
                notification.notify_newsletters = False
            if notification.notify_payments is None:
                notification.notify_payments = False
            if notification.notify_trouble_integrations is None:
                notification.notify_trouble_integrations = False

            setting.notification = notification

        self.session.add(setting)

        return SettingBase(**setting.dict(), setting_=setting)

    def list(self, user_id, limit=None, **filters):
        query = (self.session.query(SettingModel).join(SettingModel.organization).join(OrganizationModel.employees)
                 .filter(EmployeeModel.id == user_id))
        if filters:
            query = query.filter_by(**filters)
        if limit:
            orgs = query.limit(limit).all()
        else:
            orgs = query.all()
        # res = (self.session.query(OrganizationModel).join(EmployeeModel.organization_id)
        #         .filter(EmployeeModel.id == user_id).filter_by(**filters)
        #         .limit(limit).all())
        return [SettingBase(**o.dict()) for o in orgs]

    def get(self, organization_id, user_id):
        pass

    def update(self, organization_id, **payload):
        pass

    def delete(self, organization_id, user_id):
        pass
