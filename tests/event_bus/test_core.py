import pytest

from tests.mixins.test_mixin import TestCaseMixin


class TestEvent(TestCaseMixin):
    """
    add_subscriber
    """

    def test_add_subscriber_with_not_function_raise_type_error(self):
        event = self.event_factory()
        with pytest.raises(TypeError, match="The subscriber isn't a function."):
            event.add_subscriber("not a function")

    def test_add_subscriber_with_async_function_return_none(self):
        event = self.event_factory()
        assert len(event.subscribers) == 0

        async def async_function():
            pass

        assert event.add_subscriber(async_function) is None
        assert len(event.subscribers) == 1

    def test_add_subscriber_with_success_return_none(self):
        event = self.event_factory()
        assert len(event.subscribers) == 0

        def function():
            pass

        assert event.add_subscriber(function) is None
        assert len(event.subscribers) == 1

    """
    subscribe
    """

    def test_subscribe_with_success_return_function(self):
        event = self.event_factory()
        assert len(event.subscribers) == 0

        @event.subscribe
        def function():
            pass

        assert len(event.subscribers) == 1


class TestOnEvent(TestCaseMixin):
    """
    getattr
    """

    def test_getattr_with_event_exist_return_function(self):
        bus = self.bus_factory()
        event_name = "test_event"
        assert event_name in bus._events.keys()

        event = bus._events[event_name]
        assert len(event.subscribers) == 0

        @bus.on_event.test_event
        def function():
            pass

        assert len(event.subscribers) == 1

    def test_getattr_with_success_return_function(self):
        bus = self.bus_factory()
        event_name = "some_event"
        assert event_name not in bus._events.keys()

        @bus.on_event.some_event
        def function():
            pass

        event = bus._events[event_name]
        assert len(event.subscribers) == 1
        assert event_name in bus._events.keys()


class TestBus(TestCaseMixin):
    """
    trigger
    """

    def test_trigger_with_event_does_not_exist_raise_runtime_error(self):
        bus = self.bus_factory()
        event_name = "event_does_not_exist"
        with pytest.raises(RuntimeError, match=f"Event '{event_name}' doesn't exist."):
            bus.trigger(event_name)

    def test_trigger_with_success_return_none(self):
        bus = self.bus_factory()
        with self.mock_on_trigger(bus) as mock:
            assert bus.trigger("test_event") is None

        assert mock.call_count == 1
