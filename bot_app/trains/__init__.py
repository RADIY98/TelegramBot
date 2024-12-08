"""
Модуль для CRUD методов тренировок
"""
from bot_app import base_names
from bot_app.database import sql_query_scalar


def get_all_trains_for_keyboard(client_id):
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
    result.append(base_names.MAIN_MENU)
    return result


def get_all_exercises_for_keyboard(client_id, train_name) -> str:
    """
    Получить тренировку
    """
    result = sql_query_scalar(
        """
            SELECT
                "Settings"
            FROM
                "Train"
            WHERE
                "ClientID"=%s::bigint AND
                "Name"=%s
        """, [client_id, train_name]
    )
    msg = ""
    for ex_name, ex_value in result.items():
        if len(list(filter(None, ex_value))) > 1:
            msg += f"{ex_name}: \n Веса - {','.join(i for i in ex_value[0])} \n Количество подходов - {','.join(i for i in ex_value[1])}\n\n"
        else:
            msg += f"{ex_name}: \nКоличество подходов - {','.join(i for i in ex_value[0])}\n\n"

    return msg
