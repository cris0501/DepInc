from depinc import Model
from app.adapters.output import SQLiteRepository

class Flight(Model):
    _table = 'flights'
    _repository = SQLiteRepository

    def __init__(self, id: str, destination: str, pilot: str = None):
        super().__init__(id=id, destination=destination, pilot=pilot)
