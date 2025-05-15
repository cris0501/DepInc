from app.use_cases.flight_service import FlightService
from adapters.out.memory_flight_repository import MemoryFlightRepository
from adapters.out.console_event_dispatcher import ConsoleEventDispatcher
from app.ports.out.repository import Repository
from app.ports.out.event_dispatcher import EventDispatcher

providers = {
        FlightService: {
            'imp': FlightService,
            'path': 'app.use_cases.flight_service',
        },
        Repository: {
            'imp': MemoryFlightRepository,
            'path': 'adapters.out.memory_flight_repository',
        },
        EventDispatcher: {
            'imp': ConsoleEventDispatcher,
            'path': 'adapters.out.console_event_dispatcher',
        },
}