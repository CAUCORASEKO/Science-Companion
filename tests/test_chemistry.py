from core.chemistry import find_element


def test_element_reference_data() -> None:
    mg = find_element("Mg")
    assert mg and (mg.atomic_number, mg.period, mg.group, mg.family, mg.common_ion) == (12, 3, 2, "alkaline_earth", "+2")
    cl = find_element("Cl")
    assert cl and (cl.atomic_number, cl.period, cl.group, cl.family, cl.common_ion) == (17, 3, 17, "halogen", "−1")
    he = find_element("He")
    assert he and (he.atomic_number, he.period, he.group, he.family) == (2, 1, 18, "noble_gas")
    assert find_element("Co").atomic_number == 27
    assert find_element("S").symbol == "S" and find_element("S").atomic_number == 16
    assert (find_element("Al").period, find_element("Al").group, find_element("Al").valence_electrons) == (3, 13, 3)
    assert (find_element("Ca").period, find_element("Ca").group) == (4, 2)
    assert find_element("Ge").classification == "metalloid"
    assert find_element("Na").family == "alkali_metal"
    assert find_element("Si").classification == "metalloid"


def test_element_lookup_uses_both_languages() -> None:
    assert find_element("Mg").symbol == "Mg"
    assert find_element("magnesio").symbol == "Mg"
    assert find_element("magnesium").symbol == "Mg"
