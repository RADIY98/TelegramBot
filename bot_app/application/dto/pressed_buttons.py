from dataclasses import dataclass
from typing import Optional


@dataclass
class PressedButton:
    user_id: int
    button_id: int
    entity_id: Optional[int]
    text: str