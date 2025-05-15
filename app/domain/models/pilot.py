from app.domain.models.model import Model

class Pilot(Model):
    def __init__(self, name: str):
        super().__init__(name=name) # Set init attributes