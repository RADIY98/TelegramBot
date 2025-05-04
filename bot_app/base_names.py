global_id = 534311410

TOKEN = "1083751838:AAGYO7eAqtntiN9rLlG2vPI9t2V2Asv2uus"
URL = "https://api.telegram.org/bot"
TEST_URL = "http://127.0.0.1/"

class DbUser:
    DB_ROLE = "admin"
    ADMIN_PASSWORD = "Trepol845"

DB_PASSWORD = "k02bkhBM"

MAIN_MENU = "В главное меню"
BACK_TO_MAIN_MENU = "Вы в главном меню"
NO_EXERCISE = "Давайте добавим упражнение"
LETS_SET_TRAIN_FROM_LIST = "Давайте настроим тренировки\nВыберите тренировку из списка"
ENTER_TRAIN_NAME = "Введите название тренировки"
CHOOSE_TRAIN_FROM_LIST = "Выберите тренировку из списка"
LETS_CREATE_TRAIN = "Давайте добавим тренировку"
SELECTED_TRAIN = 'Вы выбрали тренировку - "{}"'
UPDATED_EXERCISE = 'Настройки упражнения успешно сохранены\n'

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

class SetExerciseSettingsButtons:
    delete = "Удалить упражнение"
    rename = "Переименовать упражнение"
    change = "Изменить настройки упражнения"
    back = "К упражнениям"
    buttons_array = [delete, change, rename, back]


class TrainStatus:
    CHANGE = 1
    DELETE = 2
    CREATE = 3
    RENAME = 4
    status_array = [CREATE, DELETE, CHANGE, RENAME]

class ExerciseStatus:
    CREATE = 5
    DELETE = 6
    CHANGE = 7
    RENAME = 8
    UPDATE = 9
    status_array = [CREATE, RENAME, CHANGE, DELETE, UPDATE]


EXERCISE_READ_STATUS = 10

class AllStatus:
    status_array = TrainStatus.status_array + ExerciseStatus.status_array