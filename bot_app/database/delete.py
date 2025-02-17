"""
модуль для удаления данных
"""
from bot_app.database import sql_query


def delete_all_trains(client_id: int) -> None:
    """
    Удаляем все тренировки
    """
    sql_query("""
                DELETE FROM
                    "Train"
                WHERE
                    "ClientID"=%s::bigint
                """, [client_id]
    )

def delete_train(train_name: str) -> None:
    """
    Удаление тренировки
    """
    sql_query(
        """
            DELETE FROM
                "Train"
            WHERE
                "Name"=%s::text
        """, [train_name]
    )

def delete_exercise(client_id: int) -> None:
    """
    Удаление упражнения
    """
    sql_query(
        """
        DELETE FROM
            "Exercise"
        WHERE
            "id"=(SELECT "SelectedEntity" FROM "Client" WHERE "id"=%s)
        """, client_id
    )