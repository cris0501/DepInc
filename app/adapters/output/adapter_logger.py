import logging
from depinc.adapter import Adapter
from depinc.plugins.logger import logger


class LoggerAdapter(Adapter):
    def __init__(self, adapter: Adapter):
        self._name = adapter.__class__.__name__

    def run(self):
        logger.set(logging.getLogger(self._name))