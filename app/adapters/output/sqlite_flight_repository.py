import sqlite3
from app.ports.output.repository import Repository
from config.paths import paths


class SQLiteFlightRepository(Repository):
    def __init__(self):
        self.conn = sqlite3.connect(paths['root'] / 'database.db')
        self._ensure_table()

    def _ensure_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS flights (
                id TEXT PRIMARY KEY,
                destination TEXT,
                pilot TEXT
            )
        """)
        self.conn.commit()

    def save(self, entity):
        if entity._exists:
            changes = entity.get_dirty()
            if not changes:
                return
            set_clause = ', '.join(f'{k} = :{k}' for k in changes)
            self.conn.execute(
                f"UPDATE flights SET {set_clause} WHERE id = :id",
                {**changes, 'id': entity.id}
            )
        else:
            data = entity.to_dict()
            columns = ', '.join(data)
            placeholders = ', '.join(f':{k}' for k in data)
            self.conn.execute(
                f"INSERT INTO flights ({columns}) VALUES ({placeholders})",
                data
            )
        self.conn.commit()
        entity.sync_original()

    def find_by_id(self, model_class, id_value):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, destination, pilot FROM flights WHERE id = ?", (id_value,))
        row = cursor.fetchone()
        if row:
            columns = [desc[0] for desc in cursor.description]
            return model_class.from_persistence(**dict(zip(columns, row)))
        return None
