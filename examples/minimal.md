# Minimal usage

The root project is the minimal starting point.

`app/adapter.py` contains the entry point — a class extending `Adapter` with a `run()` method.
`commands/run.py` imports it directly and the container resolves it with DI.

## How resolve works

`App()` scans `app/` and registers every non-abstract class as itself:

```python
_bindings[GreeterService] = GreeterService
```

When you call `app.resolve(GreeterService)`, the container reads `__init__` type annotations
and builds each dependency recursively — no manual wiring needed.

```python
class ReportService:
    def __init__(self, mailer: MailService, db: DbService):
        ...

app.resolve(ReportService)  # builds MailService and DbService automatically
```

## Default adapter

`app/adapter.py` is where you start. Replace `AppAdapter` with your own logic
or add more adapters and wire them in `commands/run.py`.

```python
from depinc.adapter import Adapter

class AppAdapter(Adapter):
    def run(self):
        print("Hello from DepInc!")
```
