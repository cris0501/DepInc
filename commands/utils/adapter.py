from pathlib import Path
from config.paths import paths

def prompt_yesno(question: str) -> bool:
    ans = input(question + " [Y/n] > ").strip().lower()
    return ans in ("y", "yes")

def make_adapter(name):
    stub_path = paths['stubs'] / "adapter_out.stub"
    _type = False
    if prompt_yesno("¿Tu adapter es de entrada? (Por defecto, es de salida)"):
        stub_path = paths['stubs'] / "adapter_ent.stub"
        _type = True
    
    file_name = name.lower() if name.endswith('adapter') else name.lower()+"_adapter"
    file_path = paths['adapter'] / "ent" / f"{file_name}.py" if _type else paths['adapter'] / "out" / f"{file_name}.py"
    
    return [
      stub_path.read_text(),
      name.capitalize() if name.endswith("Adapter") else name.capitalize() + "Adapter",
      file_path
    ]