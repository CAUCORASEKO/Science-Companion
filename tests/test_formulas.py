from core.formulas import FORMULAS


def formula(key: str):
    return next(item for item in FORMULAS if item.key == key)


def test_formula_keys_are_unique() -> None:
    keys = [item.key for item in FORMULAS]
    assert len(keys) == len(set(keys))


def test_distance_formula() -> None:
    assert formula("distance").expression == "s = v · t"


def test_newtons_second_law() -> None:
    assert formula("newton_second_law").expression == "F = m · a"


def test_acceleration_from_force() -> None:
    assert formula("acceleration_from_force").expression == "a = F / m"


def test_mechanical_power() -> None:
    assert formula("power").expression == "P = W / t"


def test_electric_power() -> None:
    assert formula("electric_power").expression == "P = U · I"


def test_ohms_law() -> None:
    assert formula("ohms_law").expression == "U = R · I"
