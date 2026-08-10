from decimal import Decimal

from app.physics_units import to_si
from core.physics_calculator import solve_physics


def test_speed_unit_is_converted_before_physics_calculation() -> None:
    speed = to_si(Decimal("72"), "v", "kmh")
    result = solve_physics(
        "motion",
        "s",
        {"v": speed, "t": Decimal("1")},
    )
    assert result.value == Decimal("20")


def test_grams_are_converted_to_kilograms() -> None:
    assert to_si(Decimal("500"), "m", "g") == Decimal("0.5")


def test_minutes_are_converted_to_seconds() -> None:
    assert to_si(Decimal("3"), "t", "minute") == Decimal("180")


def test_kilojoules_are_converted_to_joules() -> None:
    assert to_si(Decimal("2"), "W", "kJ") == Decimal("2000")
