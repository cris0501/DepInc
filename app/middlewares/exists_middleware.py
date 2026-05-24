from depinc import Middleware


class ExistsMiddleware(Middleware):
    def before(self, ctx) -> bool:
        print("Exists check...")
        return True
