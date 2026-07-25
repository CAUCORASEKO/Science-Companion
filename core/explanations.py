from decimal import Decimal

from core.conversion_registry import CATEGORIES
from core.decimal_utils import format_decimal


def build_explanation(value: Decimal, category: str, from_unit: str, to_unit: str, result: Decimal, language: str) -> tuple[str, str, str]:
    definition = CATEGORIES[category]
    value_text = format_decimal(value); result_text = format_decimal(result)
    if definition.kind == "temperature":
        relationship = f"{from_unit} → {to_unit}"
        calculation = f"{value_text} {from_unit} → {result_text} {to_unit}"
        notes = {"es": "La temperatura se convierte mediante una fórmula, no con un único factor de escala.", "fi": "Lämpötila muunnetaan kaavalla, ei yhdellä ainoalla muuntokertoimella."}
        return relationship, calculation, notes.get(language, notes["es"])
    factor = definition.factors[from_unit] / definition.factors[to_unit]
    factor_text = format_decimal(factor)
    relationship = f"1 {from_unit} = {factor_text} {to_unit}"
    calculation = f"{value_text} {from_unit} × {factor_text} = {result_text} {to_unit}"
    direction = "multiply" if factor >= 1 else "divide"
    notes = {
        "es": {
            "length": {"multiply": "En la escala métrica avanzamos hacia una unidad más pequeña, por eso multiplicamos por {factor}.", "divide": "En la escala métrica avanzamos hacia una unidad más grande, por eso dividimos entre {factor}."},
            "area": "En una medida de superficie, cada paso de la escala métrica multiplica o divide por 100.",
            "volume": "En volumen, cada paso de la escala métrica multiplica o divide por 1000.",
            "capacity": "En la escala de capacidad, cada paso multiplica o divide por 10.",
            "mass": "En la escala de masa, cada paso multiplica o divide por 10.",
            "time": "La conversión usa la relación exacta entre las unidades de tiempo.",
            "speed": "La conversión usa factores precisos respecto al metro por segundo.",
        },
        "fi": {
            "length": {"multiply": "Metrijärjestelmässä siirrytään pienempään yksikköön, joten kerrotaan luvulla {factor}.", "divide": "Metrijärjestelmässä siirrytään suurempaan yksikköön, joten jaetaan luvulla {factor}."},
            "area": "Pinta-alassa jokainen metrijärjestelmän askel kertoo tai jakaa luvulla 100.",
            "volume": "Tilavuudessa jokainen metrijärjestelmän askel kertoo tai jakaa luvulla 1000.",
            "capacity": "Vetoisuusmitoissa jokainen askel kertoo tai jakaa luvulla 10.",
            "mass": "Massayksiköissä jokainen askel kertoo tai jakaa luvulla 10.",
            "time": "Muunnos käyttää aikayksiköiden tarkkaa suhdetta.",
            "speed": "Muunnos käyttää tarkkoja kertoimia suhteessa metriin sekunnissa.",
        },
    }
    note_template = notes.get(language, notes["es"])[category]
    if isinstance(note_template, dict): note_template = note_template[direction]
    return relationship, calculation, note_template.format(factor=factor_text)


def build_length_explanation(value: Decimal, from_unit: str, to_unit: str, factor: Decimal, language: str) -> tuple[str, str, str]:
    result = value * factor
    return build_explanation(value, "length", from_unit, to_unit, result, language)
