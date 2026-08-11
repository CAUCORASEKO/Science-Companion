import json
from pathlib import Path


def test_locales_have_matching_interface_keys() -> None:
    locale_dir = Path(__file__).parents[1] / "locales"
    es = json.loads((locale_dir / "es.json").read_text(encoding="utf-8"))
    fi = json.loads((locale_dir / "fi.json").read_text(encoding="utf-8"))
    assert set(es) == set(fi)
    required = {
        "km",
        "hm",
        "dam",
        "m",
        "dm",
        "cm",
        "mm",
        "um",
        "nm",
        "m²",
        "m³",
        "L",
        "kg",
        "g",
        "second",
        "celsius",
        "mps",
        "mJ",
        "J",
        "kJ",
        "MJ",
        "GJ",
    }
    assert required <= set(es["units"])
    assert set(es["categories"]) == {
        "length",
        "area",
        "volume",
        "capacity",
        "mass",
        "time",
        "temperature",
        "speed",
        "energy",
        "frequency",
    }


def test_quantity_translations_exist() -> None:
    import json
    from pathlib import Path

    from core.quantities import QUANTITIES

    for locale_name in ("es", "fi"):
        data = json.loads(
            Path(f"locales/{locale_name}.json").read_text(encoding="utf-8")
        )

        for quantity in QUANTITIES:
            assert quantity.key in data["quantities"]
            assert quantity.key in data["si_units"]


def test_exercise_solver_translations_exist() -> None:
    import json
    from pathlib import Path

    required = {
        "exercise_solver",
        "exercise_placeholder",
        "solve",
        "exercise_examples",
        "invalid_exercise",
        "unknown_unit",
        "incompatible_units",
    }

    for locale in ("es", "fi"):
        data = json.loads(
            Path(f"locales/{locale}.json").read_text(
                encoding="utf-8"
            )
        )

        assert required <= data.keys()


def test_formula_translations_exist() -> None:
    import json
    from pathlib import Path

    from core.formulas import FORMULAS

    for locale in ("es", "fi"):
        data = json.loads(
            Path(f"locales/{locale}.json").read_text(
                encoding="utf-8"
            )
        )

        for formula in FORMULAS:
            assert formula.key in data["formula_names"]

            for _, variable_key, _ in formula.variables:
                assert (
                    variable_key
                    in data["formula_variables"]
                )


def test_physics_calculator_translations_exist() -> None:
    import json
    from pathlib import Path

    required = {
        "physics_title",
        "physics_intro",
        "physics_formula",
        "physics_expression",
        "physics_solve_for",
        "physics_process",
        "physics_enter_value",
        "physics_formula_names",
        "physics_variables",
    }

    for locale in ("es", "fi"):
        data = json.loads(
            Path(f"locales/{locale}.json").read_text(
                encoding="utf-8"
            )
        )

        assert required <= data.keys()
        assert {"mechanics", "matter_energy", "electricity", "waves"} <= data["physics_formula_groups"].keys()
