"""
модуль для удаления данных
"""
from ..database import sql_query, sql_query_record


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

def delete_exercise(client_id: int) -> (str, int):
    """
    Удаление упражнения
    """
    exercise = sql_query_record(
        """
        DELETE FROM
            "Exercise"
        WHERE
            "id"=(SELECT "SelectedEntity" FROM "Client" WHERE "id"=%s)
        RETURNING
            "Name",
            "TrainId"
        """, [client_id]
    )
    return exercise.get("Name"), int(exercise.get("TrainId"))
