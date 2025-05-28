from typing import List

from requests import Response


class Trains:
    def __init__(self, train_name: str):
        self.train_name: str = train_name
        self.exercises: List[Exercise] = []

    def save_exercise(self, exercise):
        self.exercises.append(exercise)

    def create_json(self):
        exercises: dict = self.__compact_exercises()
        return {self.train_name: exercises}

    def __compact_exercises(self):
        result = {}
        for exercise in self.exercises:
            result.update(exercise.create_json())

        return result


class Exercise:
    def __init__(self, exercise_name, exercise_weight):
        self.exercise_name = exercise_name
        self.exercise_number = None
        self.exercise_weight = exercise_weight

    def set_numbers(self, exercise_numbers):
        self.exercise_number = exercise_numbers

    def create_json(self):
        return {self.exercise_name: [self.exercise_weight, self.exercise_number]}
