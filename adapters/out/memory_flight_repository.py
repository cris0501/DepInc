from app.ports.out.flight_repository import FlightRepository

class MemoryFlightRepository(FlightRepository):
    def __init__(self):
        self.flights = {}

    def save(self, flight):
        self.flights[flight.flight_id] = flight

    def find_by_id(self, flight_id: str):
        return self.flights.get(flight_id)