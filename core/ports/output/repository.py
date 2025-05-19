from abc import ABC, abstractmethod
from infrastructure.decorators import inyectable

class Repository(ABC):
    @abstractmethod
    def save(self, entity):
        pass

    @abstractmethod
    def find_by_id(self, id_value):
        pass
