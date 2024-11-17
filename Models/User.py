#!/bin/python
from Providers.dbProvider import dbProvider as DB
from Providers.observerProvider import observerProvider

class User (observerProvider):
    def __init__(self, db: DB):
        pass

    def update(self, msj):
        print(f"User: {msj}")
