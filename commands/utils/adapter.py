from pathlib import Path
from config.paths import paths
#from config.providers import providers
from commands.utils.dependency_rules import filter_providers_for
from commands.utils.interactive import prompt_yesno, prompt_select_providers

def make_adapter(name: str):
    is_entry = prompt_yesno("¿Tu adapter es de entrada? (Por defecto, es de salida)")
    stub_name = "adapter_input.stub" if is_entry else "adapter_output.stub"
    stub_path = paths['stubs'] / stub_name

    file_name = name.lower() if name.endswith("adapter") else name.lower() + "_adapter"
    class_name = name.capitalize() if name.lower().endswith("adapter") else name.capitalize() + "Adapter"
    file_path = paths["adapters"] / ("input" if is_entry else "output") / f"{file_name}.py"

    deps = []
    #if prompt_yesno("¿Deseas usar dependencias?"):
    #    valid = filter_providers_for("adapter", providers)
    #    deps = prompt_select_providers(valid)

    return stub_path.read_text(), class_name, file_path, deps