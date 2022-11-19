import asyncio
from asyncio import AbstractEventLoop
from typing import Generator

import pytest


@pytest.fixture(scope="module")
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()
