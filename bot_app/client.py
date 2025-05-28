"""
Модуль для работы с объектом клиента
"""
from .database import select

class Client:
    """
    Класс клиента
    """
    def __init__(self, client_id: int):
        """
        Инициализация объекта
        """
        self.client_id = client_id
        self.update_id = None
        self.trains = None
        self.status = None
        self.selected_entity = None
        self.get_client_info()

    def get_client_info(self):
        """
        Получить информацию по клиенту
        """
        client_info = select.get_client_data(self.client_id)
        self.update_id = client_info['UpdateId']
        self.trains = client_info['Trains'] if client_info['Trains'] else []
        self.status = client_info['Status']
        self.selected_entity = client_info['SelectedEntity']
