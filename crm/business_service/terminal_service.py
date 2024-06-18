from crm.repository.terminal_repository import TerminalRepository


class TerminalService:
    def __init__(self, terminal_repository: TerminalRepository):
        self.terminal_repository = terminal_repository

    def create_terminal(self, org_id, **payload):
        # FIXME avoid creating a duplicate terminal with the same code
        return self.terminal_repository.add(org_id, **payload)

    def get(self, id_, user_id_):
        return self.terminal_repository.get(id_, user_id_)

    def list_terminal(self, org_id, user_id, limit=None, **filters):
        return self.terminal_repository.list(org_id, user_id, limit, **filters)

    def update_terminal(self, id_, org_id, user_id, **payload):
        return self.terminal_repository.update(id_, org_id, user_id, **payload)

    def delete_terminal(self, id_, org_id, user_id):
        return self.terminal_repository.delete(id_, org_id, user_id)