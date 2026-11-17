def calculate_cost(duration_seconds):
    if duration_seconds < 0:
        raise ValueError("duration_seconds must be >= 0")
    minutes = -(-duration_seconds // 60)  # округление вверх без float
    return 50 + minutes * 8
