from abc import ABC
from depinc import context


class Service(ABC):
    def repository_for(self, model_class):
        """
            This method delivery breack hexagonal arquitecture,
            due to that this is implement, then, dev should
            invoque this function manually, simillary to
            hatch in services
        """

        repo_cls = getattr(model_class, '_repository', None)
        if repo_cls:
            repo = context.container._build(repo_cls)
        else:
            repo = self.repository

        repo._migrate(model_class)
        return repo