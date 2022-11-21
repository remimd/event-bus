from __future__ import annotations

import asyncio
import functools
from asyncio import Future
from concurrent.futures import ThreadPoolExecutor
from inspect import iscoroutinefunction
from typing import Any, Awaitable, TYPE_CHECKING

from .abstract_handler import BusHandler

if TYPE_CHECKING:
    from event_bus import Event, Subscriber


class AsyncHandler(BusHandler):
    @classmethod
    def on_trigger(cls, event: Event, *args, **kwargs) -> Future:
        awaitables = cls._prepare_subscribers(event.subscribers, *args, **kwargs)
        job = asyncio.gather(*awaitables)
        return asyncio.ensure_future(job)

    @classmethod
    def _prepare_subscribers(
        cls, subscribers: list[Subscriber], *args, **kwargs
    ) -> tuple[Awaitable, ...]:
        return tuple(
            cls._to_awaitable(subscriber, *args, **kwargs) for subscriber in subscribers
        )

    @classmethod
    def _to_awaitable(cls, subscriber: Subscriber, *args, **kwargs) -> Awaitable:
        if iscoroutinefunction(subscriber):
            return subscriber(*args, **kwargs)

        return cls._run_in_thread(subscriber, *args, **kwargs)

    @staticmethod
    async def _run_in_thread(subscriber: Subscriber, *args, **kwargs) -> Any:
        loop = asyncio.get_running_loop()
        subscriber = functools.partial(subscriber, *args, **kwargs)

        with ThreadPoolExecutor() as executor:
            return await loop.run_in_executor(executor, subscriber)
