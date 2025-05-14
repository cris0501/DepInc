from pathlib import Path
from config.paths import paths
from commands.utils.use_case import make_use_case
from commands.utils.adapter import make_adapter
from config.providers import providers

TYPES = ['Adapter', 'UseCase']

def prompt_yesno(question: str) -> bool:
    ans = input(question + " [Y/n] > ").strip().lower()
    return ans in ("y", "yes")

def prompt_select_providers(providers):
    keys = list(providers.keys())
    print("\nSelecciona las dependencias a inyectar (separa por coma):")
    for i, key in enumerate(keys, 1):
        print(f"[{i}] {key.__name__}")
    indexes = input("> ").strip().split(",")
    selected = []
    for idx in indexes:
        try:
            key = keys[int(idx.strip()) - 1]
            dep = providers[key]
            dep["__class__"] = key
            selected.append(dep)
        except:
            continue
    return selected

def generate_code(stub, class_name, deps):
    import_lines = "\n".join([
        f"from {d['path']} import {d['__class__'].__name__}"
        for d in deps
    ]) or ""

    constructor_args = ", ".join([
        f"{d['__class__'].__name__[0].lower() + d['__class__'].__name__[1:]}: {d['__class__'].__name__}"
        for d in deps
    ]) or ""

    stub = stub.replace("__imports__", import_lines)
    stub = stub.replace("__deps__", constructor_args)
    stub = stub.replace("__class_name__", class_name)

    return stub

def write_file(path: Path, content: str, force: bool = False):
    if path.exists() and not force:
        print(f"[!] El archivo '{path}' ya existe. Usa --force para sobrescribir.")
        return False
    path.write_text(content)
    print(f"[✓] Archivo creado: {path}")
    return True

def execute():
    print("\nQué tipo de archivo quieres crear:")
    for i, item in enumerate(TYPES, 1):
        print(f"[{i}] {item}")
    type_file = int(input("> ")) - 1
    name_type = TYPES[type_file].lower()

    print(f"\nNombre del {name_type}:")
    name = input("> ").lower()

    deps = []
    if prompt_yesno("¿Deseas usar dependencias?"):
        deps = prompt_select_providers(providers)

    stub, class_name, file_path = make_adapter(name) if (type_file == 0) else make_use_case(name)
    stub = generate_code(stub, class_name, deps)

    write_file(file_path, stub)