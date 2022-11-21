class EventDoesNotExist(Exception):
    base_message = "Event '{name}' doesn't exist."

    def __init__(self, event_name: str):
        cls = self.__class__
        message = cls.base_message.format(name=event_name)
        super().__init__(message)
