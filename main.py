#!/bin/python
import inspect
from typing import Type, Any
from Models.User import User
from Models.School import School

from Providers.dbProvider import *
from Providers.eventProvider import *
from Providers.observerProvider import *

_dependencies = {}

def loadProviders(interface, implementation):
    _dependencies[interface] = implementation

def resolve(cls):
    constructor = cls.__init__
    parameters = constructor.__annotations__
    dependencies = {
        name: _dependencies[param] for name,
        param in parameters.items() if param in _dependencies
    }
    return cls(**dependencies)

def main ():
    print("Iniciando DepInc")
    print("By Cristian R")
    # Configuraciones
    # contenedor
    # Provaiders

    # Iniciar servicios
    # Router
    # Eventos

    # Busqueda y ejecucion de routeo

    # user = User()
    loadProviders(eventProvider, eventProvider())
    loadProviders(observerProvider, observerProvider())
    loadProviders(dbProvider, dbProvider())

    user = resolve(User)
    user2 = resolve(User)
    school = resolve(School)

    school.register(user)
    school.register(user2)

    school.notify()

if (__name__ == '__main__'):
    main()
