import pytest
from hypothesis import given
from hypothesis.strategies import builds, integers

from pymoney import Money


@pytest.mark.parametrize(
    ("money", "expected"),
    (("dollars_0", "0.00$"), ("dollars_5", "5.00$"), ("dollars_negative_5", "-5.00$"), ("euros_0_50", "0.50€")),
)
def test_money_string_representation(money: str, expected: str, request: pytest.FixtureRequest) -> None:
    assert str(request.getfixturevalue(money)) == expected


@pytest.mark.parametrize(
    ("first_amount", "second_amount", "expected"),
    (
        ("dollars_0", "dollars_5", "dollars_5"),
        ("dollars_5", "dollars_5", "dollars_10"),
        ("dollars_5", "dollars_negative_5", "dollars_0"),
        ("euros_0_50", "euros_0_50", "euros_1"),
    ),
)
def test_money_addition(first_amount: str, second_amount: str, expected: str, request: pytest.FixtureRequest) -> None:
    assert request.getfixturevalue(first_amount) + request.getfixturevalue(second_amount) == request.getfixturevalue(
        expected
    )


@pytest.mark.parametrize(
    ("first_amount", "second_amount", "expected"),
    (
        ("dollars_5", "dollars_0", "dollars_5"),
        ("dollars_5", "dollars_5", "dollars_0"),
        ("dollars_5", "dollars_negative_5", "dollars_10"),
        ("euros_2", "euros_1", "euros_1"),
    ),
)
def test_money_subtraction(
    first_amount: str, second_amount: str, expected: str, request: pytest.FixtureRequest
) -> None:
    assert request.getfixturevalue(first_amount) - request.getfixturevalue(second_amount) == request.getfixturevalue(
        expected
    )


@pytest.mark.parametrize(
    ("money", "expected"),
    (("dollars_0", "dollars_0"), ("dollars_negative_5", "dollars_5"), ("dollars_5", "dollars_negative_5")),
)
def test_negative_money(money: str, expected: str, request: pytest.FixtureRequest) -> None:
    assert -request.getfixturevalue(money) == request.getfixturevalue(expected)


@pytest.mark.parametrize(
    ("money", "expected"), (("dollars_0", False), ("dollars_5", True), ("dollars_negative_5", True), ("euros_1", True))
)
def test_boolean_value_money(money: str, expected: bool, request: pytest.FixtureRequest) -> None:
    assert bool(request.getfixturevalue(money)) == expected


@pytest.mark.parametrize(
    ("money", "expected"), (("dollars_0", "dollars_0"), ("dollars_negative_5", "dollars_5"), ("euros_1", "euros_1"))
)
def test_absolute_money(money: str, expected: str, request: pytest.FixtureRequest) -> None:
    assert abs(request.getfixturevalue(money)) == request.getfixturevalue(expected)


@given(builds(Money, integers()), builds(Money, integers()))
def test_money_instance_after_addition(first_amount: Money, second_amount: Money) -> None:
    assert isinstance(first_amount + second_amount, Money)


@given(builds(Money, integers()), builds(Money, integers()))
def test_addition_commutative_property(first_amount: Money, second_amount: Money) -> None:
    assert first_amount + second_amount == first_amount + second_amount


@given(builds(Money, integers()), builds(Money, integers()))
def test_addition_commutative_property_with_negative_values(first_amount: Money, second_amount: Money) -> None:
    assert first_amount - second_amount == -second_amount + first_amount
