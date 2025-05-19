from abc import ABC, abstractmethod
from infrastructure.decorators import inyectable

class EventDispatcher(ABC):
    @abstractmethod
    def dispatch(self, event: str, payload: dict): pass