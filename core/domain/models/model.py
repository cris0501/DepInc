class Model:
    def __init__(self, **kwargs):
        # Use basic setter
        super().__setattr__('_attributes', {})
        super().__setattr__('_original', {})
        super().__setattr__('_fillable', set(kwargs.keys()))

        for k, v in kwargs.items():
            """ Create a base model attributes """
            self._attributes[k] = v # All attributes
            self._original[k] = v # Original values

    def __getattr__(self, name):
        """ Use to obj.attr """
        return self._attributes.get(name)

    def __setattr__(self, name, value):
        self._attributes[name] = value

    def __getitem__(self, key):
        """ Use to obj['item'] """
        return self._attributes.get(key)

    def __setitem__(self, key, value):
        self._attributes[key] = value

    def to_dict(self):
        """ Convert attributes to dicc, only one fillable """
        return {k: v for k, v in self._attributes.items() if k in self._fillable}

    def get_dirty(self):
        """ Get attributes with changes and only one fillable """
        return {
            k: v for k, v in self._attributes.items()
            if k in self._fillable and (k not in self._original or self._original[k] != v)
        }

    def sync_original(self):
        """ After save, run sync to update 'original' values """
        self._original = {
            k: v for k, v in self._attributes.items() if k in self._fillable
        }

    def allow(self, *fields):
        """ Allow mark attribute to save """
        self._fillable.update(fields)
