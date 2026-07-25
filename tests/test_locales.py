import json
from pathlib import Path


def test_locales_have_matching_interface_keys() -> None:
    locale_dir = Path(__file__).parents[1] / "locales"
    es = json.loads((locale_dir / "es.json").read_text(encoding="utf-8"))
    fi = json.loads((locale_dir / "fi.json").read_text(encoding="utf-8"))
    assert set(es) == set(fi)
    assert set(es["units"]) == {"km", "hm", "dam", "m", "dm", "cm", "mm", "um", "nm"}
