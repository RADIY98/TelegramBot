from ..database import sql_query

class Client:
    def __init__(self, client_id: int):
        self.client_id = client_id
