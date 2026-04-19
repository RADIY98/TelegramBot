from bot_app.infrastructure.repositories import postgres_user_repository


class ClientService:
    def __init__(self, client_rep: client_repository.ClientRepository):
        self.client_rep = client_rep
