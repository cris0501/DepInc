#!/bin/python
from base.Provider import Provider

class dbProvider (Provider):
    _instance = None
    
    def __new__(cls):
        print(cls)
        if cls._instance is None:
            print('Creando DB')
            cls._instance = super(dbProvider, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        print('Iniciando DB')

    def create():
        pass
