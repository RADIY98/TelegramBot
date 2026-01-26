from typing import Tuple, List, Dict
import json

from . import exercise_repository
from . import *


class ExerciseOperationService:
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
        self.exercise_repository = exercise_repository.ExerciseRepository
        self.client_id: int = client_id

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
        self.exercise_repository.add(msg, self.client_id)
        update_client_status(self.client_id, TrainStatus.CHANGE)

        return self.EXERCISE_CREATED.format(msg), SetTrainSettingsButtons.buttons_array

    def delete(self) -> str:
        """
        Удаление упражнения
        """
        exercise_name, train_id = self.exercise_repository.delete(self.client_id)
        update_selected_entity_by_id(self.client_id, train_id)
        update_client_status(self.client_id, ExerciseStatus.CHANGE)

        return self.EXERCISE_DELETED.format(exercise_name)

    def rename(self, new_name: str) -> Tuple[str, list]:
        """
        Переименовать упражнение
        """
        update_client_status(self.client_id, ExerciseStatus.CHANGE)
        selected_entity = get_client_selected_entity(self.client_id)

        self.exercise_repository.rename(new_name, selected_entity)

        return "Упражнение переименовано", SetExerciseSettingsButtons.buttons_array

    def change(self, msg: str) -> Tuple[str, list]:
        """
        Изменить упражнение
        """
        text_msg = ""
        keyboard = []
        selected_entity = get_client_selected_entity(self.client_id)
        if msg == MAIN_MENU:
            update_client_selected_entity(self.client_id, None)
            update_client_status(self.client_id, None)
            return BACK_TO_MAIN_MENU, StartButtons.buttons_array
        # TODO Это вообще пиздец. Нельзя ориентироваться на название упражнения. Переделать на статус клиента
        # if is_exercise(msg):
        if False:
            update_client_selected_entity(self.client_id, msg)
            text_msg = self.SELECTED_EXERCISE.format(msg)
            keyboard = SetExerciseSettingsButtons.buttons_array
        elif msg == NO_EXERCISE:
            update_client_status(self.client_id, ExerciseStatus.CREATE)
            text_msg = self.WRITE_NEW_EXERCISE_NAME
            keyboard = SetTrainSettingsButtons.buttons_array

        elif msg == SetExerciseSettingsButtons.delete:
            text_msg, keyboard = self.exercise_repository.delete(self.client_id)
        elif msg == SetExerciseSettingsButtons.rename:
            update_client_status(self.client_id, ExerciseStatus.RENAME)
            text_msg = self.WRITE_NEW_EXERCISE_NAME
            keyboard = SetExerciseSettingsButtons.buttons_array
        elif msg == SetExerciseSettingsButtons.back:
            exercise: dict = self.exercise_repository.read(selected_entity)
            train_id: int = exercise.get("TrainId")
            update_selected_entity_by_id(self.client_id, train_id)
            text_msg, keyboard = self.BACK_TO_EXERCISE, self.get_exercises_name_by_train(train_id)
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

        self.exercise_repository.update(selected_entity, json.dumps(msg))
        update_client_status(self.client_id, ExerciseStatus.CHANGE)
        return UPDATED_EXERCISE, SetExerciseSettingsButtons.buttons_array

    def get_exercises_name_by_train(self, train_id: int):
        exercises: List[Dict]  = self.exercise_repository.get_by_train([train_id])
        exercises_names: List[str] = [exe.get("Name") for exe in exercises]
        if not exercises_names:
            exercises_names = ["Давайте добавим упражнения"]
        exercises_names.append(MAIN_MENU)

        return exercises_names