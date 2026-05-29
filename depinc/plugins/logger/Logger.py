from contextvars import ContextVar
import logging

_var: ContextVar[logging.Logger] = ContextVar("logger")


class _LoggerProxy:
    def set(self, value: logging.Logger):
        _var.set(value)

    def get(self) -> logging.Logger:
        return _var.get()

    def debug(self, msg, *args, **kwargs):
        _var.get().debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        _var.get().info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        _var.get().warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        _var.get().error(msg, *args, **kwargs)


logger = _LoggerProxy()
