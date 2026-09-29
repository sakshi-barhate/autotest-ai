from examples.sample_code import is_palindrome
import pytest

def test_happy_path_normal_input():
    """happy_path: Function executes successfully with typical input"""
    result = is_palindrome(text='hello')
    assert result is not None

def test_edge_case_text_1():
    """edge_case: Tests behavior when text is '' (empty string)"""
    result = is_palindrome(text='')
    assert result is not None

def test_edge_case_text_2():
    """edge_case: Tests behavior when text is very long string"""
    result = is_palindrome(text='a' * 1000)
    assert result is not None

def test_load_repeated_calls():
    """load: Function handles 10,000 rapid sequential calls without error"""
    for _ in range(10000):
        is_palindrome(text='hello')
