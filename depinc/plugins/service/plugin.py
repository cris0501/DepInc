import logging
from pathlib import Path

logger = logging.getLogger(__name__)

FOLDERS = [
    "app/ports/input",
    "app/ports/output",
    "app/use_cases",
]


def install(container):
    _create_folders()
    logger.debug("Service install")


def _create_folders():
    root = Path.cwd()
    for folder in FOLDERS:
        path = root / folder
        path.mkdir(parents=True, exist_ok=True)
        init = path / "__init__.py"
        if not init.exists():
            init.write_text("")
