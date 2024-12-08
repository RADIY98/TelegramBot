global_id = 534310929

TOKEN = "1083751838:AAG2uzNZMtbCcR3RmhNNCAG5Pd0lLSsID-E"
URL = "https://api.telegram.org/bot"
TEST_URL = "http://127.0.0.1/"
MAIN_MENU = "В главное меню"


class StartButtons:
    trains = "Тренировки"
    statistic = "Статистика"
    buttons_array = [trains, statistic]


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
