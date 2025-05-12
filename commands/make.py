from pathlib import Path
from config.paths import paths

def load_stub(kind: str, _type=None):
    if _type and _type == 'ent':
        stub_path = Path(__file__).parent.parent / "stubs" / f"{kind}_ent.stub"
    elif _type and _type == 'out':
        stub_path = Path(__file__).parent.parent / "stubs" / f"{kind}_out.stub"
    else:
      stub_path = Path(__file__).parent.parent / "stubs" / f"{kind}.stub"
    
    if not stub_path.exists():
        raise FileNotFoundError(f"No stub encontrado para '{kind}' en {stub_path}")
    return stub_path.read_text()

def interpolate_stub(stub: str, class_name: str):
    return stub.replace("__class_name__", class_name)

def write_file(path: Path, content: str, force: bool = False):
    if path.exists() and not force:
        print(f"[!] El archivo '{path}' ya existe. Usa --force para sobrescribir.")
        return False
    path.write_text(content)
    print(f"[✓] Archivo creado: {path}")
    return True

def update_init(directory: Path, class_name: str, file_name: str):
    init_file = directory / "__init__.py"
    import_line = f"from .{file_name[:-3]} import {class_name}"
    if init_file.exists():
        lines = init_file.read_text().splitlines()
        if import_line in lines:
            print(f"[i] El archivo __init__.py ya incluye la clase {class_name}.")
            return
    else:
        lines = []
    lines.append(import_line)
    init_file.write_text("\n".join(lines) + "\n")
    print(f"[✓] Actualizado: {init_file}")

def execute(args):
    suffix = args.type.capitalize()
    class_name = args.name.capitalize() if args.name.endswith(suffix) else args.name.capitalize() + suffix
  
    file_name = args.name if args.name.endswith(args.type) else args.name + f"_{args.type}"
    
    type_stub = None
    if args.ent:
        type_stub = 'ent'
    elif args.out:
        type_stub = 'out'

    try:
        stub = load_stub(args.type, type_stub)
    except FileNotFoundError as e:
        print(f"[x] {e}")
        return

    content = interpolate_stub(stub, class_name)

    output_dir = paths.get(args.type)
    output_dir = output_dir / "ent" if args.ent else output_dir / "out"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    file_path = output_dir / f"{file_name}.py"

    if write_file(file_path, content, args.force) and args.register:
        update_init(output_dir, class_name, file_path.name)