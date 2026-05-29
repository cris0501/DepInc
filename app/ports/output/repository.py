from abc import ABC, abstractmethod


class Repository(ABC):
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if 'find_by_id' in cls.__dict__:
            original = cls.__dict__['find_by_id']
            def wrapped(self, model_class, id_value, _fn=original):
                result = _fn(self, model_class, id_value)
                if result is not None and not result._exists:
                    result = model_class.from_persistence(**result.to_dict())
                return result
            cls.find_by_id = wrapped

    @abstractmethod
    def save(self, entity):
        pass

    @abstractmethod
    def find_by_id(self, model_class, id_value):
        pass

    def _migrate(self, entity) -> None:
        ...