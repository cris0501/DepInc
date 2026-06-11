# Full example — escalation guide

Starting from the minimal root structure, this shows how to grow into a full hexagonal architecture using DepInc plugins.

Run from this directory:
```bash
cd examples/full
python3 main.py
```

---

## Step 1 — container_full plugin

Adds: singletons, hooks, circular-dependency detection, config loading, folder scaffolding.

```python
from depinc import App
from depinc.plugins.container_full import plugin as full

app = App()
full.install(app)
```

Generates on first run:
- `config/bindings.py` — manual interface→implementation map
- `config/database.py` — ORM driver config

---

## Step 2 — autobind plugin

Auto-discovers ports (ABCs) and wires their single implementation.
No manual `config/bindings.py` needed when there is exactly one impl per interface.

Add to `depinc/plugins/__init__.py`:
```python
plugins = ["autobind", ...]
```

Generates `config/bindings.py` automatically on each run.

---

## Step 3 — middleware plugin

Wraps service methods with before/after middleware without touching domain code.

Add to `depinc/plugins/__init__.py`:
```python
plugins = [..., "middleware"]
```

Generates `config/middlewares.py`. Example:
```python
# config/middlewares.py
from app.ports.input.flight_service_port import FlightServicePort
from app.middlewares import AuthMiddleware, LoggerMiddleware

middlewares = {
    FlightServicePort: {
        "register_flight": [AuthMiddleware, LoggerMiddleware],
    }
}
```

---

## Step 4 — orm plugin

Provides a `Repository` implementation backed by SQLite or in-memory storage.
Models declare their schema via `_schema`.

Add to `depinc/plugins/__init__.py`:
```python
plugins = [..., "orm"]
```

Configure driver in `config/database.py`:
```python
database = {"driver": "sqlite", "database": "database.db"}
```

---

## Step 5 — hexagonal structure

As the app grows, split `app/` into the standard hexagonal layout:

```
app/
├── ports/
│   ├── input/    ← abstract service interfaces (ABCs)
│   └── output/   ← abstract infrastructure interfaces
├── use_cases/    ← service implementations
├── adapters/
│   ├── input/    ← CLI, HTTP, queue consumers
│   └── output/   ← DB, email, external APIs
├── domain/       ← models, value objects
└── middlewares/  ← before/after hooks
```

Adapters are registered in `config/adapters.py` and run as threads via `commands/run.py`.
