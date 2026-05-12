from core.ports.output.repository import Repository
from core.ports.output.event_dispatcher import EventDispatcher
from adapters.output.memory_flight_repository import MemoryFlightRepository
from adapters.output.console_event_dispatcher import ConsoleEventDispatcher

bindings = {
    Repository: MemoryFlightRepository,
    EventDispatcher: ConsoleEventDispatcher,
}
