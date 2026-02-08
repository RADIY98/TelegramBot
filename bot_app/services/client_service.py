from bot_app.repositories import client_repository


class ClientService:
    def __init__(self, client_rep: client_repository.ClientRepository):
        self.client_rep = client_rep
