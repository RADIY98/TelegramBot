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

def update_client_status(client_id: int, client_status: int|None) -> None:
    """
    Обновляем клиентский статус
    """
    sql_query(
        """
        UPDATE
            "Client"
        SET
            "Status"=%s::bigint
        WHERE
            "id"=%s::bigint
        """, (client_status, client_id)
    )

def update_client_selected_entity(client_id: int, msg: str|None) -> None:
    """
    Обновлем ид выбранной сущности
    """
    sql_query(
        """
        WITH determine_selected_entity AS (
            SELECT
                "id"
            FROM 
                "Train"
            WHERE
                "Name"=%s::text
            UNION
            SELECT
                "id"
            FROM
                "Exercise"
            WHERE
                "Name"=%s::text
        )
        UPDATE
            "Client"
        SET
            "SelectedEntity"=(SELECT * FROM "determine_selected_entity" LIMIT 1)
        WHERE
            "id"=%s::bigint
        """, (msg, msg, client_id)
    )

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

def update_train(client_id: int, train_name: str) -> None:
    """
    Обновим название тренировки
    """
    sql_query(f"""
        UPDATE
            "Train"
        SET
            "Name"=%s::text
        WHERE
            "id" = (SELECT "SelectedEntity" FROM "Client" WHERE "id"=%s::int)
    """, (train_name, client_id)
    )

def rename_exercise(exercise_name: str, selected_entity: int) -> None:
    """
    Переименовываем упражнения
    """
    sql_query(
        """
        UPDATE
            "Exercise"
        SET
            "Name"=%s::text
        WHERE
            "id"=%s::int
        """, [exercise_name, selected_entity]
    )