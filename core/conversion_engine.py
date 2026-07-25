from decimal import Decimal

from core.decimal_utils import format_decimal
from core.result import CalculationResult


LENGTH_FACTORS_IN_METERS = {
    "km": Decimal("1000"),
    "hm": Decimal("100"),
    "dam": Decimal("10"),
    "m": Decimal("1"),
    "dm": Decimal("0.1"),
    "cm": Decimal("0.01"),
    "mm": Decimal("0.001"),
    "um": Decimal("0.000001"),
    "nm": Decimal("0.000000001"),
}


def convert_length(
    value: Decimal,
    from_unit: str,
    to_unit: str,
    decimal_separator: str = ",",
) -> CalculationResult:
    if from_unit not in LENGTH_FACTORS_IN_METERS:
        raise ValueError(f"Unsupported source unit: {from_unit}")

    if to_unit not in LENGTH_FACTORS_IN_METERS:
        raise ValueError(f"Unsupported target unit: {to_unit}")

    source_factor = LENGTH_FACTORS_IN_METERS[from_unit]
    target_factor = LENGTH_FACTORS_IN_METERS[to_unit]

    value_in_meters = value * source_factor
    result = value_in_meters / target_factor
    direct_factor = source_factor / target_factor

    formatted_input = format_decimal(value, decimal_separator)
    formatted_factor = format_decimal(direct_factor, decimal_separator)
    formatted_result = format_decimal(result, decimal_separator)

    formula = f"1 {from_unit} = {formatted_factor} {to_unit}"

    steps = [
        (
            f"{formatted_input} {from_unit} × "
            f"{formatted_factor} = {formatted_result} {to_unit}"
        )
    ]

    return CalculationResult(
        value=result,
        formatted_value=formatted_result,
        formula=formula,
        steps=steps,
    )
