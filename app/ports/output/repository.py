from abc import ABC, abstractmethod


class Repository(ABC):
    @abstractmethod
    def save(self, entity):
        pass

    @abstractmethod
    def find_by_id(self, model_class, id_value):
        pass

    def _migrate(self, entity) -> None:
        ...