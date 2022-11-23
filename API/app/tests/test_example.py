import pytest

@pytest.fixture
def iwillrunfirst():
    return "I'll run first"

@pytest.mark.parametrize("num1, num2, expectedResult", [
    (1,2,3),
    (2,3,5),
    (5,6,11),
    (7,11,18)
])

def test_example(num1, num2, expectedResult):
    assert sum([num1, num2]) == expectedResult

def test_hulolo(iwillrunfirst):
    print(iwillrunfirst)
    print("I'll run second")
    assert 1 == 1