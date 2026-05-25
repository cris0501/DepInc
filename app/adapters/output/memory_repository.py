from app.ports.output.repository import Repository


class MemoryRepository(Repository):
    def __init__(self):
        self._store = {}
        print("Starting memory repository")

    def save(self, entity):
        db = getattr(entity, "_db", "local")
        table = getattr(entity, "_table", "local")
        pk = getattr(entity, "_pk", "id")
        self._store.setdefault(db, {}).setdefault(table, {})[pk] = entity

    def find_by_id(self, entity, id):
        return self._store.get(entity._db, {}).get(entity._table, {}).get(id)
