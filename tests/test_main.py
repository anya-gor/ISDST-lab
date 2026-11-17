import pytest

from main import in_bounds, only_positive, unique_sorted


# ---------- only_positive ----------

def test_only_positive_keeps_positive_numbers_in_order():
    assert only_positive([3, -1, 2.5, 7]) == [3, 2.5, 7]


def test_only_positive_zero_is_not_positive():
    assert only_positive([0, 0.0, 1]) == [1]


def test_only_positive_empty_list():
    assert only_positive([]) == []


def test_only_positive_all_negative_gives_empty():
    assert only_positive([-1, -0.5, -100]) == []


def test_only_positive_does_not_mutate_input():
    data = [1, -2, 3]
    only_positive(data)
    assert data == [1, -2, 3]


# ---------- in_bounds ----------

def test_in_bounds_bounds_are_inclusive():
    assert in_bounds([1, 2, 3, 4, 5], 2, 4) == [2, 3, 4]


def test_in_bounds_keeps_order_and_duplicates():
    assert in_bounds([5, 3, 3, 1], 1, 5) == [5, 3, 3, 1]


def test_in_bounds_nothing_in_range():
    assert in_bounds([1, 2, 3], 10, 20) == []


def test_in_bounds_low_equals_high():
    assert in_bounds([1, 2, 2, 3], 2, 2) == [2, 2]


def test_in_bounds_empty_list():
    assert in_bounds([], 0, 10) == []


def test_in_bounds_low_greater_than_high_gives_empty():
    assert in_bounds([1, 2, 3], 5, 1) == []


# ---------- unique_sorted ----------

def test_unique_sorted_removes_duplicates_and_sorts():
    assert unique_sorted([3, 1, 2, 3, 1]) == [1, 2, 3]


def test_unique_sorted_empty_list():
    assert unique_sorted([]) == []


def test_unique_sorted_handles_negatives_and_floats():
    assert unique_sorted([2.5, -1, 2.5, 0, -1]) == [-1, 0, 2.5]


def test_unique_sorted_treats_int_and_float_equal_values_as_one():
    assert unique_sorted([1, 1.0, 2]) == [1, 2]


def test_unique_sorted_does_not_mutate_input():
    data = [3, 1, 3]
    unique_sorted(data)
    assert data == [3, 1, 3]
