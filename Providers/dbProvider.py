#!/bin/python
import os
from dotenv import load_dotenv
from base.Provider import Provider

class dbProvider (Provider):
    _instance = None
    
    def __new__(cls):
        print(cls)
        if cls._instance is None:
            print('Creando DB')
            cls._instance = super(dbProvider, cls).__new__(cls)
            cls._instance.create()
        return cls._instance

    def __init__(self):
        print('Iniciando DB')

    def create(self):
        load_dotenv()
        db_host = os.getenv('DB_HOST')
        print(f"Creating DB in {db_host}")
