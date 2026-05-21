from pathlib import Path

# Punto base del proyecto
project_root = Path(__file__).parent.parent.resolve()

# Directorios estándar
paths = {
    "root": project_root,
    "adapters": project_root / "app" / "adapters",
    "use_cases": project_root / "app" / "use_cases",
    "models": project_root / "app" / "domain",
    "middlewares": project_root / "app" / "middlewares",
    "stubs": project_root / "commands" / "utils" / "stubs"
}