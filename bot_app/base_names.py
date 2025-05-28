from dataclasses import dataclass


TOKEN = "1083751838:AAGQS1h7DIwe4xblTOIMnmCjUPcHRxtC6qE"
URL = "https://api.telegram.org/bot"
TEST_URL = "http://127.0.0.1/"

@dataclass
class DbUser:
    """
    Настройки пользователя для доступа к бд
    """
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
WELCOME_MESSAGE = (
    "Добро пожаловать. "
    "Данный бот предназначен для тренировок. "
    "Здесь вы можете расписать тренировки и упражнения к ним"
)
GOING_TO_DELETE = "Какую тренировку удаляем?"
GOING_TO_CHANGE = "Выберите из списка, что вы хотите изменить"

@dataclass
class StartButtons:
    """
    Стартовый набор кнопок
    """
    trains = "Тренировки"
    statistic = "Статистика"
    set_trains = "Настроить тренировки"
    buttons_array = [trains, statistic, set_trains]


@dataclass
class TrainSettingsButton:
    """
    Набор кнопок для изменения тренировок
    """
    delete = "Удалить тренировку"
    create = "Создать тренировку"
    change = "Изменить тренировку"
    main_menu = MAIN_MENU
    buttons_array = [delete, create, change, MAIN_MENU]


@dataclass
class SetTrainSettingsButtons:
    """
    Набор кнопок для изменения тренировок
    """
    change_exercise = "Изменить упражнение"
    rename_train = "Изменить название тренировки"
    add_exercise = "Добавить упражнение"
    back_to_trains = "Обратно к тренировкам"
    buttons_array = [change_exercise, rename_train, add_exercise, back_to_trains]


@dataclass
class SetExerciseSettingsButtons:
    """
    Набор кнопок для изменения упражнения
    """
    delete = "Удалить упражнение"
    rename = "Переименовать упражнение"
    change = "Изменить настройки упражнения"
    back = "К упражнениям"
    buttons_array = [delete, change, rename, back]


@dataclass
class TrainStatus:
    """
    Статусы тренировок
    """
    CHANGE = 1
    DELETE = 2
    CREATE = 3
    RENAME = 4
    status_array = [CREATE, DELETE, CHANGE, RENAME]


@dataclass
class ExerciseStatus:
    """
    Статусы упражнений
    """
    CREATE = 5
    DELETE = 6
    CHANGE = 7
    RENAME = 8
    UPDATE = 9
    status_array = [CREATE, RENAME, CHANGE, DELETE, UPDATE]


EXERCISE_READ_STATUS = 10
