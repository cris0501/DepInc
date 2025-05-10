from abc import ABC, abstractmethod

class FlightCommand(ABC):
    @abstractmethod
    def register_flight(self, flight_id: str, destination: str): pass

    @abstractmethod
    def assign_pilot(self, flight_id: str, pilot_name: str): pass