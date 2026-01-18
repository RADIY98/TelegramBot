import json
from typing import List, Tuple

from . import Operation
from .. import base_names
from ..database.insert import insert_exercise
from ..database.update import (
    update_client_status,
    update_client_selected_entity,
    update_selected_entity_by_id,
    rename_exercise,
    set_exercise_settings
)
from ..database.delete import delete_exercise
from ..database.select import get_client_selected_entity, is_exercise, all_exercise_for_keyboard, read_exercise
from ..base_names import TrainStatus, SetTrainSettingsButtons, ExerciseStatus, SetExerciseSettingsButtons

class ExerciseOperation(Operation):
    """
    Операции над упражнеениями
    """
    EXERCISE_CREATED =  'Упражнение - "{}" успешно добавлено'
    EXERCISE_DELETED = "Упражнение {} успешно удалено"
    WRITE_NEW_EXERCISE_NAME = "Напишите новое название для упражнения"
    BACK_TO_EXERCISE = "Вернулись к упражнениям"
    WRITE_EXERCISE_SETTINGS = "Напишите настройки упражнения в формате ВЕС: количество подходов через запятую"
    SELECTED_EXERCISE = 'Выбрано упражнение - "{}"'


    def __init__(self, client_id: int):
        """
        Инициализация класса
        """
        self.client_id = client_id

    def handler(self, status: int, msg: str) -> Tuple[str, list]:
        """
        Сопоставим статусу нужный метод
        """
        operation_by_status = {
            ExerciseStatus.CHANGE: self.change,
            ExerciseStatus.DELETE: self.delete,
            ExerciseStatus.CREATE: self.create,
            ExerciseStatus.RENAME: self.rename,
            ExerciseStatus.UPDATE: self.update,
        }
        method = operation_by_status.get(status)

        return method(msg)

    def create(self, msg: str) -> Tuple[str, list]:
        """
        Добавить упражнение
        """
        insert_exercise(self.client_id, msg)
        update_client_status(self.client_id, TrainStatus.CHANGE)

        return self.EXERCISE_CREATED.format(msg), SetTrainSettingsButtons.buttons_array

    def delete(self, msg: str) -> str:
        """
        Удаление упражнения
        """
        exercise_name, train_id = delete_exercise(self.client_id)
        update_selected_entity_by_id(self.client_id, train_id)
        update_client_status(self.client_id, ExerciseStatus.CHANGE)

        return self.EXERCISE_DELETED.format(exercise_name)

    def rename(self, new_name: str) -> Tuple[str, list]:
        """
        Переименовать упражнение
        """
        update_client_status(self.client_id, ExerciseStatus.CHANGE)
        selected_entity = get_client_selected_entity(self.client_id)

        rename_exercise(new_name, selected_entity)

        return "Упражнение переименовано", SetExerciseSettingsButtons.buttons_array

    def change(self, msg: str) -> Tuple[str, list]:
        """
        Изменить упражнение
        """
        text_msg = ""
        keyboard = []
        selected_entity = get_client_selected_entity(self.client_id)
        if msg == base_names.MAIN_MENU:
            update_client_selected_entity(self.client_id, None)
            update_client_status(self.client_id, None)
            return base_names.BACK_TO_MAIN_MENU, base_names.StartButtons.buttons_array

        if is_exercise(msg):
            update_client_selected_entity(self.client_id, msg)
            text_msg = self.SELECTED_EXERCISE.format(msg)
            keyboard = SetExerciseSettingsButtons.buttons_array
        elif msg == base_names.NO_EXERCISE:
            update_client_status(self.client_id, ExerciseStatus.CREATE)
            text_msg = self.WRITE_NEW_EXERCISE_NAME
            keyboard = base_names.SetTrainSettingsButtons.buttons_array

        elif msg == SetExerciseSettingsButtons.delete:
            text_msg, keyboard = ExerciseOperation(self.client_id).delete(msg)
        elif msg == SetExerciseSettingsButtons.rename:
            update_client_status(self.client_id, ExerciseStatus.RENAME)
            text_msg = self.WRITE_NEW_EXERCISE_NAME
            keyboard = SetExerciseSettingsButtons.buttons_array
        elif msg == SetExerciseSettingsButtons.back:
            exercise: dict = read_exercise(selected_entity)
            train_id: int = exercise.get("TrainId")
            update_selected_entity_by_id(self.client_id, train_id)
            text_msg, keyboard = self.BACK_TO_EXERCISE, all_exercise_for_keyboard(train_id)
        elif msg == SetExerciseSettingsButtons.change:
            update_client_status(self.client_id, ExerciseStatus.UPDATE)
            text_msg = self.WRITE_EXERCISE_SETTINGS
            keyboard = SetExerciseSettingsButtons.buttons_array



        return text_msg, keyboard

    def update(self, msg: str) -> Tuple[str, list]:
        """
        Задать настройки тренировки
        """
        selected_entity = get_client_selected_entity(self.client_id)

        set_exercise_settings(selected_entity, json.dumps(msg))
        update_client_status(self.client_id, ExerciseStatus.CHANGE)
        return base_names.UPDATED_EXERCISE, SetExerciseSettingsButtons.buttons_array

class Exercise:
    """
    Класс с форматом упражнения
    """
    def __init__(self, exercise: dict):
        self._id: int = exercise.get("Id")
        self.name: str = exercise.get("Name")
        self.split_settings: dict = self.__split_settings(exercise.get("Settings"))
        self.train: str = exercise.get("TrainId")

    @staticmethod
    def __split_settings(settings: str) -> dict:
        """
        Внутренний метод для парсинга настроек упражнения
        """
        split_result = {}

        split_settings: List[str] = settings.split("/n")
        print(split_settings)
        for row in split_settings:
            print(row)
            split_row: List[str] = row.split(":")
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