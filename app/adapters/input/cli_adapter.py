from depinc.adapter import Adapter
from depinc import context
from depinc.plugins.logger import logger
from app.ports.input.flight_service_port import FlightServicePort
from app.use_cases.flight_service import FlightService


class CLIAdapter(Adapter):
    def run(self):
        logger.debug(f"Contenedor: {context.container}")
        flight_service = context.container.resolve(FlightServicePort)
        while True:
            print("1. Register Flight")
            print("2. Assign Pilot")
            option = input("Option: ")
            if option == "1":
                flight_id = input("Flight ID: ")
                destination = input("Destination: ")
                flight_service.register_flight(flight_id, destination)
            elif option == "2":
                flight_id = input("Flight ID: ")
                pilot = input("Pilot Name: ")
                flight_service.assign_pilot(flight_id, pilot)
