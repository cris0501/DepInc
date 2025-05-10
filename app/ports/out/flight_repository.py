from abc import ABC, abstractmethod

class FlightRepository(ABC):
    @abstractmethod
    def save(self, flight): pass

    @abstractmethod
    def find_by_id(self, flight_id: str): pass