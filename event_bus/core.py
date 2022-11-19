from __future__ import annotations

from dataclasses import dataclass, field
from inspect import isfunction
from typing import Any, Callable, Optional, Type, final

from .handlers import AsyncHandler, BusHandler


@final
@dataclass(frozen=True, slots=True)
class Event:
    subscribers: list[Callable] = field(default_factory=list, init=False)

    def add_subscriber(self, subscriber: Callable):
        if not isfunction(subscriber):
            raise TypeError("The subscriber isn't a function.")

        self.subscribers.append(subscriber)

    def subscribe(self, function: Callable) -> Callable:
        # It's a decorator
        self.add_subscriber(function)
        return function


@final
@dataclass(frozen=True, slots=True)
class OnEvent:
    bus: Bus

    def __getattr__(self, name: str):
        event = self.bus.get_or_create_event(name)
        return event.subscribe


@final
class Bus:
    on_event: OnEvent
    _events: dict[str, Event]
    _handler: Type[BusHandler]

    def __init__(self, handler: Type[BusHandler] = AsyncHandler):
        self._events = {}
        self._handler = handler
        self.on_event = OnEvent(self)

    def __setattr__(self, key: str, value: Any):
        class_name = self.__class__.__name__
        raise RuntimeError(f"'{class_name}' class cannot be updated.")

    def trigger(self, event_name: str, *args, **kwargs):
        event = self.check_event(event_name)
        self._handler.on_trigger(event, *args, **kwargs)

    def get_event(self, name: str) -> Optional[Event]:
        return self._events.get(name)

    def get_or_create_event(self, name: str) -> Event:
        if event := self.get_event(name):
            return event

        event = Event()
        self._events[name] = event
        return event

    def check_event(self, name: str) -> Event:
        if event := self.get_event(name):
            return event

        raise RuntimeError(f"Event '{name}' doesn't exist.")
