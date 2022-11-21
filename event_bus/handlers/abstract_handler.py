from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING

from event_bus.common import StaticClass

if TYPE_CHECKING:
    from event_bus import Event


class BusHandler(StaticClass, ABC):
    @classmethod
    @abstractmethod
    def on_trigger(cls, event: Event, *args, **kwargs) -> Any:
        raise NotImplementedError
