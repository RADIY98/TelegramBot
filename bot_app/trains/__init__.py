"""
Модуль для CRUD методов тренировок
"""
from bot_app import base_names
from bot_app.database import insert, delete, select
from bot_app.database import update
from bot_app.database import sql_query_scalar


class TrainOperations:
    def __init__(self, client_id: int):
        self.operation_by_status = {
            base_names.TrainStatus.CHANGE: self.change_train,
            base_names.TrainStatus.DELETE: self.delete_train,
            base_names.TrainStatus.CREATE: self.create_train,
            base_names.TrainStatus.RENAME: self.rename_train,
            base_names.ExerciseStatus.CREATE: self.create_exercise,
        }
        self.client_id = client_id

    def get_operation(self, client_status: int, msg) -> (str, list):
        operation = self.operation_by_status.get(client_status)
        return operation(msg)

    def delete_train(self, msg: str) -> (str, list):
        """
        Метод удаления тренировки
        """
        delete.delete_train(msg)
        update.update_client_status(self.client_id, None)
        return f'Тренировка "{msg}" успешно удалена', base_names.TrainSettingsButton.buttons_array

    def rename_train(self, msg: str) -> (str, list):
        """
        Создание тренировки
        """
        update.update_train(self.client_id, msg)
        update.update_client_status(self.client_id, base_names.TrainStatus.CHANGE)

        return f'Тренировка "{msg}" успешно переименована', base_names.SetTrainSettingsButtons.buttons_array

    def create_train(self, msg: str) -> (str, list):
        """
        Создание тренировки
        """
        insert.insert_train(self.client_id, msg)
        update.update_client_status(self.client_id, None)
        return f'Тренировка "{msg}" успешно создана', base_names.TrainSettingsButton.buttons_array

    def create_exercise(self, msg: str) -> (str, list):
        """
        Добавить упражнение
        """
        insert.insert_exercise(self.client_id, msg)
        update.update_client_status(self.client_id, base_names.TrainStatus.CHANGE)

        return f'Упражнение - "{msg}" успешно добавлено', base_names.SetTrainSettingsButtons.buttons_array

    def change_train(self, msg: str) -> (str, list):
        """
        Изменение настроек тренировки
        """
        keyboard = []
        selected_entity: int = select.get_client_selected_entity(self.client_id)
        if msg == base_names.MAIN_MENU:
            text_msg = ""
            keyboard = base_names.StartButtons.buttons_array
        if selected_entity:
            if msg == base_names.SetTrainSettingsButtons.rename_train:
                text_msg = "Напишите новое название тренировки"
                update.update_client_status(self.client_id, base_names.TrainStatus.RENAME)
                keyboard = base_names.SetTrainSettingsButtons.buttons_array
            elif msg == base_names.SetTrainSettingsButtons.change_exercise:
                pass
            elif msg == base_names.SetTrainSettingsButtons.add_exercise:
                text_msg = "Напишите название упражнения"
                update.update_client_status(self.client_id, base_names.ExerciseStatus.CREATE)
                keyboard = base_names.SetTrainSettingsButtons.buttons_array
            elif msg == base_names.SetTrainSettingsButtons.back_to_trains:
                text_msg = "Возвращаемся к тренировкам"
                update.drop_selected_entity(self.client_id)
                keyboard = get_all_trains_for_keyboard(self.client_id)

        else:
            update.update_client_selected_entity(self.client_id, msg)
            text_msg = f'Выбрана тренировка - "{selected_entity}"'
            keyboard = base_names.SetTrainSettingsButtons.buttons_array

        return text_msg, keyboard


def get_all_trains_for_keyboard(client_id):
    """
    Получить тренировку
    """
    result = sql_query_scalar(
        """
            SELECT
                array_agg("Name")
            FROM
                "Train"
            WHERE
                "ClientID"=%s::bigint
            GROUP BY
                "ClientID"
        """, [client_id]
    )
    if result:
        result.append(base_names.MAIN_MENU)
    else:
        result = [base_names.MAIN_MENU]
    return result


def get_all_exercises_for_keyboard(client_id, train_name) -> str:
    """
    Получить тренировку
    """
    result = sql_query_scalar(
        """
            SELECT
                "Settings"
            FROM
                "Exercise"
            WHERE
                "ClientID"=%s::bigint AND
                "Name"=%s
        """, [client_id, train_name]
    )
    msg = ""
    for ex_name, ex_value in result.items():
        if len(list(filter(None, ex_value))) > 1:
            msg += f"{ex_name}: \n Веса - {','.join(i for i in ex_value[0])} \n Количество подходов - {','.join(i for i in ex_value[1])}\n\n"
        else:
            msg += f"{ex_name}: \nКоличество подходов - {','.join(i for i in ex_value[0])}\n\n"

    return msg
