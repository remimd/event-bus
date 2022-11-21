from contextlib import contextmanager
from typing import Any, ContextManager
from unittest.mock import Mock, patch

from event_bus import Bus, Event


class TestCaseMixin:
    """
    factories
    """

    @staticmethod
    def bus_factory() -> Bus:
        bus = Bus()
        bus.get_or_create_event("test_event")
        return bus

    @staticmethod
    def event_factory() -> Event:
        return Event()

    @staticmethod
    def event_with_subscribers_factory() -> Event:
        def some_function():
            pass

        async def some_async_function():
            pass

        event = Event()

        event.add_subscriber(some_function)
        event.add_subscriber(some_async_function)

        return event

    """
    mocks
    """

    @staticmethod
    @contextmanager
    def mock_on_trigger(bus: Bus, return_value: Any = None) -> ContextManager[Mock]:
        with patch.object(
            bus._handler,
            "on_trigger",
            return_value=return_value,
        ) as mock:
            yield mock
