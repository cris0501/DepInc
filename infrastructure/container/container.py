import inspect, importlib, pkgutil

from infrastructure.decorators.inyectable import INJECTABLES, INJECTABLE_ALIASES

class Container:
    _bindings = {}
    
    def __init__(self):
        self.auto_register()
    
    def register(self, key, provider):
        self._bindings[key] = provider
    
    def auto_register(self):
        for key, cls in INJECTABLES.items():
            self.register(key, cls)
        for key, cls in INJECTABLE_ALIASES.items():
            self.register(key, cls)

    def resolve(self, key, deps: dict = None):
        cls = self._bindings.get(key)
        impl = None
    
        # Si no está registrado directamente, buscar variante
        if cls is None and deps:
            variant_key = deps.get(f"{key.__name__.lower()}")  # 'repository': 'redis'
            impl = INJECTABLE_ALIASES.get((key, variant_key))
            if impl:
                cls = impl
    
        if cls is None:
            raise ValueError(f"No binding for key {key}")
    
        # Constructor de la clase a instanciar
        sig = inspect.signature(cls.__init__)
        params = list(sig.parameters.values())[1:]  # skip self
    
        resolved_args = []
        for param in params:
            if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
                continue
    
            param_name = param.name
            param_type = param.annotation
            
            if param_type in self._bindings:
                resolved_args.append(self.resolve(param_type, deps))
            else:
                if deps:
                    variant_name = deps.get(param_name)  # "repository": "redis"
                    variant_impl = INJECTABLE_ALIASES.get((param_type, variant_name))
                    if variant_impl:
                        resolved_args.append(self.resolve(variant_impl, deps))
                        continue
    
                raise ValueError(f"No se pudo resolver el parámetro '{param_name}' en {cls.__name__}")
    
        return cls(*resolved_args)