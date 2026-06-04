import inspect
import logging


class _LoggerProxy:
    def _caller_logger(self):
        frame = inspect.stack()[2]
        module = frame[0].f_globals.get('__name__', __name__)
        return logging.getLogger(module)

    def debug(self, msg, *args, **kwargs):
        self._caller_logger().debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self._caller_logger().info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._caller_logger().warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._caller_logger().error(msg, *args, **kwargs)


logger = _LoggerProxy()
