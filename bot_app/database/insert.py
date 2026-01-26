
"""
Модуль для вставки записей в БД
"""
from ..database import sql_query

from bot_app import base_names
from bot_app.database import sql_query
from bot_app.schemas.Response import Msg


def insert_client(msg: Msg, update_id: int) -> None:
    """
    Добавляем клиента в БД
    """
    sql_query(
        """
                    INSERT INTO
                        "Client"
                    VALUES 
                        (
                            %s::bigint,
                            %s::text,
                            %s::text,
                            %s::bigint
                        )
                    """,
        (msg.chat.id, msg.chat.first_name, msg.chat.username, update_id)
    )


def insert_train(client_id: int, train_name: str) -> None:
    """
    Добавить тренировку
    """
    sql_query(
    """
        INSERT INTO
            "Train"
            (
            "Name",
            "ClientID"
            )
        VALUES 
        (
            %s::text,
            %s::int
        )
        """, (train_name, client_id)
    )
