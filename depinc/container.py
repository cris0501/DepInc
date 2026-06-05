# depinc/container.py
import inspect
from pathlib import Path
from depinc import context


class Container:
    def __init__(self):
        context.container = self
        self._bindings = {}
        self.auto_discover()

    def provider(self, key, cls):
        self._bindings[key] = cls

    def resolve(self, key):
        return self._build(key)

    def _build(self, key):
        cls = self._bindings.get(key, key)
        sig = inspect.signature(cls.__init__)
        args = []
        for param in list(sig.parameters.values())[1:]:
            if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
                continue
            args.append(self._build(param.annotation))
        print(f"Class: {args}")
        return cls(*args)

    def auto_discover(self):
        for path in ["app/use_cases", "app/ports/input", "app/ports/output"]:
            self._scan_path(path)

    def _scan_path(self, rel_path):
        base = Path(rel_path)
        if not base.exists():
            return
        for file in base.rglob("*.py"):
            if file.name.startswith("_"):
                continue
            module_path = ".".join(file.with_suffix("").parts)
            module = __import__(module_path, fromlist=[""])
            for name in dir(module):
                obj = getattr(module, name)
                if inspect.isclass(obj) and not inspect.isabstract(obj):
                    self._bindings[obj] = obj
