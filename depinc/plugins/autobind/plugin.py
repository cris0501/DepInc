import importlib
import inspect
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

SCAN_PATHS = ["app"]


def install(container):
    interfaces, implementations = _discover(SCAN_PATHS)

    for abc_cls in interfaces:
        if abc_cls in container._bindings:
            continue  # explicit bindings (config/bindings.py) always win
        impls = implementations.get(abc_cls, [])
        if len(impls) == 1:
            container.provider(abc_cls, impls[0])
            logger.debug("Auto-bind %s -> %s", abc_cls.__name__, impls[0].__name__)
        elif len(impls) > 1:
            names = ', '.join(i.__name__ for i in impls)
            logger.debug(
                "Skipping auto-bind for %s: multiple implementations (%s). "
                "Declare it in config/bindings.py", abc_cls.__name__, names
            )

    logger.debug("Autobind install")


def _discover(scan_paths):
    """Scan the app for interfaces (ABCs) and their concrete implementations.

    An interface is any abstract class found in the scan paths, plus any
    abstract base in the MRO of a discovered concrete class (this covers
    framework ports like Repository).
    """
    interfaces = set()
    implementations = {}

    for rel_path in scan_paths:
        base = Path(rel_path)
        if not base.exists():
            continue
        for file in base.rglob("*.py"):
            if file.name.startswith("_"):
                continue
            module_path = ".".join(file.with_suffix("").parts)
            module = importlib.import_module(module_path)
            for obj in vars(module).values():
                # only classes defined in this module, not re-exports
                if not inspect.isclass(obj) or obj.__module__ != module_path:
                    continue
                if inspect.isabstract(obj):
                    interfaces.add(obj)
                else:
                    for ancestor in obj.__mro__[1:]:
                        if inspect.isabstract(ancestor):
                            interfaces.add(ancestor)
                            impls = implementations.setdefault(ancestor, [])
                            if obj not in impls:
                                impls.append(obj)

    return interfaces, implementations
