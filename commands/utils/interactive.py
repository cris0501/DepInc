from pathlib import Path

def prompt_yesno(question: str) -> bool:
    ans = input(question + " [Y/n] > ").strip().lower()
    return ans in ("", "y", "yes")

def prompt_select_providers(provider_dict):
    keys = list(provider_dict.keys())
    print("\nSelecciona las dependencias a inyectar (separa por coma):")
    for i, key in enumerate(keys, 1):
        print(f"[{i}] {key.__name__}")
    indexes = input("> ").strip().split(",")
    selected = []
    for idx in indexes:
        try:
            key = keys[int(idx.strip()) - 1]
            dep = provider_dict[key]
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