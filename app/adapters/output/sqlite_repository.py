import sqlite3
from app.ports.output.repository import Repository
from config.paths import paths


class SQLiteRepository(Repository):
    def __init__(self):
        print("Starting sqlite repository")
        self.conn = sqlite3.connect(paths['root'] / 'database.db')
        self._migrate()

    def _migrate(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS flights (
                id TEXT PRIMARY KEY,
                destination TEXT,
                pilot TEXT
            )
        """)
        self.conn.commit()

    def save(self, entity):
        table = getattr(entity, "_table", "local")
        pk = getattr(entity, "_pk", "id")
        if entity._exists:
            changes = entity.get_dirty()
            if not changes:
                return
            set_clause = ', '.join(f'{k} = :{k}' for k in changes)
            self.conn.execute(
                f"UPDATE {table} SET {set_clause} WHERE {pk} = :{pk}",
                {**changes, pk: entity[pk]}
            )
        else:
            data = entity.to_dict()
            columns = ', '.join(data)
            placeholders = ', '.join(f':{k}' for k in data)
            self.conn.execute(
                f"INSERT INTO {table} ({columns}) VALUES ({placeholders})",
                data
            )
        self.conn.commit()
        entity.sync_original()

    def find_by_id(self, model_class, id_value):
        table = model_class._table
        pk = model_class._db
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM {table} WHERE {pk} = ?", (id_value,))
        row = cursor.fetchone()
        if row:
            columns = [desc[0] for desc in cursor.description]
            return model_class.from_persistence(**dict(zip(columns, row)))
        return None