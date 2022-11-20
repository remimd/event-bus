# How to use

## Define a bus

```python
from event_bus import Bus


bus = Bus()
```

## Subscribe a function to an event

> ***`event_name`** is the name of the event.*
> 
> *If the event doesn't exist, it's automatically generated.*
> 
> *Also works with an async function.*

```python
@bus.on_event.event_name
def some_function():
    # ...
```

## Trigger an event

> ***If you use a default handler**, you need an active event loop from `asyncio`.*

```python
bus.trigger("event_name")
```

## Custom handler

> *You can create a custom handler to modify the behavior of the trigger.*

```python
from event_bus import BusHandler, Event


class CustomHandler(BusHandler):
    @classmethod
    def on_trigger(cls, event: Event, *args, **kwargs):
        # ...
```

> *Define a bus with a custom handler.*

```python
from event_bus import Bus


bus = Bus(CustomHandler)
```
