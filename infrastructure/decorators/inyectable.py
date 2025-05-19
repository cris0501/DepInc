INJECTABLES = {}
INJECTABLE_ALIASES = {}  # (interface, variant) -> class

def inyectable(key=None, variant=None):
    def decorator(cls):
        if key:
            if variant:
                INJECTABLES[cls] = cls
                INJECTABLE_ALIASES[(key, variant)] = cls
            else:
                INJECTABLES[key] = cls
        else:
            INJECTABLES[cls] = cls
        return cls
    return decorator