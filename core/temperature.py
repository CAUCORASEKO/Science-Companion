from decimal import Decimal


ABSOLUTE_ZERO = {"celsius": Decimal("-273.15"), "fahrenheit": Decimal("-459.67"), "kelvin": Decimal("0")}


def to_celsius(value: Decimal, unit: str) -> Decimal:
    if unit == "celsius": return value
    if unit == "fahrenheit": return (value - Decimal("32")) * Decimal(5) / Decimal(9)
    return value - Decimal("273.15")


def from_celsius(value: Decimal, unit: str) -> Decimal:
    if unit == "celsius": return value
    if unit == "fahrenheit": return value * Decimal(9) / Decimal(5) + Decimal("32")
    return value + Decimal("273.15")


def convert_temperature(value: Decimal, from_unit: str, to_unit: str) -> Decimal:
    if value < ABSOLUTE_ZERO[from_unit]:
        raise ValueError("absolute_zero")
    return from_celsius(to_celsius(value, from_unit), to_unit)
