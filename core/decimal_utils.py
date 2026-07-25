from decimal import Decimal, InvalidOperation


def parse_decimal(value: str) -> Decimal:
    normalized = value.strip().replace(" ", "").replace(",", ".")

    if not normalized:
        raise ValueError("empty_value")

    try:
        return Decimal(normalized)
    except InvalidOperation as exc:
        raise ValueError("invalid_number") from exc


def format_decimal(
    value: Decimal,
    decimal_separator: str = ",",
) -> str:
    if value == 0:
        text = "0"
    else:
        text = format(value.normalize(), "f")

    if "." in text:
        text = text.rstrip("0").rstrip(".")

    if decimal_separator != ".":
        text = text.replace(".", decimal_separator)

    return text
