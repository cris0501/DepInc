from pathlib import Path

# Punto base del proyecto
project_root = Path(__file__).parent.parent.resolve()

# Directorios estándar
paths = {
    "root": project_root,
    "adapter": project_root / "adapters",
    "usecase": project_root / "app" / "usecases",
    "stubs": project_root / "stubs"
}