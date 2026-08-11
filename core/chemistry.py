from dataclasses import dataclass


@dataclass(frozen=True)
class Element:
    symbol: str
    atomic_number: int
    name_es: str
    name_fi: str
    period: int
    group: int
    classification: str
    family: str | None = None
    valence_electrons: int | None = None
    common_ion: str | None = None


ELEMENTS = (
    Element("H", 1, "Hidrógeno", "Vety", 1, 1, "nonmetal", None, 1, "+1 / −1"),
    Element("He", 2, "Helio", "Helium", 1, 18, "nonmetal", "noble_gas", 2),
    Element("Li", 3, "Litio", "Litium", 2, 1, "metal", "alkali_metal", 1, "+1"),
    Element("Be", 4, "Berilio", "Beryllium", 2, 2, "metal", "alkaline_earth", 2, "+2"),
    Element("C", 6, "Carbono", "Hiili", 2, 14, "nonmetal", None, 4),
    Element("N", 7, "Nitrógeno", "Typpi", 2, 15, "nonmetal", None, 5, "−3"),
    Element("O", 8, "Oxígeno", "Happi", 2, 16, "nonmetal", None, 6, "−2"),
    Element("F", 9, "Flúor", "Fluori", 2, 17, "nonmetal", "halogen", 7, "−1"),
    Element("Na", 11, "Sodio", "Natrium", 3, 1, "metal", "alkali_metal", 1, "+1"),
    Element("Mg", 12, "Magnesio", "Magnesium", 3, 2, "metal", "alkaline_earth", 2, "+2"),
    Element("Al", 13, "Aluminio", "Alumiini", 3, 13, "metal", None, 3, "+3"),
    Element("Si", 14, "Silicio", "Pii", 3, 14, "metalloid", None, 4),
    Element("P", 15, "Fósforo", "Fosfori", 3, 15, "nonmetal", None, 5, "−3 / +3 / +5"),
    Element("S", 16, "Azufre", "Rikki", 3, 16, "nonmetal", None, 6, "−2"),
    Element("Cl", 17, "Cloro", "Kloori", 3, 17, "nonmetal", "halogen", 7, "−1"),
    Element("K", 19, "Potasio", "Kalium", 4, 1, "metal", "alkali_metal", 1, "+1"),
    Element("Ca", 20, "Calcio", "Kalsium", 4, 2, "metal", "alkaline_earth", 2, "+2"),
    Element("Fe", 26, "Hierro", "Rauta", 4, 8, "metal", None, None, "+2 / +3"),
    Element("Co", 27, "Cobalto", "Koboltti", 4, 9, "metal", None, None, "+2 / +3"),
    Element("Ni", 28, "Níquel", "Nikkeli", 4, 10, "metal", None, None, "+2"),
    Element("Cu", 29, "Cobre", "Kupari", 4, 11, "metal", None, None, "+1 / +2"),
    Element("Zn", 30, "Zinc", "Sinkki", 4, 12, "metal", None, None, "+2"),
    Element("Ge", 32, "Germanio", "Germanium", 4, 14, "metalloid", None, 4),
    Element("Sn", 50, "Estaño", "Tina", 5, 14, "metal", None, 4, "+2 / +4"),
    Element("Au", 79, "Oro", "Kulta", 6, 11, "metal", None, None, "+1 / +3"),
    Element("U", 92, "Uranio", "Uraani", 7, 0, "metal"),
)

# Keep lookup independent of the UI and ready for the full periodic table.
ELEMENTS_BY_SYMBOL = {element.symbol.lower(): element for element in ELEMENTS}


def find_element(query: str) -> Element | None:
    normalized = query.strip().casefold()
    if not normalized:
        return None
    for element in ELEMENTS:
        if normalized in {element.symbol.casefold(), element.name_es.casefold(), element.name_fi.casefold()}:
            return element
    return None
