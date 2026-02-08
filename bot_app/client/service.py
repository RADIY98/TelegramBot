from . import Client

class ClientService:
    def __init__(self, client_obj: Client):
        self.client_obj = client_obj

    def _update_client_stat(self, status: int):
