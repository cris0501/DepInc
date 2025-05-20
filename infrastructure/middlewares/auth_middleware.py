from .middleware import Middleware

class AuthMiddleware (Middleware):
    __type__ = "input"
    
    def execute (self, ctx):
        print("Auth check...")
        return True