global_id = 534310929

TOKEN = "1083751838:AAG2uzNZMtbCcR3RmhNNCAG5Pd0lLSsID-E"
URL = "https://api.telegram.org/bot"
TEST_URL = "http://127.0.0.1/"
MAIN_MENU = "В главное меню"


class StartButtons:
    trains = "Тренировки"
    statistic = "Статистика"
    set_trains = "Настроить тренировки"
    buttons_array = [trains, statistic, set_trains]


class TrainSettingsButton:
    delete = "Удалить тренировку"
    create = "Создать тренировку"
    change = "Изменить тренировку"
    main_menu = MAIN_MENU
    buttons_array = [delete, create, change, MAIN_MENU]


class SetTrainSettingsButtons:
    change_exercise = "Изменить упражнение"
    rename_train = "Изменить название тренировки"
    add_exercise = "Добавить упражнение"
    back_to_trains = "Обратно к тренировкам"
    buttons_array = [change_exercise, rename_train, add_exercise, back_to_trains]

class TrainStatus:
    CHANGE_TRAIN = 1
    DELETE_TRAIN = 2
    CREATE_TRAIN = 3
    RENAME_TRAIN = 4
    CREATE_EXERCISE = 5
    status_array = [CREATE_TRAIN, DELETE_TRAIN, CHANGE_TRAIN, RENAME_TRAIN, CREATE_EXERCISE]


# Пока просто захордкодим данные, чтобы не лехть
Train = "Треня 1"
Train2 = "Треня 2"
Train3 = "Треня 3"
TRAIN = {
    Train: '0.25',
    Train2: '0.25',
    Train3: '0.25',
    MAIN_MENU: '0.25'
}

exercise1 = "Упражнение 1"
exercise2 = "Упражнение 2"
exercise3 = "Упражнение 3"
back_to_trains = "К тренировкам"

EXERCISE = {
    exercise1: '0.25',
    exercise2: '0.25',
    exercise3: '0.25',
    back_to_trains: '0.25'
}
