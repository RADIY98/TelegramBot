"""
Модуль для обновления данных
"""
from typing import List, Optional

from ..database import sql_query


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



def update_selected_entity_by_id(client_id: int, concrete_id: int):
    """
    Обновляем выбранный ИД
    """
    sql_query(
        """
        UPDATE 
            "Client"
        SET
            "SelectedEntity"=%s::int
        WHERE
            "id"=%s::bigint
            """, [concrete_id, client_id]
    )

def drop_selected_entity(client_id: int) -> None:
    """
    Сбросим ид выбранной сущности, так как мы вышли в главное меню
    """
    sql_query(
        f"""
        UPDATE
            "Client"
        SET
            "SelectedEntity"=NULL
        WHERE
            "id"={client_id}::bigint
        """
    )
