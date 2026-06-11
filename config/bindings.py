# Explicit bindings are only needed when a port has multiple implementations
# (ambiguity) or you want to force one different from the convention.
# The 'autobind' plugin automatically binds each interface to its single
# discovered implementation under app/.
#
# Example:
# from depinc import Repository
# from app.adapters.output import MemoryRepository
#
# bindings = {Repository: MemoryRepository}

bindings = {}
