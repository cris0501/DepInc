import time
from depinc import context
from depinc.adapter import Adapter
from depinc.plugins.logger import logger
from app.ports.input.flight_service_port import FlightServicePort


class TestAdapter(Adapter):
    def run(self):
        flight_service = context.container.resolve(FlightServicePort)
        counter = 0
        while True:
            logger.info("tick %d", counter)
            counter += 1
            time.sleep(10)