#!/bin/python
from base.Provider import Provider

class observerProvider (Provider):
    #_instance = None
    
    #def __new__(cls, *args, **kwargs):
    #    if cls._instance is None:
    #        cls._instance = super(observerProvider, cls).__new__(cls)
    #    return cls._instance

    def __init__(self):
        pass

    def create(self):
        pass

    def update(self, msj):
        print(f"{msj}")
