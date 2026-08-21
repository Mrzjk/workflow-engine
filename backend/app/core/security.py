def redact(value: object) -> object:
    if isinstance(value, dict): return {k: ("***" if "key" in k.lower() or "token" in k.lower() else redact(v)) for k,v in value.items()}
    return value
