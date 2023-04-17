import pytest
from app.calculations import add, subtract, multiply, divide


@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (7, 1, 8),
    (12, 4, 16)
])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected


def test_subtract():
    assert subtract(9, 4) == 5


def test_multiply():
    assert multiply(5, 3) == 15


def test_divide():
    assert divide(10, 5) == 2
