#!/bin/python
from base.Provider import Provider

class eventProvider (Provider):
    _instance = None
    
    def __new__(cls):
        print(cls)
        if cls._instance is None:
            print('Creando Event')
            cls._instance = super(eventProvider, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        print('Iniciando Event')

    def create(self):
        pass
