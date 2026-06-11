from ..Repository import Repository


class MemoryRepository(Repository):
    def __init__(self):
        self._store = {}

    def save(self, entity):
        db = getattr(entity, "_db", "local")
        table = getattr(entity, "_table", "local")
        pk = getattr(entity, "_pk", "id")
        self._store.setdefault(db, {}).setdefault(table, {})[entity[pk]] = entity

    def find_by_id(self, entity, id):
        db = getattr(entity, "_db", "local")
        table = getattr(entity, "_table", "local")
        return self._store.get(db, {}).get(table, {}).get(id)
