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
        return Money(self.cents + other.cents, self.currency)

    def __sub__(self, other: Money) -> Money:
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
        return self.cents < other.cents
