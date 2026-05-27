from abc import ABC, abstractmethod


class Adapter(ABC):
    def __init__(self, container):
        self._app = container

    @abstractmethod
    def run(self):
        pass
