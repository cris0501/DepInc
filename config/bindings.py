from app.adapters.output.console_event_dispatcher import ConsoleEventDispatcher
from app.ports.input.flight_service_port import FlightServicePort
from app.ports.output.event_dispatcher import EventDispatcher
from app.use_cases.flight_service import FlightService

bindings = {
    FlightServicePort: FlightService,
    EventDispatcher: ConsoleEventDispatcher,
}
