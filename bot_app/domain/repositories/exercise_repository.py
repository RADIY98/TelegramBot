from abc import ABC

from bot_app.domain.entities.exercise_entity import Exercise, ExerciseSettings


class IExerciseRepository(ABC):

    @staticmethod
    def read(exercise_id: int) -> Exercise:
        pass
