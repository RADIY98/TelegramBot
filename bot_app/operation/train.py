"""
Модуль для работы с тренировками
"""
from ..operation import Operation
from ..database.insert import insert_train
from ..database.select import get_client_selected_entity, get_all_trains_for_keyboard
from ..database.delete import delete_train
from ..database.update import update_client_status, update_train, drop_selected_entity, update_client_selected_entity
from ..base_names import TrainSettingsButton, TrainStatus, SetTrainSettingsButtons, ExerciseStatus, MAIN_MENU, StartButtons


class TrainOperation(Operation):
    def __init__(self, client_id: int):
        self.client_id = client_id


    def execute_method_by_status(self, status: int, msg: str) -> (str, list):
        """
        Сопоставим статусу нужный метод
        """
        operation_by_status = {
            TrainStatus.CHANGE: self.change,
            TrainStatus.DELETE: self.delete,
            TrainStatus.CREATE: self.create,
            TrainStatus.RENAME: self.rename,
        }
        method = operation_by_status.get(status)

        return method(msg)

    def create(self, msg: str) -> (str, list):
        """
        Создание тренировки
        """
        insert_train(self.client_id, msg)
        update_client_status(self.client_id, None)
        return f'Тренировка "{msg}" успешно создана', TrainSettingsButton.buttons_array

    def delete(self, msg: str) -> (str, list):
        """
        Метод удаления тренировки
        """
        delete_train(msg)
        update_client_status(self.client_id, None)

        return f'Тренировка "{msg}" успешно удалена', TrainSettingsButton.buttons_array

    def rename(self, msg: str) -> (str, list):
        """
        Создание тренировки
        """
        update_train(self.client_id, msg)
        update_client_status(self.client_id, TrainStatus.CHANGE)

        return f'Тренировка "{msg}" успешно переименована', SetTrainSettingsButtons.buttons_array

    def change(self, msg: str) -> (str, list):
        """
        Изменение настроек тренировки
        """
        keyboard = []
        selected_entity: int = get_client_selected_entity(self.client_id)
        if msg == MAIN_MENU:
            text_msg = ""
            keyboard = StartButtons.buttons_array
        else:
            if selected_entity:
                if msg == SetTrainSettingsButtons.rename_train:
                    text_msg = "Напишите новое название тренировки"
                    update_client_status(self.client_id, TrainStatus.RENAME)
                    keyboard = SetTrainSettingsButtons.buttons_array
                elif msg ==SetTrainSettingsButtons.back_to_trains:
                    text_msg = "Возвращаемся к тренировкам"
                    drop_selected_entity(self.client_id)
                    keyboard = get_all_trains_for_keyboard(self.client_id)
                    keyboard.append(MAIN_MENU)

            else:
                update_client_selected_entity(self.client_id, msg)
                text_msg = f'Выбрана тренировка - "{msg}"'
                keyboard = SetTrainSettingsButtons.buttons_array

        return text_msg, keyboard
