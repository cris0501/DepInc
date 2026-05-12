from core.ports.output.event_dispatcher import EventDispatcher

class ConsoleEventDispatcher(EventDispatcher):
    def dispatch(self, event: str, payload: dict):
        print(f"[EVENT] {event} -> {payload}")