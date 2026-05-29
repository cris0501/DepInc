import inspect
import importlib
import logging
from depinc import context

logger = logging.getLogger(__name__)


class Container:
    def __init__(self):
        context.container = self
        self._hooks = {
            "before_resolve": [],
            "after_resolve":  [],
        }

        self._bindings = {}
        self._singletons: set = set() # Save class
        self._cache = {} # Save instances / objs
        self.auto_register()

    def provider(self, key, provider):
        """ Register providers of dependencies """
        self._bindings[key] = provider

    def singleton(self, *classes):
        """ Register providers that will be singletons """
        self._singletons.update(classes)
        return self

    def hook(self, point: str, fn, priority: int = 50):
        """ Register hook """
        if point not in self._hooks:
            raise ValueError(f"Hook '{point}' no existe")
        self._hooks[point].append((priority, fn))
        self._hooks[point].sort(key=lambda x: x[0])

    def resolve(self, key, overrides=None):
        # Some pluggin would interrup resolve
        for _, hook in self._hooks["before_resolve"]:
            result = hook(key)
            if result is not None:
                return result # Override resolve for pluggin

        override_map = self._normalize_overrides(overrides) if overrides else {}
        if key in self._singletons:
            if key not in self._cache:
                self._cache[key] = self._build(key, override_map)
            return self._cache[key]

        instance = self._build(key, override_map)

        # Pluggins that modify execution of obj
        for _, hook in self._hooks["after_resolve"]:
            instance = hook(key, instance)

        return instance

    def _normalize_overrides(self, overrides):
        """ Create a dicc with type -> class """
        if isinstance(overrides, dict):
            return overrides

        result = {}
        if inspect.isclass(overrides):
            overrides = [overrides]

        for cls in overrides:
            registered_bases = [b for b in cls.__bases__ if b in self._bindings]
            if not registered_bases:
                raise ValueError(
                    f"'{cls.__name__}' does not implement any interface registered in bindings"
                )
            if len(registered_bases) > 1:
                names = ', '.join(b.__name__ for b in registered_bases)
                raise ValueError(
                    f"'{cls.__name__}' implements multiple registered interfaces ({names}). "
                    f"Use a dict to be explicit: {{Interface: {cls.__name__}}}"
                )
            result[registered_bases[0]] = cls
        return result

    def _validate(self, key, chain=None, override_map=None):
        """ Recursive fuction that registry dependencies """
        chain = chain or set()
        override_map = override_map or {}

        if key in chain:
            raise ValueError(f"Circular dependency: {key.__name__}")

        cls = override_map.get(key) or self._bindings.get(key, key)

        if inspect.isabstract(cls):
            raise ValueError(f"'{cls.__name__}' is abstract and has no registered binding")

        sig = inspect.signature(cls.__init__)
        for param in list(sig.parameters.values())[1:]:
            if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
                continue
            if param.annotation is inspect.Parameter.empty:
                raise ValueError(f"'{param.name}' in {cls.__name__} has no type annotation")
            self._validate(param.annotation, chain | {key}, override_map)

    def _build(self, key, override_map=None):
        override_map = override_map or {}
        cls = override_map.get(key) or self._bindings.get(key, key)
        logger.debug(f"Build {key.__name__} -> {cls}")
        sig = inspect.signature(cls.__init__)
        args = []

        for param in list(sig.parameters.values())[1:]:
            if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
                continue

            local_override = getattr(cls, '_bindings', {}).get(param.annotation)
            if local_override:
                args.append(self._build(local_override, override_map))
            else:
                args.append(self._build(param.annotation, override_map))

        return cls(*args)

    def auto_register(self):
        from config.bindings import bindings
        for key, cls in bindings.items():
            self.provider(key, cls)

        from depinc.plugins import plugins
        for name in plugins:
            mod = importlib.import_module(f"depinc.plugins.{name}.plugin")
            mod.install(self)
