import asyncio
import functools
from concurrent.futures import ThreadPoolExecutor
from inspect import iscoroutinefunction
from typing import Any, Awaitable, Callable


def to_awaitable(function: Callable, *args, **kwargs) -> Awaitable:
    if iscoroutinefunction(function):
        return function(*args, **kwargs)

    return run_in_thread(function, *args, **kwargs)


async def run_in_thread(function: Callable, *args, **kwargs) -> Any:
    loop = asyncio.get_running_loop()
    function = functools.partial(function, *args, **kwargs)

    with ThreadPoolExecutor() as executor:
        return await loop.run_in_executor(executor, function)
