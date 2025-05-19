# core/ports/__init__.py
import os
import pkgutil
import importlib
import inspect

# Ruta de paquete base
package_name = __name__
package_path = os.path.dirname(__file__)

__all__ = []

# Recorremos subcarpetas (input, output, etc.)
for finder, modname, ispkg in pkgutil.iter_modules([package_path]):
    print(modname)
    submodule_path = os.path.join(package_path, modname)
    full_mod_path = f"{package_name}.{modname}"

    if ispkg:
        for _, submodname, _ in pkgutil.iter_modules([submodule_path]):
            full_submod = f"{full_mod_path}.{submodname}"
            mod = importlib.import_module(full_submod)

            for name, obj in inspect.getmembers(mod):
                # Aquí puedes aplicar lógica: solo clases, solo que terminen en Interface, etc.
                globals()[name] = obj
                __all__.append(name)