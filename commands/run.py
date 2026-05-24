from depinc import App
from app.adapters.input.cli_adapter import CLIAdapter
from app.use_cases.flight_service import FlightService
from app.adapters.output.memory_repository import MemoryRepository


def execute():
    app = App()
    flight_service = app.resolve(FlightService, MemoryRepository)
    cli = CLIAdapter(flight_service)
    cli.run()
