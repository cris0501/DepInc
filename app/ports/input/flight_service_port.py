from abc import ABC, abstractmethod


class FlightServicePort(ABC):
    @abstractmethod
    def register_flight(self, flight_id: str, destination: str): ...

    @abstractmethod
    def assign_pilot(self, flight_id: str, pilot_name: str): ...
