from app.ports.output import Repository

class Service:
    _container = None 

    def __init__(self, repository: Repository):
        self.repository = repository

    def repository_for(self, model_class):
        """
            This method delivery breack hexagonal arquitecture,
            due to that this is implement, then, dev should
            invoque this function manually, simillary to
            hatch in services
        """
        repo_cls = getattr(model_class, '_repository', None)
        if repo_cls:
            return self._container._build(repo_cls)
        return self.repository        