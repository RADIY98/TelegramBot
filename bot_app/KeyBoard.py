class KeyboardButton:
    def __init__(self, text):
        self.text = text


class KeyBoard:
    """
    Класс отвечающий за отображение клавиатуры
    """

    def __init__(self, buttons):
        self.button_dict = buttons

    def get_keyboard(self):
        """
        Получить объект клавиатуры

        :return:
        """

        return [[KeyboardButton(text=key).text] for key, _ in self.button_dict.items()]
