"""
Модуль для работы с тренировками
"""
from typing import Tuple

from bot_app import base_names
from bot_app.domain.entities.client_status import ClientStatus
from bot_app.operation import Operation
from bot_app.database.select import get_client_selected_entity
from bot_app.database.update import drop_selected_entity, update_client_selected_entity
from bot_app.base_names import TrainSettingsButton, SetTrainSettingsButtons, MAIN_MENU, StartButtons
from bot_app.repositories.train_repository import TrainRepository
from bot_app.train import TrainStatus


class TrainService(Operation):
    TRAIN_CREATED = 'Тренировка "{}" успешно создана'
    TRAIN_DELETED = 'Тренировка "{}" успешно удалена'
    TRAIN_RENAMED = 'Тренировка "{}" успешно переименована'
    WRITE_NEW_TRAIN_NAME = "Напишите новое название тренировки"
    BACK_TO_TRAIN = "Возвращаемся к тренировкам"

    def __init__(self, client_id: int, train_crud: TrainRepository, client_status: ClientStatus):
        self.client_id = client_id
        self._handlers = {
            TrainStatus.CHANGE: self.change,
            TrainStatus.DELETE: self.delete,
            TrainStatus.CREATE: self.create,
            TrainStatus.RENAME: self.rename,
        }
        self.train_crud = train_crud
        self.client_status = client_status


    def process(self, status: int, msg: str) -> Tuple[str, list]:
        """
        Сопоставим статусу нужный метод
        """
        return self._handlers.get(status)(msg)

    def create(self, msg: str) -> Tuple[str, list]:
        """
        Создание тренировки
        """
        self.train_crud.add(self.client_id, msg)

        self.client_status.set_status(None)

        return self.TRAIN_CREATED.format(msg), TrainSettingsButton.buttons_array

    def delete(self, msg: str) -> Tuple[str, list]:
        """
        Метод удаления тренировки
        """
        self.train_crud.delete(msg)

        self.client_status.set_status(None)

        return self.TRAIN_DELETED.format(msg), TrainSettingsButton.buttons_array

    def rename(self, msg: str) -> Tuple[str, list]:
        """
        Создание тренировки
        """
        self.train_crud.rename(self.client_id, msg)

        self.client_status.set_status(TrainStatus.CHANGE)

        return self.TRAIN_RENAMED.format(msg), SetTrainSettingsButtons.buttons_array

    def change(self, msg: str) -> Tuple[str, list]:
        """
        Изменение настроек тренировки
        """
        keyboard = []
        selected_entity: int = get_client_selected_entity(self.client_id)
        if msg == MAIN_MENU:
            text_msg = base_names.BACK_TO_MAIN_MENU
            keyboard = StartButtons.buttons_array
        else:
            if selected_entity:
                if msg == SetTrainSettingsButtons.rename_train:
                    text_msg = self.WRITE_NEW_TRAIN_NAME

                    self.client_status.set_status(TrainStatus.RENAME)

                    keyboard = SetTrainSettingsButtons.buttons_array
                elif msg ==SetTrainSettingsButtons.back_to_trains:
                    text_msg = self.BACK_TO_TRAIN
                    drop_selected_entity(self.client_id)
                    keyboard = self.train_crud.get_all_trains_name(self.client_id)
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
        train_info = self.train_crud.read(self.client_id, train_id)
        return train_info.get("Name")