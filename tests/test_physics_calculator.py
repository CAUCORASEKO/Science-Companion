from decimal import Decimal

import pytest

from core.physics_calculator import solve_physics


def test_speed() -> None:
    result = solve_physics(
        "motion",
        "v",
        {
            "s": Decimal("120"),
            "t": Decimal("8"),
        },
    )

    assert result.value == Decimal("15")
    assert result.unit == "m/s"


def test_distance() -> None:
    result = solve_physics(
        "motion",
        "s",
        {
            "v": Decimal("15"),
            "t": Decimal("8"),
        },
    )

    assert result.value == Decimal("120")
    assert result.unit == "m"


def test_time_from_motion() -> None:
    result = solve_physics(
        "motion",
        "t",
        {
            "s": Decimal("120"),
            "v": Decimal("15"),
        },
    )

    assert result.value == Decimal("8")


def test_acceleration() -> None:
    result = solve_physics(
        "acceleration",
        "a",
        {
            "dv": Decimal("20"),
            "dt": Decimal("4"),
        },
    )

    assert result.value == Decimal("5")
    assert result.unit == "m/s²"


def test_force() -> None:
    result = solve_physics(
        "force",
        "F",
        {
            "m": Decimal("5"),
            "a": Decimal("2"),
        },
    )

    assert result.value == Decimal("10")
    assert result.unit == "N"


def test_acceleration_from_force() -> None:
    result = solve_physics(
        "force",
        "a",
        {
            "F": Decimal("10"),
            "m": Decimal("5"),
        },
    )

    assert result.value == Decimal("2")


def test_mass_from_force() -> None:
    result = solve_physics(
        "force",
        "m",
        {
            "F": Decimal("10"),
            "a": Decimal("2"),
        },
    )

    assert result.value == Decimal("5")


def test_work() -> None:
    result = solve_physics(
        "work",
        "W",
        {
            "F": Decimal("20"),
            "s": Decimal("3"),
        },
    )

    assert result.value == Decimal("60")
    assert result.unit == "J"


def test_mechanical_power() -> None:
    result = solve_physics(
        "mechanical_power",
        "P",
        {
            "W": Decimal("600"),
            "t": Decimal("30"),
        },
    )

    assert result.value == Decimal("20")
    assert result.unit == "W"


def test_density() -> None:
    result = solve_physics(
        "density",
        "rho",
        {
            "m": Decimal("12"),
            "V": Decimal("3"),
        },
    )

    assert result.value == Decimal("4")
    assert result.unit == "kg/m³"


def test_volume_from_density() -> None:
    result = solve_physics(
        "density",
        "V",
        {
            "m": Decimal("12"),
            "rho": Decimal("4"),
        },
    )

    assert result.value == Decimal("3")


def test_pressure() -> None:
    result = solve_physics(
        "pressure",
        "p",
        {
            "F": Decimal("100"),
            "A": Decimal("2"),
        },
    )

    assert result.value == Decimal("50")
    assert result.unit == "Pa"


def test_electric_power() -> None:
    result = solve_physics(
        "electric_power",
        "P",
        {
            "U": Decimal("230"),
            "I": Decimal("2"),
        },
    )

    assert result.value == Decimal("460")
    assert result.unit == "W"


def test_electric_power_from_voltage_and_resistance() -> None:
    result = solve_physics("electric_power", "P", {"U": Decimal("24"), "R": Decimal("8")})
    assert result.value == Decimal("72")


def test_electric_power_second_example() -> None:
    result = solve_physics("electric_power", "P", {"U": Decimal("25"), "R": Decimal("5")})
    assert result.value == Decimal("125")


def test_ohm_examples() -> None:
    assert solve_physics("ohm", "I", {"U": Decimal("24"), "R": Decimal("8")}).value == Decimal("3")
    assert solve_physics("ohm", "I", {"U": Decimal("25"), "R": Decimal("5")}).value == Decimal("5")


def test_voltage_from_ohms_law() -> None:
    result = solve_physics(
        "ohm",
        "U",
        {
            "R": Decimal("10"),
            "I": Decimal("2"),
        },
    )

    assert result.value == Decimal("20")
    assert result.unit == "V"


def test_current_from_ohms_law() -> None:
    result = solve_physics(
        "ohm",
        "I",
        {
            "U": Decimal("20"),
            "R": Decimal("10"),
        },
    )

    assert result.value == Decimal("2")
    assert result.unit == "A"


def test_resistance_from_ohms_law() -> None:
    result = solve_physics(
        "ohm",
        "R",
        {
            "U": Decimal("20"),
            "I": Decimal("2"),
        },
    )

    assert result.value == Decimal("10")
    assert result.unit == "Ω"


def test_zero_division_is_rejected() -> None:
    with pytest.raises(ValueError):
        solve_physics(
            "motion",
            "v",
            {
                "s": Decimal("10"),
                "t": Decimal("0"),
            },
        )


def test_decimal_comma_output() -> None:
    result = solve_physics(
        "motion",
        "v",
        {
            "s": Decimal("1"),
            "t": Decimal("4"),
        },
    )

    assert result.formatted_value == "0,25"


def test_kinetic_energy() -> None:
    result = solve_physics(
        "kinetic_energy",
        "Ek",
        {"m": Decimal("10"), "v": Decimal("4")},
    )
    assert result.value == Decimal("80")
    assert result.unit == "J"


def test_speed_from_kinetic_energy() -> None:
    result = solve_physics(
        "kinetic_energy",
        "v",
        {"Ek": Decimal("80"), "m": Decimal("10")},
    )
    assert result.value == Decimal("4")


def test_potential_energy() -> None:
    result = solve_physics(
        "potential_energy",
        "Ep",
        {
            "m": Decimal("10"),
            "g": Decimal("9.81"),
            "h": Decimal("5"),
        },
    )
    assert result.value == Decimal("490.50")


def test_thermal_energy() -> None:
    result = solve_physics(
        "thermal_energy",
        "Q",
        {
            "m": Decimal("2"),
            "c": Decimal("4200"),
            "dT": Decimal("5"),
        },
    )
    assert result.value == Decimal("42000")


def test_energy_efficiency_from_course_example() -> None:
    result = solve_physics(
        "efficiency_energy",
        "eta",
        {
            "Eout": Decimal("55"),
            "Ein": Decimal("503"),
        },
    )
    assert result.value.quantize(Decimal("0.01")) == Decimal("10.93")


def test_power_efficiency_from_course_example() -> None:
    result = solve_physics(
        "efficiency_power",
        "eta",
        {
            "Pout": Decimal("7"),
            "Pin": Decimal("109"),
        },
    )
    assert result.value.quantize(Decimal("0.01")) == Decimal("6.42")
