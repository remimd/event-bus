import pytest

from event_bus.core import Event


class TestEvent:
    @staticmethod
    def event_factory():
        return Event()

    @staticmethod
    def some_function():
        pass

    @staticmethod
    async def some_async_function():
        pass

    """ add_subscriber """

    def test_add_subscriber_with_not_function_raise_type_error(self):
        event = self.event_factory()
        with pytest.raises(TypeError, match="The subscriber isn't a function."):
            event.add_subscriber("not a function")

    def test_add_subscriber_with_async_function_return_none(self):
        event = self.event_factory()
        assert len(event._subscribers) == 0
        assert event.add_subscriber(self.some_async_function) is None
        assert len(event._subscribers) == 1

    def test_add_subscriber_with_success_return_none(self):
        event = self.event_factory()
        assert len(event._subscribers) == 0
        assert event.add_subscriber(self.some_function) is None
        assert len(event._subscribers) == 1


class TestBus:
    pass


class TestOnEvent:
    pass
