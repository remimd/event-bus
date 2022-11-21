from asyncio import Future

import pytest

from event_bus import AsyncHandler
from tests.mixins.test_case_mixin import TestCaseMixin


class TestAsyncHandler(TestCaseMixin):
    handler = AsyncHandler

    """
    __new__
    """

    def test_new_with_success_raise_runtime_error(self):
        with pytest.raises(
            RuntimeError,
            match=f"{self.handler.__name__} can't be instantiated.",
        ):
            self.handler()

    """
    on_trigger
    """

    async def test_on_trigger_with_success_return_future(self):
        event = self.event_with_subscribers_factory()
        future = self.handler.on_trigger(event)
        assert isinstance(future, Future)
        result = await future
        assert isinstance(result, list)

    """
    _run_in_thread
    """

    async def test_run_in_thread_with_success_return_any(self):
        def hello_world() -> str:
            return "Hello world!"

        expected = hello_world()
        actual = await self.handler._run_in_thread(hello_world)

        assert actual == expected
