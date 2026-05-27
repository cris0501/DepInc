import logging
import threading
from depinc import App, registry
from depinc import Service
from config.adapters import adapters

logger = logging.getLogger(__name__)

def execute():
    app = App()
    registry.set_container(app)
    Service._container = app

    threads = [
        threading.Thread(target=adapter_cls(app).run, daemon=True)
        for adapter_cls in adapters
    ]

    for t in threads:
        t.start()

    for t in threads:
        t.join()
