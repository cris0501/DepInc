from depinc import Model

class Flight(Model):
    _schema = {
        'id':          'TEXT PRIMARY KEY',
        'destination': 'TEXT NOT NULL',
        'pilot':       'TEXT',
    }

    # Use _repository is bad practique and break hexagonal arq
    # but due to i want colocation of components, add hatch
    # _repository = SQLiteRepository

    def __init__(self, id: str, destination: str, pilot: str = None):
        super().__init__(id=id, destination=destination, pilot=pilot)
