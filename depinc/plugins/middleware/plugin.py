# depinc/plugins/middleware/plugin.py
import logging
from pathlib import Path

from .Middleware import apply

logger = logging.getLogger(__name__)


def install(container):
    _ensure_config()

    try:
        from config.middlewares import middlewares
    except ImportError:
        middlewares = {}

    def _apply(key, instance):
        method_map = middlewares.get(key)
        if not method_map:
            return instance

        for method_name, mws in method_map.items():
            original = getattr(instance, method_name)
            setattr(instance, method_name, apply(mws, original))

        return instance

    container.hook("after_resolve", _apply, priority=50)
    logger.debug("Middleware install")


def _ensure_config():
    root = Path(__file__).resolve().parent.parent.parent.parent
    mw_config = root / "config" / "middlewares.py"
    if mw_config.exists():
        return
    mw_config.write_text("""\
middlewares = {}
""")
