import logging
from depinc.adapter import Adapter
from depinc import context


class AdapterLogger(Adapter):
    def __init__(self, name: str):
        super().__init__(None)
        self._logger = logging.getLogger(name)

    def run(self):
        context.logger.set(self)

    def debug(self, msg, *args, **kwargs):
        self._logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self._logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._logger.error(msg, *args, **kwargs)
