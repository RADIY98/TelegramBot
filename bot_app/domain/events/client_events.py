
class ClientEventStatusChange:
    def __init__(self, client_rep, client_status: int, client_id: int):
        self.client_status = client_status
        self.client_id = client_id
        self.client_rep = client_rep

    def handle(self):
        self.client_rep.update_status(self.client_id, self.client_status)


class ClientEventSelectedEntityChange:
    def __init__(self, client_rep, selected_id: str, client_id: int):
        self.selected_id = selected_id
        self.client_id = client_id
        self.client_rep = client_rep

    def handle(self):
        self.client_rep.update_selected_entity(self.client_id, self.selected_id)