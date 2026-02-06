from typing import Dict, List

from ..database import sql_query, sql_query_record
from ..base_names import *
from ..database.update import (
    update_client_status,
    update_client_selected_entity,
    update_selected_entity_by_id,
)
from ..database.select import get_client_selected_entity


class ExerciseStatus:
    """
    Статусы упражнений
    """
    CREATE = 5
    DELETE = 6
    CHANGE = 7
    RENAME = 8
    UPDATE = 9
    status_array = [CREATE, RENAME, CHANGE, DELETE, UPDATE]


class Exercise:
    """
    Класс с форматом упражнения
    """
    def __init__(self, exercise: dict):
        self._id: int = exercise.get("Id")
        self.name: str = exercise.get("Name")
        self.split_settings: Dict[str, str] = self.split_settings(exercise.get("Settings"))
        self.train: str = exercise.get("TrainId")

    @staticmethod
    def split_settings(settings: str) -> Dict[str, str]:
        """
        Внутренний метод для парсинга настроек упражнения
        """
        split_result = {}
        if not settings:
            raise Exception("Not transmitted parameter - Settings")

        split_settings: List[str] = settings.split("/n")
        for row in split_settings:
            split_row: List[str] = row.split(":")
            split_row = list(map(str.strip, split_row))
            split_result[split_row[0]] = split_row[1]

        return split_result

    def get_exercise_str(self) -> str:
        """
        Получить настройки упражнения в виде отформатированной строки
        """
        result = f'Упражнение - {self.name}\n' + \
                  "\n\n".join(
                      f"Вес - {count} \nКоличество подходов - {value}" for count, value in self.split_settings.items()
                  )

        return result