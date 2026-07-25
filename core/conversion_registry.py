from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class CategoryDefinition:
    code: str
    unit_codes: tuple[str, ...]
    factors: dict[str, Decimal]
    defaults: tuple[str, str]
    kind: str = "linear"


def _metric(prefixes: tuple[str, ...], exponent: int, base: str) -> dict[str, Decimal]:
    powers = {"k": 3, "h": 2, "da": 1, "": 0, "d": -1, "c": -2, "m": -3}
    return {f"{prefix}{base}": Decimal(10) ** (powers[prefix] * exponent) for prefix in prefixes}


CATEGORIES = {
    "length": CategoryDefinition("length", ("km", "hm", "dam", "m", "dm", "cm", "mm", "um", "nm"), {
        "km": Decimal("1000"), "hm": Decimal("100"), "dam": Decimal("10"), "m": Decimal("1"),
        "dm": Decimal("0.1"), "cm": Decimal("0.01"), "mm": Decimal("0.001"), "um": Decimal("0.000001"), "nm": Decimal("0.000000001")}, ("m", "cm")),
    "area": CategoryDefinition("area", tuple(_metric(("k", "h", "da", "", "d", "c", "m"), 2, "m²")), _metric(("k", "h", "da", "", "d", "c", "m"), 2, "m²"), ("m²", "cm²")),
    "volume": CategoryDefinition("volume", tuple(_metric(("k", "h", "da", "", "d", "c", "m"), 3, "m³")), _metric(("k", "h", "da", "", "d", "c", "m"), 3, "m³"), ("m³", "dm³")),
    "capacity": CategoryDefinition("capacity", tuple(_metric(("k", "h", "da", "", "d", "c", "m"), 1, "L")), _metric(("k", "h", "da", "", "d", "c", "m"), 1, "L"), ("L", "mL")),
    "mass": CategoryDefinition("mass", ("t", "kg", "hg", "dag", "g", "dg", "cg", "mg", "ug"), {
        "t": Decimal("1000000"), "kg": Decimal("1000"), "hg": Decimal("100"), "dag": Decimal("10"), "g": Decimal("1"), "dg": Decimal("0.1"), "cg": Decimal("0.01"), "mg": Decimal("0.001"), "ug": Decimal("0.000001")}, ("kg", "g")),
    "time": CategoryDefinition("time", ("day", "hour", "minute", "second", "millisecond", "microsecond"), {
        "day": Decimal("86400"), "hour": Decimal("3600"), "minute": Decimal("60"), "second": Decimal("1"), "millisecond": Decimal("0.001"), "microsecond": Decimal("0.000001")}, ("hour", "minute")),
    "temperature": CategoryDefinition("temperature", ("celsius", "fahrenheit", "kelvin"), {}, ("celsius", "fahrenheit"), "temperature"),
    "speed": CategoryDefinition("speed", ("mps", "kmh", "mph", "fts", "knot"), {
        "mps": Decimal("1"), "kmh": Decimal("0.2777777777777777777777777778"), "mph": Decimal("0.44704"), "fts": Decimal("0.3048"), "knot": Decimal("0.514444")}, ("kmh", "mps")),
}


def category_codes() -> tuple[str, ...]:
    return tuple(CATEGORIES)
