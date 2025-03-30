from typing import List
import json
from re import findall

from bot_app import base_names
from bot_app.base_names import TrainStatus
from bot_app.operation.exercise import ExerciseOperation, ExerciseStatus
from bot_app.operation.train import TrainOperation
from bot_app.database.update import update_client_status, set_exercise_settings
from bot_app.database.select import all_exercise_for_keyboard, get_client_selected_entity, read_exercise

class BaseOperation():
    def call_method(self, client_id: int, client_status: int, msg) -> (str, List[str]):
        text_msg = ""
        key_board = []
        if client_status == base_names.TrainStatus.CHANGE and \
                msg.text == base_names.SetTrainSettingsButtons.add_exercise:
            update_client_status(client_id, ExerciseStatus.CREATE)
            text_msg = "Напишите название упражнения"
            key_board = base_names.SetTrainSettingsButtons.buttons_array

        elif client_status == base_names.TrainStatus.CHANGE and \
                msg.text == base_names.SetTrainSettingsButtons.rename_train:
            update_client_status(client_id, TrainStatus.RENAME)
            text_msg = "Напишите новое название для тренировки"
            key_board = base_names.SetTrainSettingsButtons.buttons_array

        elif client_status == base_names.TrainStatus.CHANGE and \
                msg.text == base_names.SetTrainSettingsButtons.change_exercise:
            update_client_status(client_id, ExerciseStatus.CHANGE)
            text_msg = "Выберите упражнение"
            key_board = all_exercise_for_keyboard(
                get_client_selected_entity(client_id)
            )

        elif client_status in base_names.TrainStatus.status_array:
            text_msg, key_board = TrainOperation(client_id).execute_method_by_status(client_status, msg.text)
        elif client_status in base_names.ExerciseStatus.status_array:
            text_msg, key_board = ExerciseOperation(client_id).execute_method_by_status(client_status, msg.text)
        elif client_status == base_names.EXERCISE_READ_STATUS and msg.text == base_names.SetExerciseSettingsButtons.back:
            selected_entity = get_client_selected_entity(client_id)
            exercise = read_exercise(selected_entity)
            train_id = exercise.get("TrainId")
            key_board = all_exercise_for_keyboard(train_id)
            text_msg = "Выбранная тренировка"

        elif client_status == base_names.EXERCISE_READ_STATUS:
            if findall(r"\d{,3}:", msg.text):
                # значит апдейтим упражнение
                selected_entity = get_client_selected_entity(client_id)
                set_exercise_settings(selected_entity, json.dumps(msg.text))

                exercise = read_exercise(selected_entity)
                train_id = exercise.get("TrainId")

                key_board = all_exercise_for_keyboard(train_id)
                text_msg = "Выбранная тренировка"
            else:
                selected_entity = get_client_selected_entity(client_id)
                exercise = read_exercise(selected_entity)
                text_msg = exercise.get("Settings")
                key_board = [base_names.SetExerciseSettingsButtons.back]


        return text_msg, key_board
