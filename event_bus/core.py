import asyncio
from dataclasses import dataclass, field
from inspect import isfunction
from typing import Awaitable, Callable, Optional, final

from .common import StaticClass
from .tools.asynchronous import to_awaitable


@final
@dataclass(repr=False, frozen=True, slots=True)
class Event:
    _subscribers: list[Callable] = field(default_factory=list, init=False)

    def add_subscriber(self, subscriber: Callable):
        if not isfunction(subscriber):
            raise TypeError("The subscriber isn't a function.")

        self._subscribers.append(subscriber)

    def subscribe(self, function: Callable) -> Callable:
        # It's a decorator
        self.add_subscriber(function)
        return function

    def build_awaitables(self, *args, **kwargs) -> tuple[Awaitable, ...]:
        return tuple(
            to_awaitable(subscriber, *args, **kwargs)
            for subscriber in self._subscribers
        )


@final
class Bus(StaticClass):
    _events: dict[str, Event] = {}

    @classmethod
    def trigger(cls, event_name: str, *args, **kwargs):
        event = cls.check_event(event_name)
        awaitables = event.build_awaitables(*args, **kwargs)
        job = asyncio.gather(*awaitables)
        asyncio.ensure_future(job)

    @classmethod
    def get_event(cls, name: str) -> Optional[Event]:
        return cls._events.get(name)

    @classmethod
    def get_or_create_event(cls, name: str) -> Event:
        if event := cls.get_event(name):
            return event

        event = Event()
        cls._events[name] = event
        return event

    @classmethod
    def check_event(cls, name: str) -> Event:
        if event := cls.get_event(name):
            return event

        raise RuntimeError(f"Event '{name}' doesn't exist.")


@final
class OnEvent:
    def __getattr__(self, name: str):
        event = Bus.get_or_create_event(name)
        return event.subscribe


on_event = OnEvent()
trigger = Bus.trigger
