from app.ports.output.repository import Repository
from app.ports.output.event_dispatcher import EventDispatcher
from app.adapters.output.sqlite_repository import SQLiteRepository
from app.adapters.output.console_event_dispatcher import ConsoleEventDispatcher

bindings = {
    Repository: SQLiteRepository,
    EventDispatcher: ConsoleEventDispatcher,
}

