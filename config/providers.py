from app.use_cases.flight_service import FlightService
from adapters.out.memory_flight_repository import MemoryFlightRepository
from adapters.out.console_event_dispatcher import ConsoleEventDispatcher
from app.ports.out.flight_repository import FlightRepository
from app.ports.out.event_dispatcher import EventDispatcher

providers = {
        FlightService: FlightService,
        FlightRepository: MemoryFlightRepository,
        EventDispatcher: ConsoleEventDispatcher,
}