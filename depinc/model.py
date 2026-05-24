class Model:
    def __init__(self, **kwargs):
        super().__setattr__('_attributes', {})
        super().__setattr__('_dirty', set())
        super().__setattr__('_fillable', set(kwargs.keys()))
        super().__setattr__('_exists', False)

        for k, v in kwargs.items():
            self._attributes[k] = v
            self._dirty.add(k)

    @classmethod
    def from_persistence(cls, **kwargs):
        instance = cls(**kwargs)
        instance._dirty.clear()
        object.__setattr__(instance, '_exists', True)
        return instance

    def __getattr__(self, name):
        return self._attributes.get(name)

    def __setattr__(self, name, value):
        self._attributes[name] = value
        self._dirty.add(name)

    def __getitem__(self, key):
        return self._attributes.get(key)

    def __setitem__(self, key, value):
        self._attributes[key] = value
        self._dirty.add(key)

    def to_dict(self):
        return {k: v for k, v in self._attributes.items() if k in self._fillable}

    def get_dirty(self):
        return {k: self._attributes[k] for k in self._dirty if k in self._fillable}

    def sync_original(self):
        self._dirty.clear()
        object.__setattr__(self, '_exists', True)

    def allow(self, *fields):
        self._fillable.update(fields)
