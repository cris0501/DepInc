import importlib
import inspect
import logging

from .Repository import Repository

logger = logging.getLogger(__name__)

DEFAULT_DRIVER = "memory"


def install(container):
    # explicit bindings (config/bindings.py, loaded before plugins) always win
    if Repository in container._bindings:
        logger.debug("Repository already bound, skipping driver setup")
        return

    driver = database_config().get("driver", DEFAULT_DRIVER)
    container.provider(Repository, _driver_class(driver))
    logger.debug("ORM install: driver '%s'", driver)


def database_config():
    try:
        from config.database import database
        return database
    except ImportError:
        return {}


def _driver_class(name):
    """Resolve a driver by convention: drivers/<name>.py exposing a Repository subclass."""
    try:
        module = importlib.import_module(f".drivers.{name}", package=__package__)
    except ImportError as e:
        raise LookupError(f"Unknown database driver '{name}': {e}") from e

    for obj in vars(module).values():
        if (
            inspect.isclass(obj)
            and issubclass(obj, Repository)
            and not inspect.isabstract(obj)
            and obj.__module__ == module.__name__
        ):
            return obj

    raise LookupError(f"Driver module '{name}' does not define a Repository subclass")
