from depinc import Model
# from app.adapters.output import SQLiteRepository

class Pilot(Model):
    _table = "flights"
    _schema = {
        'id':          'TEXT PRIMARY KEY',
        'destination': 'TEXT NOT NULL',
        'pilot':       'TEXT',
    }

    # Use _repository is bad practique and break hexagonal arq
    # but due to i want colocation of components, add hatch
    # _repository = SQLiteRepository

    def __init__(self, name: str):
        super().__init__(name=name)
