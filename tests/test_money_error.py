import pytest

from pymoney import Money
from pymoney.money import CurrencyError, MoneyTypeError, validate_currency, validate_money_type


def test_money_type_error(dollars_0: Money) -> None:
    validate_money_type(dollars_0)

    with pytest.raises(MoneyTypeError):
        validate_money_type(10_00)


@pytest.mark.parametrize(
    ("money_fixture_name", "expected_currency", "wrong_currency"), (("dollars_0", "$", "€"), ("euros_1", "€", "$"))
)
def test_currency_error(
    money_fixture_name: str, expected_currency: str, wrong_currency: str, request: pytest.FixtureRequest
) -> None:
    money: Money = request.getfixturevalue(money_fixture_name)

    validate_currency(money, expected_currency)

    with pytest.raises(CurrencyError):
        validate_currency(money, wrong_currency)


def test_money_methods_raising_errors(dollars_10: Money, euros_1: Money) -> None:
    with pytest.raises(MoneyTypeError):
        dollars_10 + 1_00

    with pytest.raises(CurrencyError):
        dollars_10 - euros_1

    with pytest.raises(MoneyTypeError):
        dollars_10 > 1_00
