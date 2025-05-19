from core.domain.models.model import Model

class Flight(Model):
    def __init__(self, _id: str, destination: str, pilot: str = None):
        super().__init__(id=_id, destination=destination, pilot=pilot) # Set init attributes