def only_positive(nums: list[float]) -> list[float]:
    """Возвращает только строго положительные числа, сохраняя порядок."""
    return [n for n in nums if n > 0]


def in_bounds(nums: list[float], low: float, high: float) -> list[float]:
    """Возвращает числа из диапазона [low, high] (границы включительно), сохраняя порядок."""
    return [n for n in nums if low <= n <= high]


def unique_sorted(nums: list[float]) -> list[float]:
    """Возвращает отсортированные по возрастанию значения без дубликатов."""
    return sorted(set(nums))
