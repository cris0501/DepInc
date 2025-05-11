import inspect
from config.providers import providers

class Container:
    def __init__(self):
        self._bindings = {}
        self.loadProviders()
    
    def loadProviders(self):
        for key, implementation in providers.items():
            self.bind(key, implementation)
        
    def bind(self, name: str, cls):
        self._bindings[name] = cls

    def resolve(self, key):
        cls = self._bindings.get(key)
        if cls is None:
            raise ValueError(f"No binding for key {key}")

        sig = inspect.signature(cls.__init__) # Analize dependencies of class
        params = list(sig.parameters.values())[1:]  # Skip `self`

        dependencies = []
        for param in params:
            param_type = param.annotation # Needed use annotations
            if param_type in self._bindings:
                dependencies.append(self.resolve(param_type)) # Recursive resolver
            # else:
            #     print('None')
            #     dependencies.append(None)  # Add none value and used default
        
        return cls(*dependencies) # Resolve and create a instance of class