# app/ports/in/adapter_interface.py
from abc import ABC, abstractmethod

class InputAdapter(ABC):
    def run(self):
        print("Run input adapter")
    
    def shutdown(self):
        print("Shutdown input adapter")