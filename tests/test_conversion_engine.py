from decimal import Decimal

import pytest

from core.conversion_engine import convert_length
from core.decimal_utils import format_decimal, parse_decimal


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("0,08", Decimal("0.08")),
        ("0.08", Decimal("0.08")),
        (" 70000 ", Decimal("70000")),
    ],
)
def test_parse_decimal(text: str, expected: Decimal) -> None:
    assert parse_decimal(text) == expected


def test_convert_meters_to_decimeters() -> None:
    result = convert_length(Decimal("0.08"), "m", "dm")

    assert result.value == Decimal("0.8")
    assert result.formatted_value == "0,8"


def test_convert_decimeters_to_centimeters() -> None:
    result = convert_length(Decimal("7"), "dm", "cm")

    assert result.value == Decimal("70")
    assert result.formatted_value == "70"


def test_convert_meters_to_millimeters() -> None:
    result = convert_length(Decimal("3.9"), "m", "mm")

    assert result.value == Decimal("3900")


def test_format_decimal_removes_unnecessary_zeroes() -> None:
    assert format_decimal(Decimal("70.000")) == "70"
    assert format_decimal(Decimal("0.800")) == "0,8"
