import time
from depinc.adapter import Adapter
from app.ports.input.flight_service_port import FlightServicePort


class TestAdapter(Adapter):
    def run(self):
        flight_service = self._app.resolve(FlightServicePort)
        counter = 0
        while True:
            print(f"[TestAdapter] tick {counter}")
            counter += 1
            time.sleep(10)
