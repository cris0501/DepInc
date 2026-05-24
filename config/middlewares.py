from app.ports.input.flight_service_port import FlightServicePort
from app.middlewares import AuthMiddleware, ExistsMiddleware, LoggerMiddleware

middlewares = {
    FlightServicePort: {
        "register_flight": [AuthMiddleware, LoggerMiddleware],
        "assign_pilot":    [ExistsMiddleware],
    }
}
