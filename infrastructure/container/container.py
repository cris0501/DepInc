import inspect
from config.providers import default_providers

class Container:
    def __init__(self):
        self._bindings = {}
        self.auto_register()

    def register(self, key, provider):
        self._bindings[key] = provider

    def auto_register(self):
        for key, cls in default_providers.items():
            self.register(key, cls)

    def resolve(self, key):
        cls = self._bindings.get(key)

        if cls is None:
            raise ValueError(f"No binding for {key}")

        sig = inspect.signature(cls.__init__)
        params = list(sig.parameters.values())[1:]

        resolved_args = []
        for param in params:
            if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
                continue

            param_type = param.annotation

            if param_type in self._bindings:
                resolved_args.append(self.resolve(param_type))
            else:
                raise ValueError(f"No se pudo resolver '{param.name}' en {cls.__name__}")

        return cls(*resolved_args)
