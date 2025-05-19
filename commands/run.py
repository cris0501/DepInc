from infrastructure import App
from adapters import CLIAdapter, ConsoleEventDispatcher, MemoryFlightRepository, SQLiteFlightRepository
from config.paths import paths

from core.use_cases.flight_service import FlightService
from adapters import *

def execute():
  
    app = App()
    
    flight_service = app.resolve(FlightService, {'repository': 'memory'})
    cli = CLIAdapter(flight_service)
    
    cli.run()