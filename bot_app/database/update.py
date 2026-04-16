"""
Модуль для обновления данных
"""
from typing import List, Optional

from ..database import sql_query


def update_selected_entity_by_id(client_id: int, concrete_id: int):
    """
    Обновляем выбранный ИД
    """
    sql_query(
        """
        UPDATE 
            "User"
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
            "User"
        SET
            "SelectedEntity"=NULL
        WHERE
            "id"={client_id}::bigint
        """
    )
