from decimal import Decimal

from core.conversion_engine import convert


# Only unit names and categories live here. Conversion factors remain in the
# shared conversion registry used by the conversion page.
INPUT_UNITS: dict[str, tuple[str, ...]] = {
    "speed": ("mps", "kms", "kmh"),
    "distance": ("m", "km", "cm", "mm"),
    "time": ("second", "minute", "hour"),
    "mass": ("kg", "g"),
    "area": ("m²", "cm²"),
    "volume": ("m³", "dm³", "L"),
    "energy": ("J", "kJ", "MJ"),
    "frequency": ("Hz", "kHz", "MHz"),
    "wavelength": ("m", "cm", "mm"),
}

_VARIABLE_DIMENSIONS = {
    "v": "speed",
    "v0": "speed",
    "dv": "speed",
    "s": "distance",
    "t": "time",
    "dt": "time",
    "T": "time",
    "f": "frequency",
    "lambda": "wavelength",
    "m": "mass",
    "A": "area",
    "V": "volume",
    "W": "energy",
    "Ek": "energy",
    "Ep": "energy",
    "Q": "energy",
    "Eout": "energy",
    "Ein": "energy",
    "d": "distance",
}


def dimension_for(variable: str) -> str | None:
    return _VARIABLE_DIMENSIONS.get(variable)


def units_for(variable: str) -> tuple[str, ...]:
    return INPUT_UNITS.get(dimension_for(variable) or "", ())


def to_si(value: Decimal, variable: str, unit: str) -> Decimal:
    dimension = dimension_for(variable)
    if not dimension or unit not in INPUT_UNITS[dimension]:
        return value

    if dimension == "speed":
        return convert(value, "speed", unit, "mps").value
    if dimension == "distance":
        return convert(value, "length", unit, "m").value
    if dimension == "time":
        return convert(value, "time", unit, "second").value
    if dimension == "mass":
        return convert(value, "mass", unit, "kg").value
    if dimension == "area":
        return convert(value, "area", unit, "m²").value
    if dimension == "energy":
        return convert(value, "energy", unit, "J").value
    if dimension == "frequency":
        return convert(value, "frequency", unit, "Hz").value
    if dimension == "wavelength":
        return convert(value, "length", unit, "m").value
    if unit == "L":
        litres = convert(value, "capacity", "L", "L").value
        return convert(litres, "volume", "dm³", "m³").value
    return convert(value, "volume", unit, "m³").value
