import inspect
from depinc.middleware import apply


class Container:
    def __init__(self):
        self._bindings = {}
        self._middlewares = {}
        self.auto_register()

    def register(self, key, provider):
        self._bindings[key] = provider

    def auto_register(self):
        from config.bindings import bindings
        for key, cls in bindings.items():
            self.register(key, cls)

        try:
            from config.middlewares import middlewares
            self._middlewares = middlewares
        except ImportError:
            pass

    def resolve(self, key, overrides=None):
        override_map = self._normalize_overrides(overrides) if overrides else {}
        self._validate(key, override_map=override_map)
        return self._build(key, override_map=override_map)

    def _normalize_overrides(self, overrides):
        if isinstance(overrides, dict):
            return overrides

        result = {}
        if inspect.isclass(overrides):
            overrides = [overrides]

        for cls in overrides:
            registered_bases = [b for b in cls.__bases__ if b in self._bindings]
            if not registered_bases:
                raise ValueError(
                    f"'{cls.__name__}' no implementa ninguna interfaz registrada en bindings"
                )
            if len(registered_bases) > 1:
                names = ', '.join(b.__name__ for b in registered_bases)
                raise ValueError(
                    f"'{cls.__name__}' implementa múltiples interfaces registradas ({names}). "
                    f"Usa un dict para ser explícito: {{Interface: {cls.__name__}}}"
                )
            result[registered_bases[0]] = cls
        return result

    def _validate(self, key, chain=None, override_map=None):
        chain = chain or set()
        override_map = override_map or {}

        if key in chain:
            raise ValueError(f"Dependencia circular detectada: {key.__name__}")

        cls = override_map.get(key) or self._bindings.get(key, key)

        if inspect.isabstract(cls):
            raise ValueError(f"'{cls.__name__}' es abstracta y no tiene binding registrado")

        sig = inspect.signature(cls.__init__)
        for param in list(sig.parameters.values())[1:]:
            if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
                continue
            if param.annotation is inspect.Parameter.empty:
                raise ValueError(f"'{param.name}' en {cls.__name__} no tiene anotación de tipo")
            self._validate(param.annotation, chain | {key}, override_map)

    def _build(self, key, override_map=None):
        override_map = override_map or {}
        cls = override_map.get(key) or self._bindings.get(key, key)
        sig = inspect.signature(cls.__init__)
        args = []
        for param in list(sig.parameters.values())[1:]:
            if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
                continue
            args.append(self._build(param.annotation, override_map))
        instance = cls(*args)
        self._apply_middlewares(key, instance)
        return instance

    def _apply_middlewares(self, key, instance):
        method_map = self._middlewares.get(key)
        if not method_map:
            return
        for method_name, mws in method_map.items():
            original = getattr(instance, method_name)
            setattr(instance, method_name, apply(mws, original))
