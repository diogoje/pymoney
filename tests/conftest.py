import pytest

from pymoney import Money


@pytest.fixture
def dollars_0() -> Money:
    return Money(0_00)


@pytest.fixture
def dollars_5() -> Money:
    return Money(5_00)


@pytest.fixture
def dollars_10() -> Money:
    return Money(10_00)


@pytest.fixture
def dollars_negative_5() -> Money:
    return Money(-5_00)


@pytest.fixture
def euros_0_50() -> Money:
    return Money(50, "€")


@pytest.fixture
def euros_1() -> Money:
    return Money(1_00, "€")


@pytest.fixture
def euros_2() -> Money:
    return Money(2_00, "€")
