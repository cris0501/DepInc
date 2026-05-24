from depinc import Middleware


class LoggerMiddleware(Middleware):
    def after(self, ctx, result):
        print(f"[Log] llamada completada, resultado: {result}")
