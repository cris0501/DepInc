from commands.utils.use_case import make_use_case
from commands.utils.adapter import make_adapter
from commands.utils.interactive import generate_code, write_file

def execute():
    print("\nQué tipo de archivo quieres crear:")
    print("[1] Adapter")
    print("[2] UseCase")
    type_file = int(input("> ")) - 1

    name_type = ["adapter", "usecase"][type_file]
    print(f"\nNombre del {name_type}:")
    name = input("> ").strip()

    if name_type == "adapter":
        stub, class_name, file_path, deps = make_adapter(name)
    else:
        stub, class_name, file_path, deps = make_use_case(name)

    stub = generate_code(stub, class_name, deps)
    write_file(file_path, stub)