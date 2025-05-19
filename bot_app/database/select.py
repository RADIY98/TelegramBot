from typing import List, Dict, Optional

from bot_app import base_names
from bot_app.database import sql_query, sql_query_scalar, sql_query_record


def get_client_selected_entity(client_id: int) -> int:
    """
    Получим ид сущности которой будем делать изменения
    """
    result = sql_query_scalar(
        f"""
        SELECT
            "SelectedEntity"
        FROM
            "Client"
        WHERE
            "id"=%(client)s::bigint
        """, {"client": client_id}
    )
    return result

def exercise_by_train(client_id: int) -> List[str]:
    """
    Получить все упражнения по тренировки
    """
    result = sql_query_scalar(
        """
            SELECT
                array_agg("Name")
            FROM
                "Exercise"
            WHERE
                "TrainId"=(SELECT "SelectedEntity" FROM "Client" WHERE "id"=%s::bigint)
            GROUP BY
                "TrainId"
        """, [client_id]
    )
    return result

def get_all_trains_for_keyboard(client_id) -> list:
    """
    Получить тренировку
    """
    result = sql_query_scalar(
        """
            SELECT
                array_agg("Name")
            FROM
                "Train"
            WHERE
                "ClientID"=%s::bigint
            GROUP BY
                "ClientID"
        """, [client_id]
    )

    return result if result else []


def all_exercise_for_keyboard(train_id: int):
    sql = """
            SELECT
                array_agg("Name")
            FROM
                "Exercise"
            WHERE
                "TrainId"=%s::bigint
        """
    result = sql_query_scalar(sql, [train_id])
    if not result:
        result = ["Давайте добавим упражнения"]
    result.append(base_names.MAIN_MENU)
    return result

def get_all_exercises_for_keyboard(train_id: int) -> str:
    """
    Получить тренировку
    """
    result = sql_query_scalar(
        """
            SELECT
                "Settings"
            FROM
                "Exercise"
            WHERE
                "TrainId"=%s::bigint
        """, [train_id]
    )
    msg = ""
    for ex_name, ex_value in result.items():
        if len(list(filter(None, ex_value))) > 1:
            msg += f"{ex_name}: \n Веса - {','.join(i for i in ex_value[0])} \n Количество подходов - {','.join(i for i in ex_value[1])}\n\n"
        else:
            msg += f"{ex_name}: \nКоличество подходов - {','.join(i for i in ex_value[0])}\n\n"

    return msg

def is_exercise(exercise_name: str) -> bool:
    """
    Метод определяет выбрана тренировка или нет
    """
    result = sql_query_scalar(
        """
            SELECT
                1
            FROM
                "Exercise"
            WHERE
                "Name"=%s::text
        """, [exercise_name]
    )
    print(result)
    return result


def read_exercise(exercise_id: int) -> dict:
    """
    Прочитаем упражнение
    """
    result = sql_query_record(
        """
        SELECT
            *
        FROM 
            "Exercise"
        WHERE
            "id" = %s::bigint
            """, [exercise_id]
    )
    return result

def read_train(client_id: int, train_id: int) -> dict:
    """
    Прочитать тренировку
    """
    result = sql_query_record(
        """        
        SELECT
            *
        FROM 
            "Train"
        WHERE
            "id" = %s::bigint AND
            "ClientID"=%s::bigint
            """, [train_id, client_id]
    )
    return result

def get_client_data(client_id: int) -> dict:
    """
    Получить разом информацию по клиенту
    """
    result = sql_query_record(
        """
        WITH trains AS (
            SELECT
                array_agg("Name")
            FROM
                "Train"
            WHERE 
                "ClientID"=%s::bigint
            GROUP BY
                "ClientID"
        )
        SELECT
            "id"::bigint,
            "UpdateId"::bigint,
            "Status"::int,
            "SelectedEntity"::bigint,
            (SELECT * FROM trains) "Trains"
        FROM
            "Client"
        WHERE
            "id" = %s::bigint
        """, [client_id, client_id]
    )
    return result
