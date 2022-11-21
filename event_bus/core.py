from __future__ import annotations

from dataclasses import dataclass, field
from inspect import isfunction
from typing import Any, Callable, Optional, Type, final

from .handlers import AsyncHandler, BusHandler


Subscriber = Callable


@final
@dataclass(frozen=True, slots=True)
class Event:
    subscribers: list[Subscriber] = field(default_factory=list, init=False)

    def add_subscriber(self, subscriber: Subscriber):
        if not isfunction(subscriber):
            raise TypeError("The subscriber isn't a function.")

        self.subscribers.append(subscriber)

    def subscribe(self, subscriber: Subscriber) -> Subscriber:
        # It's a decorator
        self.add_subscriber(subscriber)
        return subscriber


@final
@dataclass(frozen=True, slots=True)
class OnEvent:
    bus: Bus

    def __getattr__(self, name: str) -> Callable:
        event = self.bus.get_or_create_event(name)
        return event.subscribe


@final
class Bus:
    _events: dict[str, Event]
    _handler: Type[BusHandler]
    _on_event: OnEvent

    def __init__(self, handler: Type[BusHandler] = AsyncHandler):
        self._events = {}
        self._handler = handler
        self._on_event = OnEvent(self)

    @property
    def on_event(self) -> OnEvent:
        return self._on_event  # pragma: no cover

    def trigger(self, event_name: str, *args, **kwargs) -> Any:
        event = self.check_event(event_name)
        return self._handler.on_trigger(event, *args, **kwargs)

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
