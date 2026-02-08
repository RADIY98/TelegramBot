from bot_app.domain.events import client_events
from bot_app.repositories.client_repository import ClientRepository


class UpdateClientStatus:
    def __init__(self, client_rep: ClientRepository):
        self.client_rep = client_rep

    def handle(self, event: client_events.ClientEventStatusChange):
        self.client_rep.update_status(event.client_id, event.client_status)


class UpdateClientSelectedEntity:
    def __init__(self, client_rep: ClientRepository):
        self.client_rep = client_rep

    def handle(self, event: client_events.ClientEventSelectedEntityChange):
        self.client_rep.update_selected_entity(event.client_id, event.selected_id)
