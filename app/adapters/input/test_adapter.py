import time
from depinc.adapter import Adapter
from depinc.context import logger
from app.ports.input.flight_service_port import FlightServicePort
from app.adapters.output.adapter_logger import AdapterLogger


class TestAdapter(Adapter):
    def run(self):
        AdapterLogger(self.__class__.__name__).run()
        flight_service = self._app.resolve(FlightServicePort)
        counter = 0
        while True:
            logger.get().info("tick %d", counter)
            counter += 1
            time.sleep(10)
