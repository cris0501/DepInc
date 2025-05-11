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
├── app/                    # Núcleo: modelos de dominio, puertos, casos de uso
├── config/                 # (Planeado) configuración general y de providers
├── infrastructure/         # Contenedor y configuración de dependencias
├── main.py                 # Punto de entrada principal
```

## Ejecución

```bash
python main.py
```

Esto ejecuta el adaptador CLI con comandos de prueba para vuelos (crear y listar vuelos).

## Futuro del proyecto

- Soporte para comandos personalizados (`depinc make:port`, `depinc make:adapter`, etc).
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
