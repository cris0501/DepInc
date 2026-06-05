# depinc/plugins/middleware/plugin.py
from .Middleware import apply

def install(container):
    from config.middlewares import middlewares

    def _apply(key, instance):
        method_map = middlewares.get(key)
        if not method_map:
            return instance

        for method_name, mws in method_map.items():
            original = getattr(instance, method_name)
            setattr(instance, method_name, apply(mws, original))

        return instance

    container.hook("after_resolve", _apply, priority=50)
    print("Logger install")