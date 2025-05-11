import inspect
from app.use_cases.flight_service import FlightService
from adapters.out.memory_flight_repository import MemoryFlightRepository
from adapters.out.console_event_dispatcher import ConsoleEventDispatcher

class Container:
    def __init__(self):
        self._bindings = {}
        
        self.loadProviders()
        
        self.repository = MemoryFlightRepository()
        self.dispatcher = ConsoleEventDispatcher()
        self.flight_service = FlightService(self.repository, self.dispatcher)
    
    def loadProviders(self):
        print("Load and register Providers!")
        
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
            else:
                dependencies.append(None)  # Add none value and used default

        return cls(*dependencies) # Resolve and create a instance of class