from typing import List
import json
from re import findall

from bot_app import base_names
from bot_app.base_names import TrainStatus
from bot_app.operation.exercise import ExerciseOperation, ExerciseStatus
from bot_app.operation.train import TrainOperation
from bot_app.database.update import update_client_status, set_exercise_settings, update_client_selected_entity
from bot_app.database.select import all_exercise_for_keyboard, get_client_selected_entity, read_exercise, read_train
from bot_app.operation.exercise import Exercise


class BaseOperation:
    WRITE_EXERCISE_NAME = "Напишите название упражнения"
    WRITE_NEW_TRAIN_NAME = "Напишите новое название для тренировки"
    CHOOSE_EXERCISE_FROM_LIST = "Выберите упражнение из списка"
    SELECTED_TRAIN = 'Вы выбрали тренировку - "{}"'


    def call_method(self, client_id: int, client_status: int, msg) -> (str, List[str]):
        text_msg = ""
        print(f"ВОТ так вот {client_status}  {msg.text}")
        key_board = []
        if msg.text == base_names.MAIN_MENU:
            update_client_selected_entity(client_id, None)
            update_client_status(client_id, None)
            return base_names.BACK_TO_MAIN_MENU, base_names.StartButtons.buttons_array
        if client_status == base_names.TrainStatus.CHANGE and \
                msg.text == base_names.SetTrainSettingsButtons.add_exercise:
            update_client_status(client_id, ExerciseStatus.CREATE)
            text_msg = self.WRITE_EXERCISE_NAME
            key_board = base_names.SetTrainSettingsButtons.buttons_array

        elif client_status == base_names.TrainStatus.CHANGE and \
                msg.text == base_names.SetTrainSettingsButtons.rename_train:
            update_client_status(client_id, TrainStatus.RENAME)
            text_msg = self.WRITE_NEW_TRAIN_NAME
            key_board = base_names.SetTrainSettingsButtons.buttons_array

        elif client_status == base_names.TrainStatus.CHANGE and \
                msg.text == base_names.SetTrainSettingsButtons.change_exercise:
            update_client_status(client_id, ExerciseStatus.CHANGE)
            text_msg = self.CHOOSE_EXERCISE_FROM_LIST
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
            text_msg = self.SELECTED_TRAIN.format(TrainOperation(client_id).read(train_id))

        elif client_status == base_names.EXERCISE_READ_STATUS:
            if findall(r"\d{,3}:", msg.text):
                # значит апдейтим упражнение
                selected_entity = get_client_selected_entity(client_id)
                set_exercise_settings(selected_entity, json.dumps(msg.text))

                exercise = read_exercise(selected_entity)
                train_id = exercise.get("TrainId")

                key_board = all_exercise_for_keyboard(train_id)
                text_msg = (
                    f"{base_names.UPDATED_EXERCISE}"
                    f"{base_names.SELECTED_TRAIN.format(TrainOperation(client_id).read(train_id))}"
                )

            else:
                selected_entity = get_client_selected_entity(client_id)
                text_msg = Exercise(read_exercise(selected_entity)).get_exercise_str()
                key_board = [base_names.SetExerciseSettingsButtons.back]


        return text_msg, key_board
