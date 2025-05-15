from app.ports.out.repository import Repository
from app.ports.out.event_dispatcher import EventDispatcher
from app.domain.models.flight import Flight

class FlightService():
    def __init__(self, repository: Repository, dispatcher: EventDispatcher):
        self.repository = repository
        self.dispatcher = dispatcher

    def register_flight(self, flight_id: str, destination: str):
        flight = Flight(flight_id, destination)
        self.repository.save(flight)
        self.dispatcher.dispatch("FlightRegistered", {"flight_id": flight_id, "destination": destination})

    def assign_pilot(self, flight_id: str, pilot_name: str):
        flight = self.repository.find_by_id(flight_id)
        if flight:
            flight.pilot = pilot_name
            self.repository.save(flight)
            self.dispatcher.dispatch("PilotAssigned", {"flight_id": flight_id, "pilot": pilot_name})