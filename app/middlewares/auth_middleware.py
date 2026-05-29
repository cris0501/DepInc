from depinc.plugins.middleware import Middleware


class AuthMiddleware(Middleware):
    def before(self, ctx) -> bool:
        print("Auth check...")
        return True
