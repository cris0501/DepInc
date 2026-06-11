import logging
import threading
from depinc import App
from app.adapter import AppAdapter

logger = logging.getLogger(__name__)


def execute():
    app = App()

    threads = [
        threading.Thread(target=app.resolve(AppAdapter).run, daemon=True)
    ]

    for t in threads:
        t.start()

    for t in threads:
        t.join()
