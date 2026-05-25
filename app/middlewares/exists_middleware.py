import logging
from depinc import Middleware, registry

logger = logging.getLogger(__name__)

class ExistsMiddleware(Middleware):
    def __init__(self, model=None):
        self.model = model

    def before(self, ctx) -> bool:
        entity_id = ctx["args"][0]
        repo_cls = getattr(self.model, '_repository', None)
        repo = registry.resolve_repo(repo_cls)
        repo._migrate(self.model)
        result = repo.find_by_id(self.model, entity_id)
        if not result:
            logger.debug(f"Flight {entity_id} not found")
            return False
        return True
