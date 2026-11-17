def calculate_cost(duration_seconds):
    minutes = round(duration_seconds / 60)
    return 50 + minutes * 8
