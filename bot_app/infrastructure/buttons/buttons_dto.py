"""
Модуль для конвертации формата Телеграмма
"""
from bot_app.application.models.buttons import ButtonDef


class ButtonFormater:
    def from_inline_telegram(self, callback_data: str):
        """
        Смена формата на внутренний
        """
        button_id, text = callback_data.split(":")

        return ButtonDef(id=int(button_id), text=text)
