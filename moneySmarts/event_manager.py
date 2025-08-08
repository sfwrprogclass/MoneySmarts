class EventManager:
    """
    Centralized event manager for handling game and UI events using a publish/subscribe model.

    Attributes:
        _subscribers (dict): Dictionary mapping event types to lists of handler functions.
    """
    def __init__(self):
        """Initialize the EventManager with an empty subscriber dictionary."""
        self._subscribers = {}

    def subscribe(self, event_type, handler):
        """Subscribe a handler to a specific event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    def unsubscribe(self, event_type, handler):
        """Unsubscribe a handler from a specific event type."""
        if event_type in self._subscribers:
            self._subscribers[event_type].remove(handler)
            if not self._subscribers[event_type]:
                del self._subscribers[event_type]

    def publish(self, event_type, **kwargs):
        """Publish an event to all subscribed handlers, passing event data as kwargs."""
        if event_type in self._subscribers:
            for handler in self._subscribers[event_type]:
                handler(**kwargs)

# Singleton instance for global use
EventBus = EventManager()