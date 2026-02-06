from . import *


class TrainCRUDRepository:

    @staticmethod
    def add(client_id: int, train_name: str) -> None:
        """
        Добавить тренировку
        """
        sql_query(
            """
            INSERT INTO 
                "Train"
            (
                "Name",
                "ClientID"
            )
            VALUES
            (
                %s::text,
                %s::int
            )
            """, (train_name, client_id)
        )

    @staticmethod
    def delete(train_name: str) -> None:
        """
        Удаление тренировки
        """
        sql_query(
            """
            DELETE FROM
                "Train"
            WHERE
                "Name" = %s::text
            """, [train_name]
        )

    @staticmethod
    def read(client_id: int, train_id: int) -> dict:
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

    @staticmethod
    def rename(client_id: int, train_name: str) -> None:
        """
        Обновим название тренировки
        """
        sql_query("""
            UPDATE
              "Train"
            SET
                "Name"=%s::text
            WHERE
                "id" = (SELECT "SelectedEntity" FROM "Client" WHERE "id"=%s:: int)
            """, (train_name, client_id)
        )


class TrainQueryRepository:
    @staticmethod
    def get_all_trains_name(client_id) -> list:
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
                "ClientID" = %s::bigint
            GROUP BY
                "ClientID"
            """, [client_id]
        )

        return result if result else []

class TrainRepository(TrainCRUDRepository, TrainQueryRepository):
    def __init__(self):
        TrainCRUDRepository.__init__(self)
        TrainQueryRepository.__init__(self)