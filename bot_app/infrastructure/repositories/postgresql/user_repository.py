from . import sql_query_record
from bot_app.domain.entities.user_entity import UserEntity
from bot_app.domain.repositories.user_repositoriy import IUserRepository


class PostgresClientRepository(IUserRepository):

    def __init__(self, connection):
        self.connection = connection

    @staticmethod
    def get_user_info(user_id: int) -> UserEntity:
        """Get client info"""
        data: dict = sql_query_record(
            """
                SELECT
                    user_id,
                    update_id,
                    first_name,
                    user_name
                FROM
                    "User"
                WHERE
                    %s::bigint
            """,
            [user_id]
        )

        return UserEntity(
            user_id=data.get("user_id"),
            update_id=data.get("update_id"),
            first_name=data.get("first_name"),
            user_name=data.get("user_name")
        )


    @staticmethod
    def create_user(user_id: int, first_name: str, username: str, update_id: int) -> None:
        """Create a new user"""
        sql_query_record(
            """
                INSERT INTO
                    "User"
                VALUES 
                    (
                        %s::bigint,
                        %s::text,
                        %s::text,
                        %s::bigint
                    )
            """,
            (user_id, first_name, username, update_id)
        )

    @staticmethod
    def change_update_id(user_id: int, update_id: int) -> None:
        """Change UpdateId of User"""
        sql_query_record(
            """
                UPDATE
                    "User"
                SET
                    "UpdateId"=%s::bigint
                WHERE
                    "ClientId"=%s::bigint
            """, (update_id, user_id)
        )
