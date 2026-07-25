from decimal import Decimal

import pytest

from core.conversion_engine import convert


@pytest.mark.parametrize("category, value, source, target, expected", [
    ("area", "0.08", "m²", "dm²", "8"), ("area", "0.0006", "m²", "cm²", "6"),
    ("area", "70000", "mm²", "dm²", "7"), ("area", "0.07", "cm²", "mm²", "7"), ("area", "6000000", "mm²", "m²", "6"),
    ("volume", "1", "m³", "dm³", "1000"), ("volume", "1", "dm³", "cm³", "1000"), ("volume", "1", "cm³", "mm³", "1000"),
    ("capacity", "1", "L", "mL", "1000"), ("capacity", "2.5", "hL", "L", "250"),
    ("mass", "1", "kg", "hg", "10"), ("mass", "1", "hg", "g", "100"), ("mass", "1", "g", "mg", "1000"), ("mass", "0.002", "kg", "g", "2"),
    ("time", "2", "hour", "minute", "120"), ("time", "1", "day", "second", "86400"), ("time", "1500", "millisecond", "second", "1.5"),
    ("temperature", "0", "celsius", "fahrenheit", "32"), ("temperature", "100", "celsius", "fahrenheit", "212"), ("temperature", "0", "celsius", "kelvin", "273.15"), ("temperature", "32", "fahrenheit", "celsius", "0"),
    ("speed", "1", "mps", "kmh", "3.6"), ("speed", "36", "kmh", "mps", "10"), ("speed", "1", "mph", "mps", "0.44704"), ("speed", "1", "knot", "mps", "0.514444"),
])
def test_conversion_categories(category, value, source, target, expected):
    assert convert(Decimal(value), category, source, target).value == Decimal(expected)


def test_temperature_rejects_absolute_zero_violation():
    with pytest.raises(ValueError, match="absolute_zero"):
        convert(Decimal("-274"), "temperature", "celsius", "kelvin")
