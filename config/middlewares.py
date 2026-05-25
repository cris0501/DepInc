from app.ports.input.flight_service_port import FlightServicePort
from app.middlewares import AuthMiddleware, ExistsMiddleware, LoggerMiddleware
from app.domain import Pilot

middlewares = {
    FlightServicePort: {
        "register_flight": [AuthMiddleware, LoggerMiddleware],
        "assign_pilot":    [ExistsMiddleware(Pilot)],
    }
}
