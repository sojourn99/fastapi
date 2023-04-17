from app.calculations import add, subtract, multiply, divide


def test_add():
    assert add(5, 3) == 8


def test_subtract():
    assert subtract(9, 4) == 5


def test_multiply():
    assert multiply(5, 3) == 15


def test_divide():
    assert divide(10, 5) == 2
