from typing import Callable, Type

from .core import Event
from .handlers import BusHandler


BusHandlerType = Type[BusHandler]
Events = dict[str, Event]
Subscriber = Callable
Subscribers = list[Subscriber]
