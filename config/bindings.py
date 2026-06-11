# Explicit bindings are only needed when a port has multiple implementations
# (ambiguity) or you want to force one different from the convention.
# The 'autobind' plugin automatically binds each interface to its single
# discovered implementation under app/.
#
# Example (force a driver regardless of config/database.py):
# from depinc import Repository
# from depinc.plugins.orm.drivers.memory import MemoryRepository
#
# bindings = {Repository: MemoryRepository}

bindings = {}
