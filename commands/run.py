import logging
from depinc import App
from app.adapters.input.cli_adapter import CLIAdapter
from depinc import Service

logger = logging.getLogger(__name__)

def execute():
    app = App()

    Service._container = app 

    app.resolve(CLIAdapter).run()
