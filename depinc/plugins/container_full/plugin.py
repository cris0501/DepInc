import importlib
import inspect
import logging

logger = logging.getLogger(__name__)


def install(container):
    # -- additional state ----------------------------------------------
    container._hooks      = {"before_resolve": [], "after_resolve": []}
    container._singletons = set()
    container._cache      = {}
    container._building   = []   # construction stack for circular-dependency detection

    # -- new methods ------------------------------------------------
    container.singleton = _singleton.__get__(container)
    container.hook      = _hook.__get__(container)

    # -- chainable patch: keep the originals so another plugin can wrap too --
    container._parent_resolve = container.resolve
    container._parent_build   = container._build
    container.resolve = _resolve.__get__(container)
    container._build  = _build.__get__(container)

    # -- load config and declared plugins -----------------------------
    _load_config(container)
    _load_plugins(container)
    logger.debug("Container full install")


# -- injected methods --------------------------------------------------------

def _singleton(self, *classes):
    self._singletons.update(classes)
    return self


def _hook(self, point: str, fn, priority: int = 50):
    if point not in self._hooks:
        raise ValueError(f"Hook '{point}' does not exist")
    self._hooks[point].append((priority, fn))
    self._hooks[point].sort(key=lambda x: x[0])


def _resolve(self, key, overrides=None):
    for _, hook in self._hooks["before_resolve"]:
        result = hook(key)
        if result is not None:
            return result

    override_map = _normalize_overrides(self, overrides) if overrides else {}

    cls = _target_cls(self, key, override_map)
    was_cached = cls in self._cache

    instance = self._build(key, override_map)

    if not was_cached:
        for _, hook in self._hooks["after_resolve"]:
            instance = hook(key, instance)
        if cls in self._cache:
            # cache the decorated instance: later resolves get the same
            # object and hooks are never applied twice
            self._cache[cls] = instance

    return instance


def _normalize_overrides(self, overrides):
    if isinstance(overrides, dict):
        return overrides
    result = {}
    if inspect.isclass(overrides):
        overrides = [overrides]
    for cls in overrides:
        registered_bases = [b for b in cls.__bases__ if b in self._bindings]
        if not registered_bases:
            raise ValueError(f"'{cls.__name__}' does not implement any registered interface")
        if len(registered_bases) > 1:
            names = ', '.join(b.__name__ for b in registered_bases)
            raise ValueError(
                f"'{cls.__name__}' implements multiple interfaces ({names}). "
                f"Use an explicit dict: {{Interface: {cls.__name__}}}"
            )
        result[registered_bases[0]] = cls
    return result


def _target_cls(self, key, override_map):
    return override_map.get(key) or self._bindings.get(key, key)


def _is_singleton(self, key, cls):
    return (
        key in self._singletons
        or cls in self._singletons
        or getattr(cls, '_singleton', False)
    )


def _build(self, key, override_map=None):
    override_map = override_map or {}
    cls = _target_cls(self, key, override_map)

    if not inspect.isclass(cls):
        raise TypeError(f"Cannot build '{cls!r}' (resolved from '{key!r}')")

    if inspect.isabstract(cls):
        raise LookupError(
            f"'{cls.__name__}' is abstract and has no registered binding. "
            f"Declare it in config/bindings.py"
        )

    # the cache is checked here (not only in resolve) so that nested
    # dependencies share the same singleton instance
    if _is_singleton(self, key, cls) and cls in self._cache:
        return self._cache[cls]

    if cls in self._building:
        chain = " -> ".join(c.__name__ for c in self._building + [cls])
        raise RecursionError(f"Circular dependency detected: {chain}")

    self._building.append(cls)
    try:
        sig = inspect.signature(cls.__init__)
        args = []
        for param in list(sig.parameters.values())[1:]:
            if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
                continue
            if param.annotation is inspect.Parameter.empty:
                raise TypeError(
                    f"'{cls.__name__}.__init__': parameter '{param.name}' has no type annotation"
                )
            local_override = getattr(cls, '_bindings', {}).get(param.annotation)
            dep = local_override or override_map.get(param.annotation) or param.annotation
            args.append(self._build(dep, override_map))
    finally:
        self._building.pop()

    logger.debug("Build %s", cls.__name__)
    instance = cls(*args)

    if _is_singleton(self, key, cls):
        self._cache[cls] = instance

    return instance


# -- config and plugins ----------------------------------------------------------

def _load_config(container):
    try:
        from config.bindings import bindings
        for key, cls in bindings.items():
            container.provider(key, cls)
            if getattr(cls, '_singleton', False):
                container._singletons.add(key)
    except ImportError:
        pass


def _load_plugins(container):
    try:
        from depinc.plugins import plugins
    except ImportError:
        return
    # plugin failures must not be swallowed: a broken plugin should fail loudly
    for name in plugins:
        mod = importlib.import_module(f"depinc.plugins.{name}.plugin")
        mod.install(container)
