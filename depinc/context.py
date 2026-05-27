from contextvars import ContextVar

logger = ContextVar('logger', default=None)
