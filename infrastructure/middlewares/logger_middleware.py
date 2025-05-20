from .middleware import Middleware

class LoggerMiddleware (Middleware):
    __type__ = "input"
    
    def execute (self, ctx):
        print("Logger...")
        return True