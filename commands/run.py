from infrastructure.container import Container as App
from adapters.ent.cli_adapter import CLIAdapter

from app.use_cases.flight_service import FlightService

def execute():
    app = App()
    
    flight_service = app.resolve(FlightService)
    cli = CLIAdapter(flight_service)
    
    cli.run()