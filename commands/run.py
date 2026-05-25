import logging
from depinc import App
from app.adapters.input.cli_adapter import CLIAdapter
from app.adapters.output.memory_repository import MemoryRepository

logger = logging.getLogger(__name__)

def execute():
    app = App()
    logger.debug("Init CLI with Memory repository")
    app.resolve(CLIAdapter, [MemoryRepository]).run()
