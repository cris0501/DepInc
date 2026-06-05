import importlib
import inspect


def install(container):
    # -- aditiona statel ----------------------------------------------
    container._hooks      = {"before_resolve": [], "after_resolve": []}
    container._singletons = set()
    container._cache      = {}

    # -- new methods ------------------------------------------------
    container.singleton = _singleton.__get__(container)
    container.hook      = _hook.__get__(container)

    # -- update function pointer ------------------------------------
    container.resolve = _resolve.__get__(container)
    container._build  = _build.__get__(container)

    # -- carga config y plugins declarados -----------------------------
    _load_config(container)
    _load_plugins(container)
    print("Container full install")


# -- inject methods --------------------------------------------------------

def _singleton(self, *classes):
    self._singletons.update(classes)
    return self


def _hook(self, point: str, fn, priority: int = 50):
    if point not in self._hooks:
        raise ValueError(f"Hook '{point}' no existe")
    self._hooks[point].append((priority, fn))
    self._hooks[point].sort(key=lambda x: x[0])


def _resolve(self, key, overrides=None):
    for _, hook in self._hooks["before_resolve"]:
        result = hook(key)
        if result is not None:
            return result

    override_map = _normalize_overrides(self, overrides) if overrides else {}

    if key in self._singletons:
        if key not in self._cache:
            self._cache[key] = self._build(key, override_map)
        return self._cache[key]

    instance = self._build(key, override_map)

    for _, hook in self._hooks["after_resolve"]:
        instance = hook(key, instance)

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
            raise ValueError(f"'{cls.__name__}' no implementa ninguna interfaz registrada")
        if len(registered_bases) > 1:
            names = ', '.join(b.__name__ for b in registered_bases)
            raise ValueError(
                f"'{cls.__name__}' implementa múltiples interfaces ({names}). "
                f"Usa un dict explícito: {{Interface: {cls.__name__}}}"
            )
        result[registered_bases[0]] = cls
    return result


def _build(self, key, override_map=None):
    override_map = override_map or {}
    cls = override_map.get(key) or self._bindings.get(key, key)

    sig = inspect.signature(cls.__init__)
    args = []
    for param in list(sig.parameters.values())[1:]:
        if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            continue
        local_override = getattr(cls, '_bindings', {}).get(param.annotation)
        dep = local_override or override_map.get(param.annotation) or param.annotation
        args.append(self._build(dep, override_map))

    return cls(*args)


# -- config y plugins ----------------------------------------------------------

def _load_config(container):
    try:
        from config.bindings import bindings
        for key, cls in bindings.items():
            container.provider(key, cls)
            if getattr(cls, '_singleton', False):
                container._singletons.add(cls)
    except ImportError:
        pass


def _load_plugins(container):
    try:
        from depinc.plugins import plugins
        for name in plugins:
            mod = importlib.import_module(f"depinc.plugins.{name}.plugin")
            mod.install(container)
    except ImportError:
        pass