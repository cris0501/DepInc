from contextvars import ContextVar
import logging


container = None
logger: ContextVar[logging.Logger] = ContextVar("logger")
