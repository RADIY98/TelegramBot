from typing import Optional, List
from dataclasses import dataclass, fields

import json


@dataclass
class InlineKeyboardButton:
    text: str
    callback_data: str
    icon_custom_emoji_id: Optional[str] = None

    def to_telegram(self) -> dict:
        return {field.name: getattr(self, field.name) for field in fields(self) if getattr(self, field.name) is not None}


@dataclass
class InlineKeyboardMarkup:
    items: List[List[InlineKeyboardButton]]

    def to_telegram(self):
        result = []
        if not self.items or all(len(row) for row in self.items):
            raise Exception("No buttons in keyboard")

        for row in self.items:
            result.append([[button.to_telegram() for button in row]])

        return json.dumps({"keyboard": result})

