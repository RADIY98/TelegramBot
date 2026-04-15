from dataclasses import dataclass
from typing import List


@dataclass
class Weight:
    value: int

    def __post_init__(self):
        if self.value <= 0:
            raise ValueError("Not acceptable value")


@dataclass
class Reps:
    value: int

    def __post_init__(self):
        if self.value <= 0:
            raise ValueError("Not acceptable value")
        elif isinstance(self.value, float):
            raise ValueError("Value can`t take float value ")


@dataclass
class Sets:
    value: int

    def __post_init__(self):
        if self.value <= 0:
            raise ValueError("Not acceptable value")
        elif isinstance(self.value, float):
            raise ValueError("Value can`t take float value ")


@dataclass
class ExerciseSettings:
     weight: Weight
     reps: Reps
     sets: Sets


@dataclass
class Exercise:
    exercise_id: int
    name: str
    train_id: int
    exercise_settings: List[ExerciseSettings]
