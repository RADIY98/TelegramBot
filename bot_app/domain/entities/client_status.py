from typing import Optional

class ClientStatus:
    def __init__(self):
        self.client_status: int = 0

    def set_status(self, status: Optional[int]):
        self.client_status = status

    def get_status(self):
        return self.client_status