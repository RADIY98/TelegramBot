from typing import Optional, List, Dict

from . import sql_query
from ...domain.entities.user_entity import UserEntity
from ...domain.repositories.user_repositoriy import IUserRepository


class PostgresClientRepository(IUserRepository):

    def __init__(self, connection):
        self.connection = connection

    def get_user_info(self, user_id: int) -> UserEntity:
        pass

    def create_user(self, user_id: int) -> None:
        pass