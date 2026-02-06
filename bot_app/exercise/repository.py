from typing import Tuple
import json

from . import *

class ExerciseCRUDRepository:

    def __init__(self):
        #TODO Добавить через композицию класс содержащий информацию о клиенте.
        # Пока передаем ручками
        # self.client_obj =
        pass

    @staticmethod
    def add(exercise_name: str, client_id: int):
        sql_query(
            """
            INSERT INTO "Exercise"
            ("Name",
             "TrainId")
            SELECT %s::text AS "ExerciseName", "SelectedEntity"
            FROM "Client"
            WHERE "id" = %s::bigint
            """, (exercise_name, client_id)
        )

    @staticmethod
    def delete(client_id: int) -> Tuple[str, int]:
        exercise = sql_query_record(
            """
            DELETE
            FROM "Exercise"
            WHERE "id" = (SELECT "SelectedEntity" FROM "Client" WHERE "id" = %s) RETURNING
                "Name",
                "TrainId"
            """, [client_id]
        )
        return exercise.get("Name"), int(exercise.get("TrainId"))

    @staticmethod
    def rename(exercise_name: str, selected_entity: int) -> None:
        """
        Переименовываем упражнения
        """
        sql_query(
            """
            UPDATE
                "Exercise"
            SET "Name"=%s::text
            WHERE
                "id"=%s:: int
            """, [exercise_name, selected_entity]
        )

    @staticmethod
    def update(exercise_id: int, settings: json) -> None:
        """
        Задать настройки упражнения
        """
        sql_query_record(
            """
            UPDATE
                "Exercise"
            SET "Settings"=%s::jsonb
            WHERE
                "id"=%s:: int
            """, [settings, exercise_id]
        )

    @staticmethod
    def read(exercise_id: int) -> dict:
        """
        Прочитаем упражнение
        """
        result = sql_query_record(
            """
            SELECT *
            FROM "Exercise"
            WHERE "id" = %s::bigint
            """, [exercise_id]
        )
        return result


class ExerciseQueryRepository:

    @staticmethod
    def get_by_train(train_id: int) -> List[Dict]:
        result = sql_query(
            """
            SELECT
                *
            FROM
                "Exercise"
            WHERE
                "TrainId" = %s::bigint
            """, [train_id]
        )
        return result


class ExerciseRepository(ExerciseCRUDRepository, ExerciseQueryRepository):
    def __init__(self):
        ExerciseCRUDRepository.__init__(self)
        ExerciseQueryRepository.__init__(self)
