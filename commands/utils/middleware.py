from pathlib import Path
from config.paths import paths
from commands.utils.interactive import prompt_yesno, prompt_select_providers

def make_middleware(name: str):
    class_name = name.capitalize() if name.lower().endswith("middleware") else name.capitalize() + "Middleware"
    stub_path = paths["stubs"] / "middleware.stub"

    file_path = paths["middlewares"] /  f"{name.lower()}_middleware.py"

    deps = []
    
    # registrar_middleware(name.lower())

    return stub_path.read_text(), class_name, file_path, deps

def registrar_middleware(_name: str):
    init_path = "infrastructure/middlewares/__init__.py"
    linea = f"from .{_name} import {_name}"

    # Verifica si ya está registrado
    with open(init_path, "r", encoding="utf-8") as f:
        contenido = f.readlines()
        if linea in contenido:
            print(f"{_name} ya está registrado.")
            return

    # Escribe la línea al final
    with open(init_path, "a", encoding="utf-8") as f:
        f.write("\n"+linea)
        print(f"{_name} registrado correctamente.")