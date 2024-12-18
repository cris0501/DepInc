#!/bin/python
from abc import ABC, abstractmethod

class Provider(ABC):
    @abstractmethod
    def create(self):
        pass
