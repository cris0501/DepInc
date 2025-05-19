from pathlib import Path

# Punto base del proyecto
project_root = Path(__file__).parent.parent.resolve()

# Directorios estándar
paths = {
    "root": project_root,
    "adapters": project_root / "adapters",
    "use_cases": project_root / "core" / "use_cases",
    "models": project_root / "core" / "domain" / "models",
    "middlewares": project_root / "infrastructure" / "middlewares",
    "stubs": project_root / "commands" / "utils" / "stubs"
}