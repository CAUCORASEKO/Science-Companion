from decimal import Decimal

from core.conversion_registry import CATEGORIES
from core.decimal_utils import format_decimal
from core.result import CalculationResult
from core.temperature import convert_temperature

LENGTH_FACTORS_IN_METERS = CATEGORIES["length"].factors


def convert(value: Decimal, category: str, from_unit: str, to_unit: str, decimal_separator: str = ",") -> CalculationResult:
    definition = CATEGORIES[category]
    if from_unit not in definition.unit_codes: raise ValueError(f"Unsupported source unit: {from_unit}")
    if to_unit not in definition.unit_codes: raise ValueError(f"Unsupported target unit: {to_unit}")
    if definition.kind == "temperature":
        result = convert_temperature(value, from_unit, to_unit)
        factor = None
    else:
        factor = definition.factors[from_unit] / definition.factors[to_unit]
        result = value * factor
    input_text = format_decimal(value, decimal_separator); result_text = format_decimal(result, decimal_separator)
    if factor is None:
        formula = f"{from_unit} → {to_unit}"
        step = f"{input_text} {from_unit} → {result_text} {to_unit}"
    else:
        factor_text = format_decimal(factor, decimal_separator)
        formula = f"1 {from_unit} = {factor_text} {to_unit}"
        step = f"{input_text} {from_unit} × {factor_text} = {result_text} {to_unit}"
    return CalculationResult(result, result_text, formula, [step])


def convert_length(value: Decimal, from_unit: str, to_unit: str, decimal_separator: str = ",") -> CalculationResult:
    return convert(value, "length", from_unit, to_unit, decimal_separator)
