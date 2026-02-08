from typing import List, Type
from .domain.events import Event

class InMemoryEventBus:
    """
    Простая in-memory реализация шины событий.
    Для продакшена нужна устойчивая к сбоям реализация.
    """

    def __init__(self):
        self._subscriptions: List[Type[Event]] = []

    def process(self):
        for event in self._subscriptions:
            event.handle()
