from app.ports.output.repository import Repository


class MemoryRepository(Repository):
    def __init__(self):
        self._store = {}
        print("Starting memory repository")

    def save(self, entity):
        db = getattr(entity, "_db", "local")
        table = getattr(entity, "_table", "local")
        self._store.setdefault(db, {}).setdefault(table, {})[entity.id] = entity

    def find_by_id(self, entity_class, id):
        return self._store.get(entity_class._db, {}).get(entity_class._table, {}).get(id)
