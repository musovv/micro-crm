from abc import ABC
from datetime import datetime

from crm.business_service.bases import TerminalBase
from crm.repository.models import TerminalTypeModel, TerminalModel, SettingModel
from crm.repository.repository import Repository


class TerminalRepository(Repository, ABC):
    def __init__(self, session):
        self.session = session

    def add(self, org_id, **payload):
        payload.pop('id', None)
        terminal_type = payload.pop('terminal_type', None)
        if terminal_type:
            terminal_type = (self.session.query(TerminalTypeModel)
                             .filter(TerminalTypeModel.code == terminal_type['code']).first())
        if not terminal_type:
            raise ValueError('Terminal type not found')

        terminal = TerminalModel(**payload)
        terminal.date_created = datetime.utcnow()
        terminal.terminal_type = terminal_type
        # find setting:
        setting = (self.session.query(SettingModel).filter(SettingModel.organization_id == org_id).first())
        if not setting:
            raise ValueError('Setting not found')
        terminal.setting = setting
        self.session.add(terminal)
        return TerminalBase(**terminal.dict(), terminal_=terminal)

    def _get(self, id_, org_id):
        terminal = (self.session.query(TerminalModel)
                    .join(TerminalModel.setting)
                    .filter(TerminalModel.id == id_, SettingModel.organization_id == org_id).first())
        if not terminal:
            raise ValueError('Terminal not found')
        return terminal

    def get(self, id_, org_id, user_id):
        pass  # is not used

    def list(self, org_id, user_id, limit=None, **filters):
        query = (self.session.query(TerminalModel).join(TerminalModel.setting)
                 .filter(SettingModel.organization_id == org_id))
        if filters:
            query = query.filter_by(**filters)
        if limit:
            query = query.limit(limit)
        terminals = query.all()

        return [TerminalBase(**terminal.dict()) for terminal in terminals]

    def update(self, id_, org_id, user_id, **payload):
        terminal = self._get(id_, org_id)
        payload.pop('id', None)
        payload.pop('terminal_type', None)
        for key, value in payload.items():
            setattr(terminal, key, value)

        return TerminalBase(**terminal.dict())

    def delete(self, id, org_id, user_id):
        self._get(id, org_id)