from app.ports.input.flight_service_port import FlightServicePort
from app.ports.output.repository import Repository
from app.ports.output.event_dispatcher import EventDispatcher
from app.adapters.output.sqlite_repository import SQLiteRepository
from app.adapters.output.console_event_dispatcher import ConsoleEventDispatcher
from app.use_cases.flight_service import FlightService

bindings = {
    FlightServicePort: FlightService,
    Repository:        SQLiteRepository,
    EventDispatcher:   ConsoleEventDispatcher,
}

