global_id = 534311172

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
    CHANGE = 1
    DELETE = 2
    CREATE = 3
    RENAME = 4
    status_array = [CREATE, DELETE, CHANGE, RENAME]

class ExerciseStatus:
    CREATE = 5
    status_array = [CREATE]


class AllStatus:
    status_array = TrainStatus.status_array + ExerciseStatus.status_array