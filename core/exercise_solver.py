import re
from dataclasses import dataclass
from decimal import Decimal

from core.conversion_engine import convert
from core.conversion_registry import CATEGORIES
from core.decimal_utils import parse_decimal


@dataclass(frozen=True)
class ExerciseSolution:
    category: str
    input_value: Decimal
    source_unit: str
    target_unit: str
    result_value: Decimal
    formatted_value: str
    formula: str
    calculation: str


UNIT_ALIASES = {
    # Length
    "km": "km",
    "hm": "hm",
    "dam": "dam",
    "m": "m",
    "dm": "dm",
    "cm": "cm",
    "mm": "mm",
    "µm": "um",
    "um": "um",
    "nm": "nm",

    # Area
    "km2": "km²",
    "km²": "km²",
    "hm2": "hm²",
    "hm²": "hm²",
    "dam2": "dam²",
    "dam²": "dam²",
    "m2": "m²",
    "m²": "m²",
    "dm2": "dm²",
    "dm²": "dm²",
    "cm2": "cm²",
    "cm²": "cm²",
    "mm2": "mm²",
    "mm²": "mm²",

    # Volume
    "km3": "km³",
    "km³": "km³",
    "hm3": "hm³",
    "hm³": "hm³",
    "dam3": "dam³",
    "dam³": "dam³",
    "m3": "m³",
    "m³": "m³",
    "dm3": "dm³",
    "dm³": "dm³",
    "cm3": "cm³",
    "cm³": "cm³",
    "mm3": "mm³",
    "mm³": "mm³",

    # Capacity
    "kl": "kL",
    "hl": "hL",
    "dal": "daL",
    "l": "L",
    "dl": "dL",
    "cl": "cL",
    "ml": "mL",

    # Mass
    "t": "t",
    "kg": "kg",
    "hg": "hg",
    "dag": "dag",
    "g": "g",
    "dg": "dg",
    "cg": "cg",
    "mg": "mg",
    "µg": "ug",
    "ug": "ug",

    # Time
    "d": "day",
    "day": "day",
    "h": "hour",
    "hour": "hour",
    "min": "minute",
    "minute": "minute",
    "s": "second",
    "sec": "second",
    "second": "second",
    "ms": "millisecond",
    "µs": "microsecond",
    "us": "microsecond",

    # Temperature
    "°c": "celsius",
    "c": "celsius",
    "°f": "fahrenheit",
    "f": "fahrenheit",
    "k": "kelvin",

    # Speed
    "m/s": "mps",
    "km/h": "kmh",
    "kmh": "kmh",
    "mph": "mph",
    "ft/s": "fts",
    "kn": "knot",
    "knot": "knot",
}


def normalize_unit(text: str) -> str:
    cleaned = text.strip().lower().replace(" ", "")

    if cleaned not in UNIT_ALIASES:
        raise ValueError("unknown_unit")

    return UNIT_ALIASES[cleaned]


def find_category(source_unit: str, target_unit: str) -> str:
    matches = []

    for category, definition in CATEGORIES.items():
        units = set(definition.unit_codes)

        if source_unit in units and target_unit in units:
            matches.append(category)

    if not matches:
        raise ValueError("incompatible_units")

    return matches[0]


def solve_conversion_exercise(text: str) -> ExerciseSolution:
    normalized = text.strip()

    pattern = re.compile(
        r"^\s*"
        r"(?P<value>[+-]?(?:\d+(?:[.,]\d*)?|[.,]\d+))"
        r"\s*"
        r"(?P<source>[^\s=]+)"
        r"\s*=\s*"
        r"[xX?]"
        r"\s*"
        r"(?P<target>[^\s=]+)"
        r"\s*$"
    )

    match = pattern.match(normalized)

    if not match:
        raise ValueError("invalid_exercise")

    value = parse_decimal(match.group("value"))
    source = normalize_unit(match.group("source"))
    target = normalize_unit(match.group("target"))

    category = find_category(source, target)

    result = convert(
        value,
        category,
        source,
        target,
    )

    return ExerciseSolution(
        category=category,
        input_value=value,
        source_unit=source,
        target_unit=target,
        result_value=result.value,
        formatted_value=result.formatted_value,
        formula=result.formula,
        calculation=result.steps[0],
    )
