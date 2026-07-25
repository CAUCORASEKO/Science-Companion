from decimal import Decimal

from core.explanations import build_length_explanation


def test_spanish_explanation_is_generated_from_conversion_data() -> None:
    relationship, calculation, note = build_length_explanation(Decimal("0.08"), "m", "dm", Decimal("10"), "es")
    assert relationship == "1 m = 10 dm"
    assert calculation == "0,08 m × 10 = 0,8 dm"
    assert "multiplicamos por 10" in note


def test_finnish_explanation_is_localized() -> None:
    _, _, note = build_length_explanation(Decimal("0.08"), "m", "dm", Decimal("10"), "fi")
    assert "Metrijärjestelmässä" in note
    assert "kerrotaan luvulla 10" in note
