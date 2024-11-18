#!/bin/python
from Models.User import User
from Models.School import School
from base.Container import Container as App

def main ():
    print("Iniciando DepInc")
    print("By Cristian R")
    
    app = App()
    
    user = app.resolve(User)
    user2 = app.resolve(User)
    school = app.resolve(School)

    school.register(user)
    school.register(user2)

    school.change('Hora de salida')

if (__name__ == '__main__'):
    main()
