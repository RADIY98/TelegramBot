from typing import Optional, List
from dataclasses import dataclass, fields

import json


@dataclass
class KeyboardButton:
    text: str
    icon_custom_emoji_id: Optional[str] =None

    def to_telegram(self) -> dict:
        return {field.name: getattr(self, field.name) for field in fields(self) if getattr(self, field.name) is not None}

@dataclass
class ReplyKeyboardMarkup:
    items: List[List[KeyboardButton]]

    def to_telegram(self):
        result = []
        if not self.items or all(len(row) for row in self.items):
            raise Exception("No buttons in keyboard")

        for row in self.items:
            result.append([[button.to_telegram() for button in row]])

        return json.dumps({"keyboard": result})
