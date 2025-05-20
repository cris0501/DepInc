def middleware(middlewares):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            ctx = {"args": args, "kwargs": kwargs, "self": self}
            for mw in middlewares:
                instance = mw() if isinstance(mw, type) else mw # Create instance or use function

                passed = instance.execute(ctx)
                if not passed:
                    print(f"[Middleware bloqueado]: {instance.__class__.__name__}")
                    return
            return func(self, *args, **kwargs)
        return wrapper
    return decorator
