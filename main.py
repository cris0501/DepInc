#!/bin/python
import inspect
from typing import Type, Any
from Models.User import User
from Models.School import School

def loadProviders():
    pass

def resolve(cls: Type):
    data = inspect.signature(cls.__init__)
    for [key, item] in data.parameters.items():
        if item.annotation != inspect._empty:
            print(key,',',item.annotation)
            temp = item.annotation()

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
    resolve(User)
    resolve(School)

if (__name__ == '__main__'):
    main()
