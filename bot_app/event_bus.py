from typing import Dict, List, Type


class InMemoryEventBus
    """
    Простая in-memory реализация шины событий.
    Для продакшена нужна устойчивая к сбоям реализация.
    """

    def __init__(self):
        self._subscriptions = []

    def process(self):
        for event in self._subscriptions:
            event.handle()