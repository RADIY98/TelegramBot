from typing import List


class KeyboardButton:
    def __init__(self, text):
        self.text = text


class KeyBoard:
    """
    Класс отвечающий за отображение клавиатуры
    """

    def __init__(self, buttons: List[str]):
        self.buttons: List[str] = buttons

    def get_keyboard(self):
        """
        Получить объект клавиатуры

        :return:
        """

        return [[KeyboardButton(text=key).text] for key in self.buttons]


class InlineKeyboardButton:
    def __init__(self, text):
        self.text = text


class InlineKeyBoard:
    """
    Класс, отвечающий за inline-клавиатуру
    """
    def __init__(self, buttons):
        self.buttons = buttons

    def get_keyboard(self):
        return [[InlineKeyboardButton(text=key).text] for key in self.buttons]
