from decimal import Decimal

from app.physics_units import to_si
from core.physics_calculator import solve_physics


def test_wave_speed():
    assert solve_physics("wave_speed", "v", {"f": Decimal("5"), "lambda": Decimal("2")}).value == Decimal("10")


def test_wave_frequency_and_period():
    assert solve_physics("wave_speed", "f", {"v": Decimal("340"), "lambda": Decimal("2")}).value == Decimal("170")
    assert solve_physics("frequency_period", "T", {"f": Decimal("50")}).value == Decimal("0.02")


def test_echo_sonar_and_lightning_distance():
    assert solve_physics("echo_distance", "d", {"v": Decimal("340"), "t": Decimal("3")}).value == Decimal("510")
    assert solve_physics("echo_distance", "d", {"v": Decimal("1500"), "t": Decimal("0.30")}).value == Decimal("225")
    assert solve_physics("sound_distance", "s", {"v": Decimal("340"), "t": Decimal("19")}).value == Decimal("6460")


def test_wave_unit_conversions():
    assert to_si(Decimal("1"), "f", "kHz") == Decimal("1000")
    assert to_si(Decimal("50"), "lambda", "cm") == Decimal("0.50")
