from depinc.plugins.middleware import Middleware


class LoggerMiddleware(Middleware):
    def after(self, ctx, result):
        print(f"[Log] call completed, result: {result}")
