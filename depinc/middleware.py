from abc import ABC


class Middleware(ABC):
    def before(self, ctx: dict) -> bool:
        return True

    def after(self, ctx: dict, result):
        pass


def apply(middlewares: list, method):
    def wrapper(*args, **kwargs):
        ctx = {"args": args, "kwargs": kwargs}
        for mw in middlewares:
            if not mw().before(ctx):
                print(f"[Middleware bloqueado]: {mw.__name__}")
                return
        result = method(*args, **kwargs)
        for mw in middlewares:
            mw().after(ctx, result)
        return result
    return wrapper
