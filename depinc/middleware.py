from abc import ABC


class Middleware(ABC):
    def before(self, ctx: dict) -> bool:
        return True

    def after(self, ctx: dict, result):
        pass


def apply(middlewares: list, method):
    def wrapper(*args, **kwargs):
        ctx = {"args": args, "kwargs": kwargs}
        
        instances = [mw() if isinstance(mw, type) else mw for mw in middlewares]
        
        for mw in instances:
            if not mw.before(ctx):
                print(f"[Middleware blocked]: {type(mw).__name__}")
                return
        
        result = method(*args, **kwargs)
        
        for mw in instances:
            mw.after(ctx, result)
        
        return result
    return wrapper
