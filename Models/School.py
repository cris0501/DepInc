#!/bin/python
from Providers.dbProvider import *
from Providers.eventProvider import *

class School (eventProvider):
    def __init__(self, db: dbProvider):
        db.__init__()

    def change(self, msj):
        self.notify(msj)
