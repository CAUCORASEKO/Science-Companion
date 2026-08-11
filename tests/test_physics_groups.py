from app.physics_view import FORMULA_GROUPS


def test_physics_formula_groups_cover_expected_calculations() -> None:
    assert {"motion", "acceleration", "force", "work", "mechanical_power"} <= set(FORMULA_GROUPS["mechanics"])
    assert {"thermal_energy", "efficiency_energy", "efficiency_power", "density", "pressure"} == set(FORMULA_GROUPS["matter_energy"])
    assert set(FORMULA_GROUPS["electricity"]) == {"ohm", "electric_power"}
    assert set(FORMULA_GROUPS["waves"]) == {"wave_speed", "frequency_period", "sound_distance", "echo_distance"}


def test_physics_formula_groups_have_no_duplicate_keys() -> None:
    groups = [key for formulas in FORMULA_GROUPS.values() for key in formulas]
    assert len(groups) == len(set(groups))
