from app.use_cases.flight_service import FlightService
from adapters.out.memory_flight_repository import MemoryFlightRepository
from adapters.out.console_event_dispatcher import ConsoleEventDispatcher

class Container:
    def __init__(self):
        self.repository = MemoryFlightRepository()
        self.dispatcher = ConsoleEventDispatcher()
        self.flight_service = FlightService(self.repository, self.dispatcher)