# DepInC (Dependency Injection Core)

**DepInC** es un micro-framework experimental en Python basado en la arquitectura **hexagonal (puertos y adaptadores)**, diseñado para facilitar el desarrollo desacoplado y modular de aplicaciones. Su núcleo está centrado en la **inyección de dependencias** y la capacidad de registrar dinámicamente servicios, casos de uso, adaptadores y modelos de dominio.

> **Nota**: El ejemplo actual implementa un dominio ficticio de "vuelos" únicamente como **prueba de concepto** para validar la funcionalidad del framework. **El objetivo real no es crear una app de vuelos**, sino sentar las bases de un sistema extensible, tipo Laravel, con comandos artesanales que faciliten la creación de puertos, adaptadores y estructuras hexagonales.

## Características

- Arquitectura **Hexagonal** real con separación de dominios, casos de uso y adaptadores.
- Contenedor de inyección de dependencias simple.
- Enrutamiento de comandos CLI como adaptador de entrada.
- Repositorio en memoria y dispatcher por consola como adaptadores de salida.
- Modelo de dominio fácilmente ampliable.
- Estructura preparada para comandos personalizados tipo `artisan`.

## Estructura

```
.
├── adapters/               # Adaptadores de entrada (CLI) y salida (repositorio en memoria, dispatcher)
├── commands/               # Comandos disponibles para el CLI
    ├── utils/stubs/        # Plantillas de archivos
├── config/                 # Configuración general de la app
├── core/                    # Núcleo: modelos de dominio, puertos, casos de uso
├── infrastructure/         # Contenedor y configuración de dependencias
    ├── container/          # Contenedor general de la APP
    ├── decorators/         # Decoradores que agregan funcionalidad
├── depinc.py               # Punto de entrada principal
```

## Ejecuta de la app

```bash
python depinc.py run
```

Esto ejecuta el adaptador CLI con comandos de prueba para vuelos (crear y listar vuelos).

## Comandos de ayuda

```bash
python depinc.py make
```

Este comando es una utilidad para crear archivos basicos que cumplen con la estructura recomendada. Es un maker interactivo que te permite personalizar la creacion de tus componentes, incluso te permite hacer una configuracion basica de los provider que puedes inyectar de forma automatica por el contenedor. Este maker nos permite creear:

- Modelos
- Casos de uso
- Adaptadores
- Middlewares

## Contenedor

El contenedor principal es el encargado de cargar los providers, services y el resto de clases marcadas para ser inyectables. Resuelve dependencias anidadas y permite la sobre escritura de dependencias. Esta lectura de dependencias **tendá** un mecanismo dual.

**En proximos commits**: Esto es, a traves de un listado podemos indicarle cuales seran las dependencias estaticas, clases que siempre estaran disponibles para ser inyectables. Aqui, DepInC incluye clases basicas, las cuales son remplazables por el desarrollador. Para ello, se usa el decorador **@inyectable()**, del cual se hara una seccion.

## Dependencias
Para saber que dependencias puede inyectar el contenedor, se puede marcar cualquier clase con el decorador **@inyectable()**, este decorador le indica al contenedor que la clase sera disponible para resolver de forma dinamica. Es importante mencionar que las dependencias del mismo estaran indicadas en el constructor de la clase como parametros, no en el cuerpo del mismo.

De igual forma, se proverá de un listado basico en la carpeta de configuraciones donde se listan las clases que estaran disponibles siempre, sin la necesidad de que estas incluyan el decorador en su definicion. Es un mecanismo poderoso que permite una dualidad dando preferencia a las clases marcadas por el decorador de forma explicita por el desarrollador. Sin embargo, para evitar coliciones y permitir la inyectabilidad de una o mas clases del mismo tipo (repositorios por ejemplo), el decorador permite hacer uso de variantes mediante el parametro **variant**.

```python
from core.ports.output.repository import Repository
from infrastructure import inyectable

@inyectable(key=Repository, variant='sqlite')
class SQLiteFlightRepository(Repository):
    def __init__(self):
        ...

@inyectable(key=Repository, variant='memory')
class MemoryFlightRepository(Repository):
    def __init__(self):
        ...
```

Posteriormente, cuando se solicita la resolucion de cualquier clase que haga uso de un repositorio, basta con pasar un diccionario indicando explicitamente el nombre de la key con la que se registro asociada a la variante que se usara:

```python
flight_service = app.resolve(FlightService, {'repository': 'memory'})
flight_service = app.resolve(FlightService, {'repository': 'sqlite'})
```

Esto indica al contenedor con precision que repositorio usar, lo que permite multiples referencias a un mismo tipo de clase sin coliciones. De esta forma, las clases pueden tener como parametro un port de tipo Repository y nos permite indicar de forma concreta cual usar sin la necesidad de instanciarlo previamente.

## Modelos

Todo modelo hereda de una clase base **model.py** el cual contiene la logica del control interno de estado. Se usan atributos internos y la modificacion de metodos magicos para controlar el estado del modelo. Esto permite:

- Conocer los atributos originales durante la creacion del modelo.
- Conocer los atributos que han sido modificados para optimizar las peticiones del repositorio.
- Mantiene un control interno de cuales son los atributos que seran almacenados por el repositorio (**fillables**).
- Marcar nuevos atributos, dinamicos o generados durante ejecucion, para ser almacenados.

## Casos de uso

Aqui se define la logica de un caso de uso (un proceso que nuestra app llevara acabo). En esta etapa no se hace directamente la modificacion de los estados internos de los modelos, esto es tarea de los propios modelos. La programacion en esta seccion debe ser mas declarativa. Es comun que sea aqui donde se usen los repositorios y los modelos juntos puesto que se hacen las valdiaciones correspondientes y se delega las tareas de mutaciones, almacenamiento y cualquier contacto con el exterior al resto de capas.

## Middlewares

Un Middleware es una funcion que se ejecuta antes o despues de una funcion y tiene la capacidad de modificar el funcionamiento de la misma, inclusive denegar su ejecucion. Este tipo de elementos son muy utiles, principalemte para hacer validaciones y permitir ejecutar ciertas acciones. Estas funciones son invocadas mediante un decorador creado para la facilidad de uso. Cuando se crea un caso de uso, este ya incluye la importacion del decorador **@middleware**. Este decorador ejecutara los middlewares en la lista que recibe como parametros. Para un caso de uso, estos se ejecutan antes del metodo que se invoca, esto ya que un middleware se ejecuta antes o despues del caso de uso y puesto que el caso de uso no tiene el deber de interacturar con la respuesta del adaptador (como escribir en db, crear respuesta json, etc), los middlewares se ejecutan antes del metodo invocado del servicio.

Se pueden crear middlewares mediante el maker que ofrece **depinc**. Ademas, estos se registran automaticamente en el modulo para que su importacion sea de lo mas sencilla.

```python
from infrastructure.middlewares import middleware, new_middleware

class Service():
    @middleware([new_middleware])
    def use_method (self, deps):
        ...
```

## Futuro del proyecto

- Soporte para mas comandos personalizados (`list [use_cases, adapters]`, etc).
- Capa ORM básica con soporte a múltiples drivers (`mysql`, `sqlite`, `mongo`).
- Sistema de eventos y observadores.
- Modularización avanzada para proyectos grandes.

## Requisitos

- Python 3.12 o superior

## Estado

Este proyecto se encuentra en **fase experimental** y está en desarrollo activo. Cualquier contribución o sugerencia es bienvenida.


## Licencia

Este proyecto está licenciado bajo la [Creative Commons Atribución 4.0 Internacional (CC BY 4.0)](http://creativecommons.org/licenses/by/4.0/).
Puedes compartir y modificar libremente este código, siempre y cuando menciones al autor original.
