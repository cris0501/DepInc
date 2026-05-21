from app.ports.input.flight_service_port import FlightServicePort


class CLIAdapter:
    def __init__(self, flight_service: FlightServicePort):
        self.flight_service = flight_service

    def run(self):
        while True:
            print("1. Register Flight")
            print("2. Assign Pilot")
            option = input("Option: ")
            if option == "1":
                flight_id = input("Flight ID: ")
                destination = input("Destination: ")
                self.flight_service.register_flight(flight_id, destination)
            elif option == "2":
                flight_id = input("Flight ID: ")
                pilot = input("Pilot Name: ")
                self.flight_service.assign_pilot(flight_id, pilot)
