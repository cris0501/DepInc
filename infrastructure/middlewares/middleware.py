def middleware(middlewares):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            """ Create and execute middleware before execute use case """
            ctx = {"args": args, "kwargs": kwargs, "self": self}
            for mw in middlewares:
                passed = mw(ctx) if callable(mw) else mw.handle(ctx)
                if not passed:
                    print(f"[Middleware bloqueado]: {mw}")
                    return
            
            return func(self, *args, **kwargs)
        return wrapper
    return decorator