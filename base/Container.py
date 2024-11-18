#!/bin/python
import inspect
from typing import Type, Any
from Providers.dbProvider import *
from Providers.eventProvider import *
from Providers.observerProvider import *

class Container():
    _dependencies = {}

    def __init__(self):
        self.loadProviders(eventProvider, eventProvider())
        self.loadProviders(observerProvider, observerProvider())
        self.loadProviders(dbProvider, dbProvider())

    def loadProviders(self, interface, implementation):
        self._dependencies[interface] = implementation

    def resolve(self, cls):
        constructor = cls.__init__
        parameters = constructor.__annotations__
        dependencies = {
            name: self._dependencies[param] for name,
            param in parameters.items() if param in self._dependencies
        }
        return cls(**dependencies)


