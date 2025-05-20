from .middleware import Middleware

class ExistsMiddleware (Middleware):
    __type__ = "input"
    
    def execute (self, ctx):
        print("Exists check...")
        return True