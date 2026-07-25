from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class CalculationResult:
    value: Decimal
    formatted_value: str
    formula: str
    steps: list[str]


@dataclass(frozen=True)
class Explanation:
    relationship: str
    calculation: str
    note: str
