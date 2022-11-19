from __future__ import annotations

import asyncio
import functools
from concurrent.futures import ThreadPoolExecutor
from inspect import iscoroutinefunction
from typing import Any, Awaitable, Callable, TYPE_CHECKING

from .abstract_handler import BusHandler

if TYPE_CHECKING:
    from event_bus import Event


class AsyncHandler(BusHandler):
    @classmethod
    def on_trigger(cls, event: Event, *args, **kwargs):
        awaitables = cls._prepare(event.subscribers)
        job = asyncio.gather(*awaitables)
        asyncio.ensure_future(job)

    @classmethod
    def _prepare(
        cls, subscribers: list[Callable], *args, **kwargs
    ) -> tuple[Awaitable, ...]:
        return tuple(
            cls._to_awaitable(subscriber, *args, **kwargs) for subscriber in subscribers
        )

    @classmethod
    def _to_awaitable(cls, function: Callable, *args, **kwargs) -> Awaitable:
        if iscoroutinefunction(function):
            return function(*args, **kwargs)

        return cls._run_in_thread(function, *args, **kwargs)

    @staticmethod
    async def _run_in_thread(function: Callable, *args, **kwargs) -> Any:
        loop = asyncio.get_running_loop()
        function = functools.partial(function, *args, **kwargs)

        with ThreadPoolExecutor() as executor:
            return await loop.run_in_executor(executor, function)
