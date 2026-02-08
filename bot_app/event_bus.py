from typing import List, Type, Dict
from .domain.events import client_events

class EventBus:
    """
    Простая in-memory реализация шины событий.
    Для продакшена нужна устойчивая к сбоям реализация.
    """

    def __init__(self):
        self._subscriptions = {
            client_events.ClientEventSelectedEntityChange: [],
            client_events.ClientEventStatusChange: []
        }

    def subscribe(self, event, handler):
        self._subscriptions[event] = handler

    def publish(self, event):
        event_type = type(event)
        if event_type in self._subscriptions:
            for handler in self._subscriptions.get(event_type):
                handler(event)

    def publish_many(self, *events):
        for event in events:
            self.publish(event)


