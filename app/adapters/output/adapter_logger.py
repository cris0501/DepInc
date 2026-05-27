import logging
from depinc.adapter import Adapter
from depinc import context


class LoggerAdapter(Adapter):
    def __init__(self, adapter: Adapter):
        self._name = adapter.__class__.__name__

    def run(self):
        context.logger.set(logging.getLogger(self._name))