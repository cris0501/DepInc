#!/bin/python
from base.Provider import Provider

class eventProvider (Provider):
    #_instance = None
    _observers = []
    
    #def __new__(cls, *args, **kwargs):
    #    if cls._instance is None:
    #        cls._instance = super(eventProvider, cls).__new__(cls)
    #    return cls._instance

    def __init__(self):
        pass

    def create(self):
        pass

    def register(self, observer):
        self._observers.append(observer)

    def remove(self, observer):
        self._observers.remove(observer)

    def notify(self, msj='Prueba'):
        for obs in self._observers:
            obs.update(msj)

