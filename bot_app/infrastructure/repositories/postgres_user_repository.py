from typing import Optional, List, Dict

from . import sql_query
from ...domain.repositories.user_repositoriy import UserRepository


class PostgresClientRepository(UserRepository):

    def __init__(self, connection):
        self.connection = connection

    def create_user(self, user_id: int) -> None:
        pass