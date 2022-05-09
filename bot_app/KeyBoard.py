import enum


class InlineKeyboardButton():
    def __init__(self, text):
        self.text = text

    def get_keyboard_obj(self):
        return self.text


class InlineKeyboardMarkup():
    def __init__(self, button_array):
        self.button_array = button_array

    def get_keyboard_markup(self):
        return [self.button_array]


class KeyBoard():
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
        button_list = [InlineKeyboardButton(text=key).get_keyboard_obj() for key, _ in self.button_dict.items()]
        return InlineKeyboardMarkup(button_list).get_keyboard_markup()
