from app.ports.out.event_dispatcher import EventDispatcher

class ConsoleEventDispatcher(EventDispatcher):
    def dispatch(self, event: str, payload: dict):
        print(f"[EVENT] {event} -> {payload}")