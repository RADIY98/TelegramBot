from dataclasses import dataclass

TOKEN = "1083751838:AAG2uzNZMtbCcR3RmhNNCAG5Pd0lLSsID-E"
URL = "https://api.telegram.org/bot"
TEST_URL = "http://127.0.0.1/"
GO_BACK = "Обратно"

@dataclass
class StartButtonsNames:
    start = "Начать тренировку"
    change = "Изменить тренировку"
    statistic = "Статистика"

@dataclass
class ExerciseButtonsNames:
    set_weight = "Установить вес"
    counts = "Количество подходов"
    end = "Закончить упражнение"

@dataclass
class ExerciseSettingsButtonsNames:
    exist_trains = "Существующие трнировки"
    delete_train = "Удалить тренировку"
    end = "Закончить упражнение"

START_KEYBOAD = {
    StartButtonsNames.start: '0.25',
    StartButtonsNames.change: '0.25',
    StartButtonsNames.statistic: '0.25'
}
START_TRAIN = {
    ExerciseButtonsNames.set_weight: '0.25',
    ExerciseButtonsNames.counts: '0.25',
    ExerciseButtonsNames.end: '0.25'
}

# Пока просто захордкодим данные, чтобы не лехть
Train = "Треня 1"
Train2 = "Треня 2"
Train3 = "Треня 3"
TRAIN = {
    Train: '0.25',
    Train2: '0.25',
    Train3: '0.25',
    GO_BACK: '0.25'
}

exercise1 = "Упражнение 1"
exercise2 = "Упражнение 2"
exercise3 = "Упражнение 3"
back = "В главное меню"

EXERCISE = {
    exercise1: '0.25',
    exercise2: '0.25',
    exercise3: '0.25',
    back: '0.25'
}
