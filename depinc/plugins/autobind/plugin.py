import importlib
import inspect
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

SCAN_PATHS = ["app"]


def install(container):
    interfaces, implementations = _discover(SCAN_PATHS)

    imports = set()
    bindings = {}

    for abc_cls in interfaces:
        impls = implementations.get(abc_cls, [])
        if len(impls) == 1:
            impl = impls[0]
            imports.add(f"from {abc_cls.__module__} import {abc_cls.__name__}")
            imports.add(f"from {impl.__module__} import {impl.__name__}")
            bindings[abc_cls.__name__] = impl.__name__
        elif len(impls) > 1:
            names = ', '.join(i.__name__ for i in impls)
            logger.debug(
                "Skipping auto-bind for %s: multiple implementations (%s). "
                "Override in config/bindings.py", abc_cls.__name__, names
            )

    if not bindings:
        logger.debug("Autobind install (no bindings found)")
        return

    root = Path(__file__).resolve().parent.parent.parent.parent
    bindings_path = root / "config" / "bindings.py"

    import_lines = "\n".join(sorted(imports))
    binding_lines = "\n".join(f"    {k}: {v}," for k, v in bindings.items())

    content = f"""{import_lines}

bindings = {{
{binding_lines}
}}
"""
    bindings_path.write_text(content)
    logger.debug("Autobind install -> wrote config/bindings.py")


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
