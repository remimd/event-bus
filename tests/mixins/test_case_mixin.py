import asyncio
import time
from contextlib import contextmanager
from typing import ContextManager
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
            time.sleep(1)

        async def some_async_function():
            await asyncio.sleep(1)

        event = Event()

        event.add_subscriber(some_function)
        event.add_subscriber(some_async_function)

        return event

    """
    mocks
    """

    @staticmethod
    @contextmanager
    def mock_on_trigger(bus: Bus) -> ContextManager[Mock]:
        with patch.object(bus._handler, "on_trigger", return_value=None) as mock:
            yield mock
