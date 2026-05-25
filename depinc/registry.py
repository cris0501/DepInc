_repos: dict = {}
_container = None

def set_container(container):
    global _container
    _container = container

def resolve_repo(repo_cls):
    if repo_cls not in _repos:
        _repos[repo_cls] = _container._build(repo_cls)
    return _repos[repo_cls]