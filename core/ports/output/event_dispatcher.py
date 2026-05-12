from abc import ABC, abstractmethod

class EventDispatcher(ABC):
    @abstractmethod
    def dispatch(self, event: str, payload: dict): pass