class Flight:
    def __init__(self, flight_id: str, destination: str, pilot: str = None):
        self.flight_id = flight_id
        self.destination = destination
        self.pilot = pilot