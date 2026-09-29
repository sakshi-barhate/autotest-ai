from examples.sample_code import calculate_discount
import pytest

def test_valid_discount_applies_correctly():
    """happy_path: Returns 90"""
    result = calculate_discount(price=100, discount_percent=10)
    assert result is not None

def test_zero_discount():
    """happy_path: Returns original price unchanged"""
    result = calculate_discount(price=100, discount_percent=0)
    assert result is not None

def test_full_discount():
    """edge_case: Returns 0"""
    result = calculate_discount(price=100, discount_percent=100)
    assert result is not None

def test_zero_price():
    """edge_case: Returns 0"""
    result = calculate_discount(price=0, discount_percent=50)
    assert result is not None

def test_negative_discount():
    """negative: Raises ValueError"""
    with pytest.raises(ValueError):
        calculate_discount(price=100, discount_percent=-10)

def test_negative_price():
    """negative: Raises ValueError"""
    with pytest.raises(ValueError):
        calculate_discount(price=-50, discount_percent=10)

def test_high_volume_calls():
    """load: Function handles 10,000 rapid sequential calls without error"""
    for _ in range(10000):
        calculate_discount(price=100, discount_percent=10)
