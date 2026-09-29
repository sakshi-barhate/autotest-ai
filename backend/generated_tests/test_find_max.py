from examples.sample_code import find_max
import pytest

def test_happy_path_normal_input():
    """happy_path: Function executes successfully with typical input"""
    result = find_max(numbers=[1, 2, 3])
    assert result is not None

def test_edge_case_numbers_1():
    """edge_case: Tests behavior when numbers is [] (empty list)"""
    result = find_max(numbers=[])
    assert result is not None

def test_edge_case_numbers_2():
    """negative: Tests behavior when numbers is None (missing value)"""
    with pytest.raises((ValueError, TypeError)):
        find_max(numbers=None)

def test_load_repeated_calls():
    """load: Function handles 10,000 rapid sequential calls without error"""
    for _ in range(10000):
        find_max(numbers=[1, 2, 3])
