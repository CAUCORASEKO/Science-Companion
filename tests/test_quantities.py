from core.quantities import QUANTITIES


def test_quantities_have_unique_keys() -> None:
    keys = [quantity.key for quantity in QUANTITIES]
    assert len(keys) == len(set(keys))


def test_basic_quantities_count() -> None:
    basic = [q for q in QUANTITIES if q.category == "basic"]
    assert len(basic) == 7


def test_derived_quantities_include_force() -> None:
    force = next(q for q in QUANTITIES if q.key == "force")

    assert force.symbol == "F"
    assert force.unit_symbol == "N"
    assert force.si_equivalence == "1 N = 1 kg·m/s²"


def test_power_equivalence() -> None:
    power = next(q for q in QUANTITIES if q.key == "power")

    assert power.unit_symbol == "W"
    assert power.si_equivalence == "1 W = 1 J/s"
