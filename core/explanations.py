from decimal import Decimal

from core.decimal_utils import format_decimal


def build_length_explanation(
    value: Decimal,
    from_unit: str,
    to_unit: str,
    factor: Decimal,
    language: str,
) -> tuple[str, str, str]:
    """Build localized learning content from conversion data."""
    decimal_separator = ","
    value_text = format_decimal(value, decimal_separator)
    factor_text = format_decimal(factor, decimal_separator)
    result_text = format_decimal(value * factor, decimal_separator)
    relationship = f"1 {from_unit} = {factor_text} {to_unit}"
    calculation = f"{value_text} {from_unit} × {factor_text} = {result_text} {to_unit}"

    direction = "up" if factor >= 1 else "down"
    notes = {
        "es": {
            "up": "En la escala métrica avanzamos hacia una unidad más pequeña, por eso multiplicamos por {factor}.",
            "down": "En la escala métrica avanzamos hacia una unidad más grande, por eso dividimos entre {divisor}.",
        },
        "fi": {
            "up": "Metrijärjestelmässä siirrytään pienempään yksikköön, joten kerrotaan luvulla {factor}.",
            "down": "Metrijärjestelmässä siirrytään suurempaan yksikköön, joten jaetaan luvulla {divisor}.",
        },
    }
    divisor = format_decimal(Decimal(1) / factor, decimal_separator) if factor else factor_text
    note = notes.get(language, notes["es"])[direction].format(
        factor=factor_text, divisor=divisor
    )
    return relationship, calculation, note
