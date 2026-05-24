from depinc import App
from app.adapters.input.cli_adapter import CLIAdapter
from app.adapters.output.memory_repository import MemoryRepository


def execute():
    app = App()
    app.resolve(CLIAdapter, [MemoryRepository]).run()
