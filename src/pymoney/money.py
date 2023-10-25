from __future__ import annotations

from dataclasses import dataclass
from functools import total_ordering


@dataclass
@total_ordering
class Money:
    cents: int
    currency: str = "$"

    def __str__(self) -> str:
        return f"{self.cents / 100:.2f}{self.currency}"

    def __add__(self, other: Money) -> Money:
        validate_money(other, self.currency)
        return Money(self.cents + other.cents, self.currency)

    def __sub__(self, other: Money) -> Money:
        validate_money(other, self.currency)
        return Money(self.cents - other.cents, self.currency)

    def __neg__(self) -> Money:
        return Money(-self.cents, self.currency)

    def __bool__(self) -> bool:
        return bool(self.cents)

    def __abs__(self) -> Money:
        return Money(abs(self.cents), self.currency)

    def __mul__(self, scalar: float) -> Money:
        return Money(int(self.cents * scalar), self.currency)

    def __rmul__(self, scalar: float) -> Money:
        return self * scalar

    def __truediv__(self, scalar: float) -> Money:
        return Money(int(self.cents / scalar), self.currency)

    def __lt__(self, other: Money) -> bool:
        validate_money(other, self.currency)
        return self.cents < other.cents


class MoneyTypeError(Exception):
    ...


class CurrencyError(Exception):
    ...


def validate_money_type(money: Money) -> None:
    if not isinstance(money, Money):
        raise MoneyTypeError(f"Expected an instance of Money, but got an object of type {type(money).__name__}.")


def validate_currency(money: Money, expected_currency: str) -> None:
    if money.currency != expected_currency:
        raise CurrencyError(
            f"Expected a Money object with the currency '{expected_currency}', but found '{money.currency}'."
        )


def validate_money(money: Money, expected_currency: str) -> None:
    validate_money_type(money)
    validate_currency(money, expected_currency)
