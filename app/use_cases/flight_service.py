from app.ports.input.flight_service_port import FlightServicePort
from app.ports.output.repository import Repository
from app.ports.output.event_dispatcher import EventDispatcher
from app.domain.flight import Flight


class FlightService(FlightServicePort):
    # Use _bindings to override dependency map
    #_bindings = {Repository: SQLiteRepository}

    def __init__(self, repository: Repository, dispatcher: EventDispatcher):
        self.repository = repository
        self.dispatcher = dispatcher

    def register_flight(self, flight_id: str, destination: str):
        flight = Flight(flight_id, destination)
        self.repository.save(flight)
        self.dispatcher.dispatch("FlightRegistered", {"flight_id": flight_id, "destination": destination})

    def assign_pilot(self, flight_id: str, pilot_name: str):
        flight = self.repository.find_by_id(Flight, flight_id)
        if flight:
            flight.pilot = pilot_name
            self.repository.save(flight)
            self.dispatcher.dispatch("PilotAssigned", {"flight_id": flight_id, "pilot": pilot_name})
