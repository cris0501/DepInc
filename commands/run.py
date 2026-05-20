from infrastructure import App
from adapters import CLIAdapter
from config.paths import paths

from core.use_cases.flight_service import FlightService
from adapters import *

def execute():
  
    app = App()
    
    flight_service = app.resolve(FlightService)
    cli = CLIAdapter(flight_service)
    
    cli.run()
