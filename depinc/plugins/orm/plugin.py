import importlib
import inspect
import logging
from pathlib import Path

from .Repository import Repository

logger = logging.getLogger(__name__)

DEFAULT_DRIVER = "sqlite"


def install(container):
    _ensure_config()

    driver = database_config().get("driver", DEFAULT_DRIVER)
    container.provider(Repository, _driver_class(driver))
    logger.debug("ORM install: driver '%s'", driver)


def _ensure_config():
    root = Path.cwd()
    _create_folder(root / "app" / "domain")
    db_config = root / "config" / "database.py"
    if db_config.exists():
        return
    db_config.write_text(f"""\
# Database driver for the ORM plugin.
# Available drivers: sqlite, memory
database = {{
    "driver": "{DEFAULT_DRIVER}",
    "database": "database.db",
}}
""")


def database_config():
    try:
        from config.database import database
        return database
    except ImportError:
        return {}


def _create_folder(path):
    path.mkdir(parents=True, exist_ok=True)
    init = path / "__init__.py"
    if not init.exists():
        init.write_text("")


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
