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
    if result:
        result.append(base_names.MAIN_MENU)
    else:
        result = [base_names.MAIN_MENU]
    return result
