import sqlite3
from core.ports.output.repository import Repository
from core.domain.models.flight import Flight
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

    def save(self, flight: Flight):
        changes = flight.get_dirty()
        if not changes:
            return

        self.conn.execute(
            "INSERT INTO flights (id, destination, pilot) VALUES (:id, :destination, :pilot) "
            "ON CONFLICT(id) DO UPDATE SET destination=excluded.destination, pilot=excluded.pilot",
            {"id": flight.id, "destination": flight.destination, "pilot": flight.pilot}
        )
        self.conn.commit()
        flight.sync_original()

    def find_by_id(self, id_value):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, destination, pilot FROM flights WHERE id = ?", (id_value,))
        row = cursor.fetchone()
        if row:
            flight = Flight(_id=row[0], destination=row[1], pilot=row[2])
            flight.sync_original()
            return flight
        return None
