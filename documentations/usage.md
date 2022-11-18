# Usage

## Subscribe a function to an event

> ***`event_name`** is the name of the event.*
> 
> *If the event doesn't exist, it's automatically generated.*
> 
> *Also works with an async function.*

```python
from event_bus import on_event


@on_event.event_name
def some_function():
    # ...
```

## Trigger an event

> ***Prerequisite:** requires an active event loop from `asyncio`.*

```python
import event_bus


def some_function():
    # ...
    event_bus.trigger("event_name")
    # ...
```
