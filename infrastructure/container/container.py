import inspect
from config.bindings import bindings

class Container:
    def __init__(self):
        self._bindings = {}
        self.auto_register()

    def register(self, key, provider):
        self._bindings[key] = provider

    def auto_register(self):
        for key, cls in bindings.items():
            self.register(key, cls)

    def resolve(self, key):
        self._validate(key)
        return self._build(key)

    def _validate(self, key, chain=None):
        chain = chain or set()

        if key in chain:
            raise ValueError(f"Dependencia circular detectada: {key.__name__}")

        cls = self._bindings.get(key, key)

        if inspect.isabstract(cls):
            raise ValueError(f"'{cls.__name__}' es abstracta y no tiene binding registrado")

        sig = inspect.signature(cls.__init__)
        for param in list(sig.parameters.values())[1:]:
            if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
                continue
            if param.annotation is inspect.Parameter.empty:
                raise ValueError(f"'{param.name}' en {cls.__name__} no tiene anotación de tipo")
            self._validate(param.annotation, chain | {key})

    def _build(self, key):
        cls = self._bindings.get(key, key)
        sig = inspect.signature(cls.__init__)
        args = []
        for param in list(sig.parameters.values())[1:]:
            if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
                continue
            args.append(self._build(param.annotation))
        return cls(*args)
