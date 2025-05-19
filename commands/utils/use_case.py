from pathlib import Path
from config.paths import paths
#from config.providers import providers
from commands.utils.dependency_rules import filter_providers_for
from commands.utils.interactive import prompt_yesno, prompt_select_providers

def make_use_case(name: str):
    stub_path = paths["stubs"] / "use_case.stub"
    file_name = name.lower() if name.endswith('service') else name.lower() + "_service"
    class_name = name.capitalize() if name.endswith("Service") else name.capitalize() + "Service"
    file_path = paths["use_cases"] / f"{file_name}.py"

    deps = []
    if prompt_yesno("¿Deseas usar dependencias?"):
        valid = filter_providers_for("use_case", {})
        deps = prompt_select_providers(valid)

    return stub_path.read_text(), class_name, file_path, deps