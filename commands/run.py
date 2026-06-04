import logging
import threading
from app.adapters.output.memory_repository import MemoryRepository
from depinc import App
from config.adapters import adapters

logger = logging.getLogger(__name__)

def execute():
    app = App()
    # app.singleton(MemoryRepository)

    threads = [
        threading.Thread(target=adapter_cls().run, daemon=True)
        for adapter_cls in adapters
    ]

    for t in threads:
        t.start()

    for t in threads:
        t.join()
