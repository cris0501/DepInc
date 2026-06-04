import sqlite3
from depinc import Repository
from config.paths import paths


class SQLiteRepository(Repository):
    def __init__(self):
        print("Starting sqlite")
        self.conn = sqlite3.connect(paths['root'] / 'database.db')

    def _migrate(self, entity):
        table = self.get_table(entity)
        schema = getattr(entity, '_schema', None)
        if schema is None:
            raise ValueError(f"{entity.__name__} no define _schema")

        columns = ',\n    '.join(f"{col} {definition}" for col, definition in schema.items())
        
        self.conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {table} (
                {columns}
            )
        """)
        self.conn.commit()

    def save(self, entity):
        self._migrate(entity)
        table = self.get_table(entity)
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
            print("Update model")
        else:
            data = entity.to_dict()
            columns = ', '.join(data)
            placeholders = ', '.join(f':{k}' for k in data)
            self.conn.execute(
                f"INSERT INTO {table} ({columns}) VALUES ({placeholders})",
                data
            )
            print("Create model")
        self.conn.commit()
        entity.sync_original()

    def find_by_id(self, model, id_value):
        table = self.get_table(model)
        pk = getattr(model, '_pk', None)
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM {table} WHERE {pk} = ?", (id_value,))
        row = cursor.fetchone()
        if row:
            columns = [desc[0] for desc in cursor.description]
            return model(**dict(zip(columns, row)))
        return None

    def get_table(self, entity):
        name = entity.__name__ if isinstance(entity, type) else type(entity).__name__
        return getattr(entity, '_table', None) or name.lower() + 's'