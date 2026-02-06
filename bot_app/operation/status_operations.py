from typing import List
import json
from re import findall

from .. import base_names
from ..exercise import ExerciseStatus
from ..train import TrainStatus
from ..client import Client
from bot_app.train.service import TrainService
from ..database.update import update_client_status, update_client_selected_entity
from ..exercise import Exercise
from ..exercise import repository, service

class BaseOperation:
    """
    Базовый метод для операций по статусам
    """
    WRITE_EXERCISE_NAME = "Напишите название упражнения"
    WRITE_NEW_TRAIN_NAME = "Напишите новое название для тренировки"
    CHOOSE_EXERCISE_FROM_LIST = "Выберите упражнение из списка"
    SELECTED_TRAIN = 'Вы выбрали тренировку - "{}"'

    def __init__(self, client_obj: Client):
        self.client_obj = client_obj
        self.exercise_service = service.ExerciseOperationService(client_obj.client_id)
        self.exercise_repository = repository.ExerciseRepository

    def call_method(self, msg) -> (str, List[str]):
        text_msg = ""
        print(f"ВОТ так вот {self.client_obj.status}  {msg.text}")
        key_board = []
        if msg.text == base_names.MAIN_MENU:
            update_client_selected_entity(self.client_obj.client_id, None)
            update_client_status(self.client_obj.client_id, None)
            return base_names.BACK_TO_MAIN_MENU, base_names.StartButtons.buttons_array
        if self.client_obj.status == TrainStatus.CHANGE and \
                msg.text == base_names.SetTrainSettingsButtons.add_exercise:
            update_client_status(self.client_obj.client_id, ExerciseStatus.CREATE)
            text_msg = self.WRITE_EXERCISE_NAME
            key_board = base_names.SetTrainSettingsButtons.buttons_array

        elif self.client_obj.status == TrainStatus.CHANGE and \
                msg.text == base_names.SetTrainSettingsButtons.rename_train:
            update_client_status(self.client_obj.client_id, TrainStatus.RENAME)
            text_msg = self.WRITE_NEW_TRAIN_NAME
            key_board = base_names.SetTrainSettingsButtons.buttons_array

        elif self.client_obj.status == TrainStatus.CHANGE and \
                msg.text == base_names.SetTrainSettingsButtons.change_exercise:
            update_client_status(self.client_obj.client_id, ExerciseStatus.CHANGE)
            text_msg = self.CHOOSE_EXERCISE_FROM_LIST
            key_board = self.exercise_service.get_exercises_name_by_train(
                self.client_obj.selected_entity
            )

        elif self.client_obj.status in TrainStatus.status_array:
            text_msg, key_board = TrainService(self.client_obj.client_id).process(
                self.client_obj.status,
                msg.text
            )
        elif self.client_obj.status in ExerciseStatus.status_array:
            text_msg, key_board = self.exercise_service.process(
                self.client_obj.status,
                msg.text
            )
        elif self.client_obj.status == base_names.EXERCISE_READ_STATUS and msg.text == base_names.SetExerciseSettingsButtons.back:
            exercise = self.exercise_repository.read(self.client_obj.selected_entity)
            train_id = exercise.get("TrainId")
            key_board = self.exercise_service.get_exercises_name_by_train(train_id)
            text_msg = self.SELECTED_TRAIN.format(TrainService(self.client_obj.client_id).read(train_id))

        elif self.client_obj.status == base_names.EXERCISE_READ_STATUS:
            if findall(r"\d{,3}:", msg.text):
                # значит апдейтим упражнение
                self.exercise_repository.update(self.client_obj.selected_entity, json.dumps(msg.text))

                exercise = self.exercise_repository.read(self.client_obj.selected_entity)
                train_id = exercise.get("TrainId")

                key_board = self.exercise_service.get_exercises_name_by_train(train_id)
                text_msg = (
                    f"{base_names.UPDATED_EXERCISE}"
                    f"{base_names.SELECTED_TRAIN.format(TrainService(self.client_obj.client_id).read(train_id))}"
                )

            else:
                text_msg = Exercise(self.exercise_repository.read(self.client_obj.selected_entity)).get_exercise_str()
                key_board = [base_names.SetExerciseSettingsButtons.back]


        return text_msg, key_board
