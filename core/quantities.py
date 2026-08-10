from dataclasses import dataclass


@dataclass(frozen=True)
class Quantity:
    key: str
    symbol: str
    unit_symbol: str
    si_equivalence: str
    category: str


QUANTITIES = (
    Quantity(
        key="length",
        symbol="l",
        unit_symbol="m",
        si_equivalence="",
        category="basic",
    ),
    Quantity(
        key="mass",
        symbol="m",
        unit_symbol="kg",
        si_equivalence="",
        category="basic",
    ),
    Quantity(
        key="time",
        symbol="t",
        unit_symbol="s",
        si_equivalence="",
        category="basic",
    ),
    Quantity(
        key="temperature",
        symbol="T",
        unit_symbol="K",
        si_equivalence="",
        category="basic",
    ),
    Quantity(
        key="electric_current",
        symbol="I",
        unit_symbol="A",
        si_equivalence="",
        category="basic",
    ),
    Quantity(
        key="amount_of_substance",
        symbol="n",
        unit_symbol="mol",
        si_equivalence="",
        category="basic",
    ),
    Quantity(
        key="luminous_intensity",
        symbol="Iᵥ",
        unit_symbol="cd",
        si_equivalence="",
        category="basic",
    ),

    Quantity(
        key="area",
        symbol="A",
        unit_symbol="m²",
        si_equivalence="m × m",
        category="derived",
    ),
    Quantity(
        key="volume",
        symbol="V",
        unit_symbol="m³",
        si_equivalence="m × m × m",
        category="derived",
    ),
    Quantity(
        key="speed",
        symbol="v",
        unit_symbol="m/s",
        si_equivalence="m/s",
        category="derived",
    ),
    Quantity(
        key="acceleration",
        symbol="a",
        unit_symbol="m/s²",
        si_equivalence="m/s²",
        category="derived",
    ),
    Quantity(
        key="force",
        symbol="F",
        unit_symbol="N",
        si_equivalence="1 N = 1 kg·m/s²",
        category="derived",
    ),
    Quantity(
        key="pressure",
        symbol="p",
        unit_symbol="Pa",
        si_equivalence="1 Pa = 1 N/m²",
        category="derived",
    ),
    Quantity(
        key="work",
        symbol="W",
        unit_symbol="J",
        si_equivalence="1 J = 1 N·m",
        category="derived",
    ),
    Quantity(
        key="energy",
        symbol="E",
        unit_symbol="J",
        si_equivalence="1 J = 1 N·m",
        category="derived",
    ),
    Quantity(
        key="power",
        symbol="P",
        unit_symbol="W",
        si_equivalence="1 W = 1 J/s",
        category="derived",
    ),
    Quantity(
        key="density",
        symbol="ρ",
        unit_symbol="kg/m³",
        si_equivalence="kg/m³",
        category="derived",
    ),
    Quantity(
        key="frequency",
        symbol="f",
        unit_symbol="Hz",
        si_equivalence="1 Hz = 1/s",
        category="derived",
    ),
    Quantity(
        key="electric_charge",
        symbol="Q",
        unit_symbol="C",
        si_equivalence="1 C = 1 A·s",
        category="derived",
    ),
    Quantity(
        key="voltage",
        symbol="U",
        unit_symbol="V",
        si_equivalence="1 V = 1 J/C",
        category="derived",
    ),
    Quantity(
        key="resistance",
        symbol="R",
        unit_symbol="Ω",
        si_equivalence="1 Ω = 1 V/A",
        category="derived",
    ),
)
