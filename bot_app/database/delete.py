"""
модуль для удаления данных
"""
from ..database import sql_query


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
