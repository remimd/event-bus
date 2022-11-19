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

    """
    mocks
    """

    @staticmethod
    @contextmanager
    def mock_on_trigger(bus: Bus) -> ContextManager[Mock]:
        with patch.object(bus._handler, "on_trigger") as mock:
            yield mock
