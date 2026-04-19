from abc import ABC

from bot_app.domain.entities.exercise_entity import Exercise, ExerciseSettings


class IExerciseRepository(ABC):

    @staticmethod
    def read(exercise_id: int) -> Exercise:
        pass

    @staticmethod
    def create(exercise_name: str, settings: ExerciseSettings) -> int:
        pass

    @staticmethod
    def delete(exercise_id: int) -> None:
        pass

    @staticmethod
    def update_settings(new_settings: ExerciseSettings) -> None:
        pass
