import logging
import threading
from depinc import App
from config.adapters import adapters
from depinc.plugins.container_full import plugin as full
from app.adapters.output.memory_repository import MemoryRepository

logger = logging.getLogger(__name__)

def execute():
    app = App()
    full.install(app)
    # app.singleton(MemoryRepository)

    threads = [
        threading.Thread(target=adapter_cls().run, daemon=True)
        for adapter_cls in adapters
    ]

    for t in threads:
        t.start()

    for t in threads:
        t.join()
