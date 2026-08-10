from decimal import Decimal

import pytest

from core.exercise_solver import solve_conversion_exercise


@pytest.mark.parametrize(
    ("exercise", "category", "expected"),
    [
        ("0,0004 dm2 = X mm2", "area", Decimal("4")),
        ("7 dm = X cm", "length", Decimal("70")),
        ("2 h = X min", "time", Decimal("120")),
        ("150 s = X min", "time", Decimal("2.5")),
        ("4 dg = X g", "mass", Decimal("0.4")),
        ("0,02 m2 = X dm2", "area", Decimal("2")),
        ("1,5 m3 = X dm3", "volume", Decimal("1500")),
        ("3 L = X mL", "capacity", Decimal("3000")),
        ("36 km/h = X m/s", "speed", Decimal("10")),
    ],
)
def test_solve_conversion_exercise(
    exercise: str,
    category: str,
    expected: Decimal,
) -> None:
    solution = solve_conversion_exercise(exercise)

    assert solution.category == category
    assert solution.result_value == expected


def test_area_exercise_formats_result() -> None:
    solution = solve_conversion_exercise(
        "0,0004 dm2 = X mm2"
    )

    assert solution.formatted_value == "4"
    assert solution.source_unit == "dm²"
    assert solution.target_unit == "mm²"


def test_incompatible_units_are_rejected() -> None:
    with pytest.raises(ValueError, match="incompatible_units"):
        solve_conversion_exercise("3 kg = X cm")


def test_invalid_exercise_is_rejected() -> None:
    with pytest.raises(ValueError, match="invalid_exercise"):
        solve_conversion_exercise("hola mundo")
