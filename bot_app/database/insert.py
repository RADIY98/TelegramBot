
"""
Модуль для вставки записей в БД
"""
import json

from bot_app.database import sql_query
from bot_app.schemas.Response import Msg


def insert_client(msg: Msg, update_id: int) -> None:
    """
    Добавляем клиента в БД
    """
    sql_query(
        f"""
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

def  insert_train(train_name: str, client_id: int, train: dict) -> None:
    sql_query(
    """
        INSERT INTO
            "Train"
            (
            "Name",
            "ClientID",
            "Settings"
            )
        VALUES 
        (
            %s::text,
            %s::bigint,
            %s::json
        )
        """, (train_name, client_id, json.dumps(train))
    )
