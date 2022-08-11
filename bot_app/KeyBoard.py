class KeyboardButton:
    def __init__(self, text):
        self.text = text


class KeyBoard:
    """
    Класс отвечающий за отображение клавиатуры
    """

    def __init__(self):
        self.button_dict = {"Начать тренировку": '0.25',
                            "Изменить тренировку": '0.25',
                            "Фактическое кол-во подходов": '0.25'}

    def get_keyboard(self):
        """
        Получить объект клавиатуры

        :return:
        """

        return [[KeyboardButton(text=key).text] for key, _ in self.button_dict.items()]
