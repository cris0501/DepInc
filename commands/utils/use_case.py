from pathlib import Path
from config.paths import paths

STUB_PATH = paths['stubs'] / "use_case.stub"

def make_use_case(name):
    file_name = name.lower() if name.endswith('service') else name.lower()+"_service"
    return [
      STUB_PATH.read_text(),
      name.capitalize() if name.endswith("Service") else name.capitalize() + "Service",
      paths['use_case'] / f"{file_name}.py"
    ]