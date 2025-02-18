from . import Operation
from ..database.insert import insert_exercise
from ..database.update import update_client_status, update_client_selected_entity
from ..database.delete import delete_exercise
from ..database.select import exercise_by_train, get_client_selected_entity, is_exercise
from ..base_names import TrainStatus, SetTrainSettingsButtons, ExerciseStatus, SetExerciseSettingsButtons

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
        selected_entity = get_client_selected_entity(self.client_id)

        if is_exercise(selected_entity):
            pass
        else:
            update_client_selected_entity(self.client_id, msg)
            text_msg = f'Выбранно упражнение - "{msg}"'
            keyboard = SetExerciseSettingsButtons.buttons_array

        return text_msg, keyboard
