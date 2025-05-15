from app.ports.out.repository import Repository

class MemoryFlightRepository(Repository):
    def __init__(self):
        self.flights = {}

    def save(self, flight):
        self.flights[flight.id] = flight

    def find_by_id(self, _id: str):
        return self.flights.get(_id)