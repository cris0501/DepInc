def filter_providers_for(context: str, providers: dict) -> dict:
    rules = {
        "use_case": lambda p: (
            "adapters.out" in p["path"]
            or "core.ports" in p["path"]
            or "infra." in p["path"]
        ),
        "adapter": lambda p: (
            "app.use_cases" in p["path"]
            or "core.use_cases" in p["path"]
        ),
        "service": lambda p: True,  # servicios pueden tener todo (o cambia según tu criterio)
    }

    rule = rules.get(context)
    if not rule:
        return {}

    return {
        k: v for k, v in providers.items() if rule(v)
    }