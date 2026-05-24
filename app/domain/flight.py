from depinc import Model


class Flight(Model):
    _table = 'flights'

    def __init__(self, id: str, destination: str, pilot: str = None):
        super().__init__(id=id, destination=destination, pilot=pilot)
