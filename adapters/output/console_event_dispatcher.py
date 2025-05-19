from core.ports.output.event_dispatcher import EventDispatcher
from infrastructure.decorators import inyectable

@inyectable(key=EventDispatcher)
class ConsoleEventDispatcher(EventDispatcher):
    def dispatch(self, event: str, payload: dict):
        print(f"[EVENT] {event} -> {payload}")