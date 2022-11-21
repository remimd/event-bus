from __future__ import annotations

from dataclasses import dataclass, field
from functools import wraps
from inspect import isfunction
from typing import Any, Callable, Final, Optional, TYPE_CHECKING, final

from .exceptions import EventDoesNotExist
from .handlers import AsyncHandler

if TYPE_CHECKING:
    from .typing import (
        BusHandlerType,
        Events,
        Subscriber,
        Subscribers,
    )


@final
@dataclass(frozen=True, slots=True)
class Event:
    subscribers: Subscribers = field(default_factory=list, init=False)

    def add_subscriber(self, subscriber: Subscriber):
        if not isfunction(subscriber):
            raise TypeError("The subscriber isn't a function.")

        self.subscribers.append(subscriber)

    def subscribe(self, subscriber: Subscriber) -> Subscriber:
        self.add_subscriber(subscriber)

        @wraps(subscriber)
        def wrapper(*args, **kwargs):
            return subscriber(*args, **kwargs)  # pragma: no cover

        return wrapper


@final
@dataclass(frozen=True, slots=True)
class OnEvent:
    bus: Bus

    def __getattr__(self, name: str) -> Callable:
        event = self.bus.get_or_create_event(name)
        return event.subscribe


@final
class Bus:
    __slots__ = "_events", "_handler", "_on_event"

    _events: Final[Events]
    _handler: Final[BusHandlerType]
    _on_event: Final[OnEvent]

    def __init__(self, handler: BusHandlerType = AsyncHandler):
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

        raise EventDoesNotExist(name)
