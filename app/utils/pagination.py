def clamp_per_page(value, default=20, maximum=100):
    try:
        v = int(value)
    except Exception:
        return default
    return max(1, min(v, maximum))
