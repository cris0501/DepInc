from core.ports.output.repository import Repository
from core.ports.output.event_dispatcher import EventDispatcher
from adapters.output.sqlite_flight_repository import SQLiteFlightRepository
from adapters.output.console_event_dispatcher import ConsoleEventDispatcher

bindings = {
    Repository: SQLiteFlightRepository,
    EventDispatcher: ConsoleEventDispatcher,
}
