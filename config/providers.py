from core.ports.output.repository import Repository
from adapters import MemoryFlightRepository

default_providers = {
    Repository: MemoryFlightRepository
}