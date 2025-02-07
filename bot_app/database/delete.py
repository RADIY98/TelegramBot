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