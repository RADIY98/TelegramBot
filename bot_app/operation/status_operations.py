from typing import List
import json
from re import findall

from .. import base_names
from ..base_names import TrainStatus
from ..client import Client
from ..operation.exercise import ExerciseOperation, ExerciseStatus
from ..operation.train import TrainOperation
from ..database.update import update_client_status, set_exercise_settings, update_client_selected_entity
from ..database import select
from ..operation.exercise import Exercise


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

    def call_method(self, msg) -> (str, List[str]):
        text_msg = ""
        print(f"ВОТ так вот {self.client_obj.status}  {msg.text}")
        key_board = []
        if msg.text == base_names.MAIN_MENU:
            update_client_selected_entity(self.client_obj.client_id, None)
            update_client_status(self.client_obj.client_id, None)
            return base_names.BACK_TO_MAIN_MENU, base_names.StartButtons.buttons_array
        if self.client_obj.status == base_names.TrainStatus.CHANGE and \
                msg.text == base_names.SetTrainSettingsButtons.add_exercise:
            update_client_status(self.client_obj.client_id, ExerciseStatus.CREATE)
            text_msg = self.WRITE_EXERCISE_NAME
            key_board = base_names.SetTrainSettingsButtons.buttons_array

        elif self.client_obj.status == base_names.TrainStatus.CHANGE and \
                msg.text == base_names.SetTrainSettingsButtons.rename_train:
            update_client_status(self.client_obj.client_id, TrainStatus.RENAME)
            text_msg = self.WRITE_NEW_TRAIN_NAME
            key_board = base_names.SetTrainSettingsButtons.buttons_array

        elif self.client_obj.status == base_names.TrainStatus.CHANGE and \
                msg.text == base_names.SetTrainSettingsButtons.change_exercise:
            update_client_status(self.client_obj.client_id, ExerciseStatus.CHANGE)
            text_msg = self.CHOOSE_EXERCISE_FROM_LIST
            key_board = select.all_exercise_for_keyboard(self.client_obj.selected_entity)

        elif self.client_obj.status in base_names.TrainStatus.status_array:
            text_msg, key_board = TrainOperation(self.client_obj.client_id).handler(
                self.client_obj.status,
                msg.text
            )
        elif self.client_obj.status in base_names.ExerciseStatus.status_array:
            text_msg, key_board = ExerciseOperation(self.client_obj.client_id).handler(
                self.client_obj.status,
                msg.text
            )
        elif self.client_obj.status == base_names.EXERCISE_READ_STATUS and msg.text == base_names.SetExerciseSettingsButtons.back:
            exercise = select.read_exercise(self.client_obj.selected_entity)
            train_id = exercise.get("TrainId")
            key_board = select.all_exercise_for_keyboard(train_id)
            text_msg = self.SELECTED_TRAIN.format(TrainOperation(self.client_obj.client_id).read(train_id))

        elif self.client_obj.status == base_names.EXERCISE_READ_STATUS:
            if findall(r"\d{,3}:", msg.text):
                # значит апдейтим упражнение
                set_exercise_settings(self.client_obj.selected_entity, json.dumps(msg.text))

                exercise = select.read_exercise(self.client_obj.selected_entity)
                train_id = exercise.get("TrainId")

                key_board = select.all_exercise_for_keyboard(train_id)
                text_msg = (
                    f"{base_names.UPDATED_EXERCISE}"
                    f"{base_names.SELECTED_TRAIN.format(TrainOperation(self.client_obj.client_id).read(train_id))}"
                )

            else:
                text_msg = Exercise(select.read_exercise(self.client_obj.selected_entity)).get_exercise_str()
                key_board = [base_names.SetExerciseSettingsButtons.back]


        return text_msg, key_board
