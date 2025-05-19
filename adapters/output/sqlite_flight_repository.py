import sqlite3
from core.ports.output.repository import Repository
from core.domain.models.flight import Flight
from infrastructure.decorators import inyectable

@inyectable(key=Repository, variant='sqlite')
class SQLiteFlightRepository(Repository):
    def __init__(self):#, db_path: str):
        #self.conn = sqlite3.connect(db_path)
        #self._ensure_table()
        print('Load SQLite')

    def _ensure_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS flights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                flight_id TEXT,
                destination TEXT
            )
        """)
        self.conn.commit()

    def save(self, flight: Flight):
        data = flight.to_dict()

        if getattr(flight, "id", None) is None:
            # INSERT
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO flights (flight_id, destination) VALUES (?, ?)",
                (data.get("flight_id"), data.get("destination"))
            )
            self.conn.commit()
            flight.id = cursor.lastrowid  # asignar id
            flight.sync_original()
        else:
            # UPDATE
            cursor = self.conn.cursor()
            changes = flight.get_dirty()
            if changes:
                sets = ", ".join(f"{k}=?" for k in changes)
                values = list(changes.values()) + [flight.id]
                cursor.execute(
                    f"UPDATE flights SET {sets} WHERE id=?",
                    values
                )
                self.conn.commit()
                flight.sync_original()

    def find_by_id(self, id_value):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, flight_id, destination FROM flights WHERE id = ?", (id_value,))
        row = cursor.fetchone()
        if row:
            return Flight(id=row[0], flight_id=row[1], destination=row[2])
        return None
