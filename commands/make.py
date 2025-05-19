from .utils import make_use_case, make_adapter, make_model, make_middleware
from .utils.interactive import generate_code, write_file

def execute():
    print("\nQué tipo de archivo quieres crear:")
    print("[1] Adapter")
    print("[2] UseCase")
    print("[3] Model")
    print("[4] Middleware")
    type_file = int(input("> ")) - 1

    name_type = ["adapter", "usecase", "model", "middleware"][type_file]
    print(f"\nNombre del {name_type}:")
    name = input("> ").strip()

    if name_type == "adapter":
        stub, class_name, file_path, deps = make_adapter(name)
    elif name_type == "usecase":
        stub, class_name, file_path, deps = make_use_case(name)
    elif name_type == "model":
        stub, class_name, file_path, deps = make_model(name)
    elif name_type == "middleware":
        stub, class_name, file_path, deps = make_middleware(name)

    stub = generate_code(stub, class_name, deps)
    write_file(file_path, stub)
