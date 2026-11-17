def only_positive(nums: list[float]) -> list[float]:
    result = []
    for n in nums:
        if n > 0:
            result.append(n)
    return result


def in_bounds(nums: list[float], low: float, high: float) -> list[float]:
    result = []
    for n in nums:
        if n >= low and n <= high:
            result.append(n)
    return result


def unique_sorted(nums: list[float]) -> list[float]:
    result = []
    for n in sorted(nums):
        if n not in result:
            result.append(n)
    return result
