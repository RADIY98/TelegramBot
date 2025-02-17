from . import Operation
from ..database.insert import insert_exercise
from ..database.update import update_client_status
from ..database.delete import delete_exercise
from ..database.select import exercise_by_train
from ..base_names import TrainStatus, SetTrainSettingsButtons, ExerciseStatus

class ExerciseOperation(Operation):
    """
    Операции над упражнеениями
    """
    def __init__(self, client_id: int):
        """
        Инициализация класса
        """
        self.client_id = client_id

    def execute_method_by_status(self, status: int, msg: str) -> (str, list):
        """
        Сопоставим статусу нужный метод
        """
        operation_by_status = {
            ExerciseStatus.CHANGE: self.change,
            ExerciseStatus.DELETE: self.delete,
            ExerciseStatus.CREATE: self.create,
            ExerciseStatus.RENAME: self.rename,
        }
        method = operation_by_status.get(status)

        return method(msg)

    def create(self, msg: str) -> (str, list):
        """
        Добавить упражнение
        """
        insert_exercise(self.client_id, msg)
        update_client_status(self.client_id, TrainStatus.CHANGE)

        return f'Упражнение - "{msg}" успешно добавлено', SetTrainSettingsButtons.buttons_array

    def delete(self, msg: str) -> (str, list):
        """
        Удаление упражнения
        """
        delete_exercise(self.client_id)
        update_client_status(self.client_id, ExerciseStatus.CHANGE)
        keyboard = exercise_by_train(self.client_id)

        return keyboard

    def change(self, msg: str) -> (str, list):
        """
        Изменить упражнение
        """
        text_msg = ""
        keyboard = []
        if msg == SetTrainSettingsButtons.add_exercise:
            text_msg = "Напишите название упражнения"
            update_client_status(self.client_id, ExerciseStatus.CREATE)
            keyboard = SetTrainSettingsButtons.buttons_array

        return text_msg, keyboard
