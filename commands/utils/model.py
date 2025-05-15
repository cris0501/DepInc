from pathlib import Path
from config.paths import paths
from config.providers import providers
from commands.utils.dependency_rules import filter_providers_for
from commands.utils.interactive import prompt_yesno, prompt_select_providers

def make_model(name: str):
    stub_path = paths["stubs"] / "model.stub"
    class_name = name.capitalize()
    file_path = paths["models"] / f"{name.lower()}.py"

    deps = []

    return stub_path.read_text(), class_name, file_path, deps