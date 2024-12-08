from typing import List

from requests import Response


def parse_file(train_file: Response):
        """
        Парсим файл на тренировки и упражнения
        """
        final_train_dict = {}
        train, exercise = None, None
        for file_line in train_file.iter_lines(decode_unicode=True):
            file_line = file_line.strip(";")
            parsed_line = file_line.split(";")
            if file_line:
                if file_line.isalpha():
                    if train is not None:
                        final_train_dict.update(train.create_json())
                    train = Trains(parsed_line[0])
                elif file_line[0].isalpha():
                    if exercise is not None:
                        train.save_exercise(exercise)
                    exercise = Exercise(parsed_line[0], parsed_line[1:])
                elif file_line[0].isdigit():
                    exercise.set_numbers(parsed_line)
            else:
                if exercise is not None:
                    train.save_exercise(exercise)
                exercise = None

        final_train_dict.update(train.create_json())
        return final_train_dict


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
