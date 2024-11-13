#!/bin/python
from Providers.dbProvider import *
from Providers.eventProvider import *

class School ():
    def __init__(self, db: dbProvider, event: eventProvider):
        db.__init__()
