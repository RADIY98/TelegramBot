"""
Модуль для описания объекта кнопки
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class ButtonDef:
    id: int
    text: str
    data: Optional[dict] = None