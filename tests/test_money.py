import pytest
from hypothesis import given
from hypothesis.strategies import builds, floats, integers, just

from pymoney import Money


@pytest.mark.parametrize(
    ("money_fixture_name", "expected_str"),
    (("dollars_0", "0.00$"), ("dollars_5", "5.00$"), ("dollars_negative_5", "-5.00$"), ("euros_0_50", "0.50€")),
)
def test_money_string_representation(
    money_fixture_name: str, expected_str: str, request: pytest.FixtureRequest
) -> None:
    money: Money = request.getfixturevalue(money_fixture_name)

    assert str(money) == expected_str


@pytest.mark.parametrize(
    ("first_amount_fixture_name", "second_amount_fixture_name", "expected_money_fixture_name"),
    (
        ("dollars_0", "dollars_5", "dollars_5"),
        ("dollars_5", "dollars_5", "dollars_10"),
        ("dollars_5", "dollars_negative_5", "dollars_0"),
        ("euros_0_50", "euros_0_50", "euros_1"),
    ),
)
def test_money_addition(
    first_amount_fixture_name: str,
    second_amount_fixture_name: str,
    expected_money_fixture_name: str,
    request: pytest.FixtureRequest,
) -> None:
    first_amount: Money = request.getfixturevalue(first_amount_fixture_name)
    second_amount: Money = request.getfixturevalue(second_amount_fixture_name)
    expected_money: Money = request.getfixturevalue(expected_money_fixture_name)

    assert first_amount + second_amount == expected_money


@pytest.mark.parametrize(
    ("first_amount_fixture_name", "second_amount_fixture_name", "expected_money_fixture_name"),
    (
        ("dollars_5", "dollars_0", "dollars_5"),
        ("dollars_5", "dollars_5", "dollars_0"),
        ("dollars_5", "dollars_negative_5", "dollars_10"),
        ("euros_2", "euros_1", "euros_1"),
    ),
)
def test_money_subtraction(
    first_amount_fixture_name: str,
    second_amount_fixture_name: str,
    expected_money_fixture_name: str,
    request: pytest.FixtureRequest,
) -> None:
    first_amount: Money = request.getfixturevalue(first_amount_fixture_name)
    second_amount: Money = request.getfixturevalue(second_amount_fixture_name)
    expected_money: Money = request.getfixturevalue(expected_money_fixture_name)

    assert first_amount - second_amount == expected_money


@pytest.mark.parametrize(
    ("money_fixture_name", "expected_money_fixture_name"),
    (("dollars_0", "dollars_0"), ("dollars_negative_5", "dollars_5"), ("dollars_5", "dollars_negative_5")),
)
def test_negative_money(
    money_fixture_name: str, expected_money_fixture_name: str, request: pytest.FixtureRequest
) -> None:
    money: Money = request.getfixturevalue(money_fixture_name)
    expected_money: Money = request.getfixturevalue(expected_money_fixture_name)

    assert -money == expected_money


@pytest.mark.parametrize(
    ("money_fixture_name", "expected"),
    (("dollars_0", False), ("dollars_5", True), ("dollars_negative_5", True), ("euros_1", True)),
)
def test_boolean_value_money(money_fixture_name: str, expected: bool, request: pytest.FixtureRequest) -> None:
    money: Money = request.getfixturevalue(money_fixture_name)

    assert bool(money) == expected


@pytest.mark.parametrize(
    ("money_fixture_name", "expected_money_fixture_name"),
    (("dollars_0", "dollars_0"), ("dollars_negative_5", "dollars_5"), ("euros_1", "euros_1")),
)
def test_absolute_money(
    money_fixture_name: str, expected_money_fixture_name: str, request: pytest.FixtureRequest
) -> None:
    money: Money = request.getfixturevalue(money_fixture_name)
    expected_money: Money = request.getfixturevalue(expected_money_fixture_name)

    assert abs(money) == expected_money


@pytest.mark.parametrize(
    ("money_fixture_name", "scalar", "expected_money_fixture_name"),
    (
        ("dollars_0", 0.8, "dollars_0"),
        ("dollars_5", 0.0, "dollars_0"),
        ("dollars_10", 0.5, "dollars_5"),
        ("dollars_negative_5", -1.0, "dollars_5"),
        ("euros_1", 1.0, "euros_1"),
    ),
)
def test_money_multiplication(
    money_fixture_name: str, scalar: float, expected_money_fixture_name: str, request: pytest.FixtureRequest
) -> None:
    money: Money = request.getfixturevalue(money_fixture_name)
    expected_money: Money = request.getfixturevalue(expected_money_fixture_name)

    assert money * scalar == expected_money


@pytest.mark.parametrize(
    ("money_fixture_name", "scalar", "expected_money_fixture_name"),
    (
        ("dollars_0", 0.8, "dollars_0"),
        ("dollars_10", 2.0, "dollars_5"),
        ("dollars_negative_5", -1.0, "dollars_5"),
        ("euros_1", 1.0, "euros_1"),
    ),
)
def test_money_division(
    money_fixture_name: str, scalar: float, expected_money_fixture_name: str, request: pytest.FixtureRequest
) -> None:
    money: Money = request.getfixturevalue(money_fixture_name)
    expected_money: Money = request.getfixturevalue(expected_money_fixture_name)

    assert money / scalar == expected_money


def test_compare_money(dollars_0: Money, dollars_negative_5: Money, dollars_5: Money) -> None:
    assert dollars_0 == Money(0_00)
    assert dollars_0 > dollars_negative_5
    assert dollars_0 < dollars_5


@given(builds(Money, integers()), builds(Money, integers()))
def test_money_instance_after_operation(first_amount: Money, second_amount: Money) -> None:
    assert isinstance(first_amount + second_amount, Money)
    assert isinstance(first_amount - second_amount, Money)
    assert isinstance(-first_amount, Money)
    assert isinstance(abs(first_amount), Money)
    assert isinstance(first_amount * 0.5, Money)
    assert isinstance(first_amount / 2.0, Money)


@given(builds(Money, integers(), just("€")), builds(Money, integers(), just("€")))
def test_money_currency_after_operation(first_amount: Money, second_amount: Money) -> None:
    third_amount = first_amount + second_amount
    assert third_amount.currency == first_amount.currency


@given(builds(Money, integers()), builds(Money, integers()))
def test_addition_commutative_property(first_amount: Money, second_amount: Money) -> None:
    assert first_amount + second_amount == first_amount + second_amount


@given(builds(Money, integers()), builds(Money, integers()))
def test_addition_commutative_property_with_negative_values(first_amount: Money, second_amount: Money) -> None:
    assert first_amount - second_amount == -second_amount + first_amount


@given(builds(Money, integers()), floats(min_value=-100, max_value=100))
def test_multiplication_commutative_property(money: Money, scalar: float) -> None:
    assert money * scalar == scalar * money
