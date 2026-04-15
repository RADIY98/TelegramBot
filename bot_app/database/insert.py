
"""
Модуль для вставки записей в БД
"""
from bot_app.database import sql_query
from bot_app.interface.telegram.request_model import Msg


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