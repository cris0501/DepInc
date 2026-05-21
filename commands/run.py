from depinc import App
from app.adapters.input.cli_adapter import CLIAdapter
from app.use_cases.flight_service import FlightService


def execute():
    app = App()
    flight_service = app.resolve(FlightService)
    cli = CLIAdapter(flight_service)
    cli.run()
