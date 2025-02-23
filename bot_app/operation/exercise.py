from . import Operation
from ..database.insert import insert_exercise
from ..database.update import update_client_status, update_client_selected_entity, update_selected_entity_by_id, rename_exercise
from ..database.delete import delete_exercise
from ..database.select import get_client_selected_entity, is_exercise, all_exercise_for_keyboard, read_exercise
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
        exercise_name, train_id = delete_exercise(self.client_id)
        update_selected_entity_by_id(exercise_name, train_id)
        update_client_status(self.client_id, ExerciseStatus.CHANGE)

        return f"Упражнение {exercise_name} успешно удалено", all_exercise_for_keyboard(train_id)

    def rename(self, msg: str) -> (str, list):
        """
        Переименовать упражнение
        """
        update_client_status(self.client_id, ExerciseStatus.CHANGE)
        selected_entity = get_client_selected_entity(self.client_id)

        rename_exercise(msg, selected_entity)

        return "Упражнение переименовано", SetExerciseSettingsButtons.buttons_array

    def change(self, msg: str) -> (str, list):
        """
        Изменить упражнение
        """
        text_msg = ""
        keyboard = []
        selected_entity = get_client_selected_entity(self.client_id)

        if is_exercise(selected_entity):
            if msg == SetExerciseSettingsButtons.delete:
                text_msg, keyboard = ExerciseOperation(self.client_id).delete(msg)
            elif msg == SetExerciseSettingsButtons.rename:
                update_client_status(self.client_id, ExerciseStatus.RENAME)
                text_msg = "Напишите новое название для упражнения"
                keyboard = SetExerciseSettingsButtons.buttons_array
            elif msg == SetExerciseSettingsButtons.back:
                exercise: dict = read_exercise(selected_entity)
                train_id: int = exercise.get("TrainId")
                update_selected_entity_by_id(self.client_id, train_id)
                text_msg, keyboard = "Вернулись к упражнениям", all_exercise_for_keyboard(train_id)

        else:
            update_client_selected_entity(self.client_id, msg)
            text_msg = f'Выбранно упражнение - "{msg}"'
            keyboard = SetExerciseSettingsButtons.buttons_array

        return text_msg, keyboard
