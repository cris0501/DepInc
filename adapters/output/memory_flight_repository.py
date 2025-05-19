from core.ports.output.repository import Repository
from infrastructure.decorators import inyectable

@inyectable(key=Repository, variant='memory')
class MemoryFlightRepository(Repository):
    def __init__(self):
        self.flights = {}

    def save(self, flight):
        self.flights[flight.id] = flight

    def find_by_id(self, _id: str):
        return self.flights.get(_id)