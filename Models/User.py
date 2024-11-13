#!/bin/python
from Providers.dbProvider import dbProvider as DB

class User ():
    def __init__(self, db: DB):
        db.__init__()
