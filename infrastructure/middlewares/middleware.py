from abc import ABC, abstractmethod

class Middleware (ABC):
    @abstractmethod
    def execute (self, ctx: dict) -> bool:
        pass