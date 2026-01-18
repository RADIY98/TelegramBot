"""
Модуль для работы с тренировками
"""
from .. import base_names
from ..operation import Operation
from ..database.insert import insert_train
from ..database.select import get_client_selected_entity, get_all_trains_for_keyboard, read_train
from ..database.delete import delete_train
from ..database.update import update_client_status, update_train, drop_selected_entity, update_client_selected_entity
from ..base_names import TrainSettingsButton, TrainStatus, SetTrainSettingsButtons, MAIN_MENU, StartButtons


class TrainOperation(Operation):
    TRAIN_CREATED = 'Тренировка "{}" успешно создана'
    TRAIN_DELETED = 'Тренировка "{}" успешно удалена'
    TRAIN_RENAMED = 'Тренировка "{}" успешно переименована'
    WRITE_NEW_TRAIN_NAME = "Напишите новое название тренировки"
    BACK_TO_TRAIN = "Возвращаемся к тренировкам"

    def __init__(self, client_id: int):
        self.client_id = client_id


    def handler(self, status: int, msg: str) -> (str, list):
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
        return self.TRAIN_CREATED.format(msg), TrainSettingsButton.buttons_array

    def delete(self, msg: str) -> (str, list):
        """
        Метод удаления тренировки
        """
        delete_train(msg)
        update_client_status(self.client_id, None)

        return self.TRAIN_DELETED.format(msg), TrainSettingsButton.buttons_array

    def rename(self, msg: str) -> (str, list):
        """
        Создание тренировки
        """
        update_train(self.client_id, msg)
        update_client_status(self.client_id, TrainStatus.CHANGE)

        return self.TRAIN_RENAMED.format(msg), SetTrainSettingsButtons.buttons_array

    def change(self, msg: str) -> (str, list):
        """
        Изменение настроек тренировки
        """
        keyboard = []
        print("Зашли")
        selected_entity: int = get_client_selected_entity(self.client_id)
        print(f"Я тута {selected_entity}")
        if msg == MAIN_MENU:
            text_msg = base_names.BACK_TO_MAIN_MENU
            keyboard = StartButtons.buttons_array
        else:
            if selected_entity:
                if msg == SetTrainSettingsButtons.rename_train:
                    text_msg = self.WRITE_NEW_TRAIN_NAME
                    update_client_status(self.client_id, TrainStatus.RENAME)
                    keyboard = SetTrainSettingsButtons.buttons_array
                elif msg ==SetTrainSettingsButtons.back_to_trains:
                    text_msg = self.BACK_TO_TRAIN
                    drop_selected_entity(self.client_id)
                    keyboard = get_all_trains_for_keyboard(self.client_id)
                    keyboard.append(MAIN_MENU)

            else:
                update_client_selected_entity(self.client_id, msg)
                text_msg = base_names.SELECTED_TRAIN.format(msg)
                keyboard = SetTrainSettingsButtons.buttons_array

        return text_msg, keyboard

    def read(self, train_id: int):
        """
        Получить информацию о тренировке
        """
        train_info = read_train(self.client_id, train_id)
        return train_info.get("Name")