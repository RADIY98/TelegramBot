from ...domain.buttons.buttons_val_obj import Button

class TrainMapper:
    handler = {

        Button.TRAINS: "Тренировки",
        Button.STATISTIC: "Статистика",
        Button.SET_TRAINS: "Настроить тренировки",

        Button.CHANGE_EXERCISE: "Изменить упражнение",
        Button.CHANGE_TRAIN_NAME: "Изменить название тренировки",
        Button.ADD_EXERCISE: "Добавить упражнение",
        Button.BACK_TO_TRAIN: "Обратно к тренировкам",

        Button.DELETE_EXERCISE: "Удалить упражнение",
        Button.RENAME_EXERCISE: "Переименовать упражнение",
        Button.CHANGE_SETTINGS_EXERCISE: "Изменить настройки упражнения",
        Button.BACK_TO_EXERCISE: "К упражнениям",

        Button.DELETE_TRAIN: "Удалить тренировку",
        Button.CREATE_TRAIN: "Создать тренировку",
        Button.CHANGE_TRAIN: "Изменить тренировку",
    }