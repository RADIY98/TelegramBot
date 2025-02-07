"""
Модуль для обновления данных
"""
from typing import List

from bot_app.database import sql_query


def update_client_last_update(client_id: int, update_id: int) -> List[dict]:
    """
    Обновляем данные о последнем обновление для клиента
    """
    res = sql_query(
        """
        UPDATE
            "Client"
        SET
            "UpdateId"=%s::bigint
        WHERE
            "id"=%s::bigint
        RETURNING
            "id",
            "UpdateId"

        """, (update_id, client_id)
    )
    return res
