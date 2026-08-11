from dataclasses import dataclass
from decimal import Decimal, DivisionByZero, InvalidOperation

from core.decimal_utils import format_decimal


@dataclass(frozen=True)
class PhysicsResult:
    formula_key: str
    solve_for: str
    value: Decimal
    formatted_value: str
    unit: str
    formula: str
    substituted: str
    calculation: str


RESULT_UNITS = {
    # Motion
    ("motion", "v"): "m/s",
    ("motion", "s"): "m",
    ("motion", "t"): "s",

    # Acceleration
    ("acceleration", "a"): "m/s²",
    ("acceleration", "dv"): "m/s",
    ("acceleration", "dt"): "s",

    # Constant acceleration velocity
    ("constant_acceleration", "v"): "m/s",
    ("constant_acceleration", "v0"): "m/s",
    ("constant_acceleration", "a"): "m/s²",
    ("constant_acceleration", "t"): "s",

    # Free fall
    ("free_fall", "v"): "m/s",
    ("free_fall", "v0"): "m/s",
    ("free_fall", "g"): "m/s²",
    ("free_fall", "t"): "s",

    # Newton
    ("force", "F"): "N",
    ("force", "m"): "kg",
    ("force", "a"): "m/s²",

    # Weight / gravitational force
    ("weight", "Fg"): "N",
    ("weight", "m"): "kg",
    ("weight", "g"): "m/s²",

    # Work
    ("work", "W"): "J",
    ("work", "F"): "N",
    ("work", "s"): "m",

    # Mechanical power
    ("mechanical_power", "P"): "W",
    ("mechanical_power", "W"): "J",
    ("mechanical_power", "t"): "s",

    # Kinetic energy
    ("kinetic_energy", "Ek"): "J",
    ("kinetic_energy", "m"): "kg",
    ("kinetic_energy", "v"): "m/s",

    # Gravitational potential energy
    ("potential_energy", "Ep"): "J",
    ("potential_energy", "m"): "kg",
    ("potential_energy", "g"): "m/s²",
    ("potential_energy", "h"): "m",

    # Thermal energy
    ("thermal_energy", "Q"): "J",
    ("thermal_energy", "m"): "kg",
    ("thermal_energy", "c"): "J/(kg·K)",
    ("thermal_energy", "dT"): "K",

    # Efficiency from energy
    ("efficiency_energy", "eta"): "%",
    ("efficiency_energy", "Eout"): "J",
    ("efficiency_energy", "Ein"): "J",

    # Efficiency from power
    ("efficiency_power", "eta"): "%",
    ("efficiency_power", "Pout"): "W",
    ("efficiency_power", "Pin"): "W",

    # Density
    ("density", "rho"): "kg/m³",
    ("density", "m"): "kg",
    ("density", "V"): "m³",

    # Pressure
    ("pressure", "p"): "Pa",
    ("pressure", "F"): "N",
    ("pressure", "A"): "m²",

    # Electric power
    ("electric_power", "P"): "W",
    ("electric_power", "U"): "V",
    ("electric_power", "I"): "A",
    ("electric_power", "R"): "Ω",

    # Ohm
    ("ohm", "U"): "V",
    ("ohm", "R"): "Ω",
    ("ohm", "I"): "A",
    ("wave_speed", "v"): "m/s",
    ("wave_speed", "f"): "Hz",
    ("wave_speed", "lambda"): "m",
    ("frequency_period", "f"): "Hz",
    ("frequency_period", "T"): "s",
    ("sound_distance", "s"): "m",
    ("sound_distance", "v"): "m/s",
    ("sound_distance", "t"): "s",
    ("echo_distance", "d"): "m",
    ("echo_distance", "v"): "m/s",
    ("echo_distance", "t"): "s",
}


FORMULA_LABELS = {
    "motion": "v = s / t",
    "acceleration": "a = Δv / Δt",
    "constant_acceleration": "v = v₀ + a · t",
    "free_fall": "v = v₀ + g · t",
    "force": "F = m · a",
    "weight": "F_g = m · g",
    "work": "W = F · s",
    "mechanical_power": "P = W / t",
    "kinetic_energy": "Eₖ = ½ · m · v²",
    "potential_energy": "Eₚ = m · g · h",
    "thermal_energy": "Q = m · c · ΔT",
    "efficiency_energy": "η = E_out / E_in · 100",
    "efficiency_power": "η = P_out / P_in · 100",
    "density": "ρ = m / V",
    "pressure": "p = F / A",
    "electric_power": "P = U · I  ·  P = U² / R  ·  P = I² · R",
    "ohm": "U = R · I",
    "wave_speed": "v = f · λ",
    "frequency_period": "f = 1 / T",
    "sound_distance": "s = v · t",
    "echo_distance": "d = v · t / 2",
}


VARIABLES = {
    "motion": ("v", "s", "t"),
    "acceleration": ("a", "dv", "dt"),
    "constant_acceleration": ("v", "v0", "a", "t"),
    "free_fall": ("v", "v0", "g", "t"),
    "force": ("F", "m", "a"),
    "weight": ("Fg", "m", "g"),
    "work": ("W", "F", "s"),
    "mechanical_power": ("P", "W", "t"),
    "kinetic_energy": ("Ek", "m", "v"),
    "potential_energy": ("Ep", "m", "g", "h"),
    "thermal_energy": ("Q", "m", "c", "dT"),
    "efficiency_energy": ("eta", "Eout", "Ein"),
    "efficiency_power": ("eta", "Pout", "Pin"),
    "density": ("rho", "m", "V"),
    "pressure": ("p", "F", "A"),
    "electric_power": ("P", "U", "I", "R"),
    "ohm": ("U", "R", "I"),
    "wave_speed": ("v", "f", "lambda"),
    "frequency_period": ("f", "T"),
    "sound_distance": ("s", "v", "t"),
    "echo_distance": ("d", "v", "t"),
}


DISPLAY_SYMBOLS = {
    "rho": "ρ",
    "dv": "Δv",
    "dt": "Δt",
    "v0": "v₀",
    "Fg": "F_g",
    "Ek": "Eₖ",
    "Ep": "Eₚ",
    "dT": "ΔT",
    "eta": "η",
    "Eout": "E_out",
    "Ein": "E_in",
    "Pout": "P_out",
    "Pin": "P_in",
    "lambda": "λ",
}


def display_symbol(variable: str) -> str:
    return DISPLAY_SYMBOLS.get(variable, variable)


def _require_nonzero(value: Decimal, variable: str) -> None:
    if value == 0:
        raise ValueError(f"zero_division:{variable}")


def _require_positive_or_zero(value: Decimal, variable: str) -> None:
    if value < 0:
        raise ValueError(f"negative_value:{variable}")


def solve_physics(
    formula_key: str,
    solve_for: str,
    values: dict[str, Decimal],
    decimal_separator: str = ",",
) -> PhysicsResult:
    if formula_key not in VARIABLES:
        raise ValueError("unknown_formula")

    variables = VARIABLES[formula_key]

    if solve_for not in variables:
        raise ValueError("unknown_variable")

    required = [v for v in variables if v != solve_for]

    # Electric power is one formula family with equivalent input pairs.
    if formula_key == "electric_power":
        required = []
        if solve_for == "P":
            if not (("U" in values and "I" in values) or ("U" in values and "R" in values) or ("I" in values and "R" in values)):
                raise ValueError("missing_value:electric_power_pair")
        elif not (("P" in values and "U" in values) or ("P" in values and "R" in values) or ("U" in values and "I" in values)):
            raise ValueError("missing_value:electric_power_pair")

    for variable in required:
        if variable not in values:
            raise ValueError(f"missing_value:{variable}")

    try:
        if formula_key == "motion":
            result = _solve_motion(solve_for, values)

        elif formula_key == "acceleration":
            result = _solve_acceleration(solve_for, values)

        elif formula_key == "constant_acceleration":
            result = _solve_constant_acceleration(solve_for, values)

        elif formula_key == "free_fall":
            result = _solve_free_fall(solve_for, values)

        elif formula_key == "force":
            result = _solve_force(solve_for, values)

        elif formula_key == "weight":
            result = _solve_weight(solve_for, values)

        elif formula_key == "work":
            result = _solve_work(solve_for, values)

        elif formula_key == "mechanical_power":
            result = _solve_mechanical_power(solve_for, values)

        elif formula_key == "kinetic_energy":
            result = _solve_kinetic_energy(solve_for, values)

        elif formula_key == "potential_energy":
            result = _solve_potential_energy(solve_for, values)

        elif formula_key == "thermal_energy":
            result = _solve_thermal_energy(solve_for, values)

        elif formula_key == "efficiency_energy":
            result = _solve_efficiency_energy(solve_for, values)

        elif formula_key == "efficiency_power":
            result = _solve_efficiency_power(solve_for, values)

        elif formula_key == "density":
            result = _solve_density(solve_for, values)

        elif formula_key == "pressure":
            result = _solve_pressure(solve_for, values)

        elif formula_key == "electric_power":
            result = _solve_electric_power(solve_for, values)

        elif formula_key == "ohm":
            result = _solve_ohm(solve_for, values)

        elif formula_key == "wave_speed":
            result = _solve_wave_speed(solve_for, values)
        elif formula_key == "frequency_period":
            result = _solve_frequency_period(solve_for, values)
        elif formula_key == "sound_distance":
            result = _solve_motion(solve_for, values)
        elif formula_key == "echo_distance":
            result = _solve_echo_distance(solve_for, values)

        else:
            raise ValueError("unknown_formula")

    except (DivisionByZero, InvalidOperation, ZeroDivisionError) as exc:
        raise ValueError("division_by_zero") from exc

    substituted = _build_substitution(
        formula_key,
        solve_for,
        values,
        decimal_separator,
    )

    formatted = format_decimal(
        result,
        decimal_separator,
    )

    symbol = display_symbol(solve_for)
    unit = RESULT_UNITS[(formula_key, solve_for)]

    return PhysicsResult(
        formula_key=formula_key,
        solve_for=solve_for,
        value=result,
        formatted_value=formatted,
        unit=unit,
        formula=FORMULA_LABELS[formula_key],
        substituted=substituted,
        calculation=f"{symbol} = {formatted} {unit}",
    )


def _solve_motion(
    solve_for: str,
    v: dict[str, Decimal],
) -> Decimal:
    if solve_for == "v":
        _require_nonzero(v["t"], "t")
        return v["s"] / v["t"]

    if solve_for == "s":
        return v["v"] * v["t"]

    _require_nonzero(v["v"], "v")
    return v["s"] / v["v"]


def _solve_acceleration(
    solve_for: str,
    v: dict[str, Decimal],
) -> Decimal:
    if solve_for == "a":
        _require_nonzero(v["dt"], "dt")
        return v["dv"] / v["dt"]

    if solve_for == "dv":
        return v["a"] * v["dt"]

    _require_nonzero(v["a"], "a")
    return v["dv"] / v["a"]


def _solve_constant_acceleration(
    solve_for: str,
    v: dict[str, Decimal],
) -> Decimal:
    if solve_for == "v":
        return v["v0"] + v["a"] * v["t"]
    if solve_for == "v0":
        return v["v"] - v["a"] * v["t"]
    if solve_for == "a":
        _require_nonzero(v["t"], "t")
        return (v["v"] - v["v0"]) / v["t"]
    _require_nonzero(v["a"], "a")
    return (v["v"] - v["v0"]) / v["a"]


def _solve_free_fall(
    solve_for: str,
    v: dict[str, Decimal],
) -> Decimal:
    if solve_for == "v":
        return v["v0"] + v["g"] * v["t"]
    if solve_for == "v0":
        return v["v"] - v["g"] * v["t"]
    if solve_for == "g":
        _require_nonzero(v["t"], "t")
        return (v["v"] - v["v0"]) / v["t"]
    _require_nonzero(v["g"], "g")
    return (v["v"] - v["v0"]) / v["g"]


def _solve_force(
    solve_for: str,
    v: dict[str, Decimal],
) -> Decimal:
    if solve_for == "F":
        return v["m"] * v["a"]

    if solve_for == "m":
        _require_nonzero(v["a"], "a")
        return v["F"] / v["a"]

    _require_nonzero(v["m"], "m")
    return v["F"] / v["m"]


def _solve_weight(
    solve_for: str,
    v: dict[str, Decimal],
) -> Decimal:
    if solve_for == "Fg":
        return v["m"] * v["g"]
    if solve_for == "m":
        _require_nonzero(v["g"], "g")
        return v["Fg"] / v["g"]
    _require_nonzero(v["m"], "m")
    return v["Fg"] / v["m"]


def _solve_work(
    solve_for: str,
    v: dict[str, Decimal],
) -> Decimal:
    if solve_for == "W":
        return v["F"] * v["s"]

    if solve_for == "F":
        _require_nonzero(v["s"], "s")
        return v["W"] / v["s"]

    _require_nonzero(v["F"], "F")
    return v["W"] / v["F"]


def _solve_mechanical_power(
    solve_for: str,
    v: dict[str, Decimal],
) -> Decimal:
    if solve_for == "P":
        _require_nonzero(v["t"], "t")
        return v["W"] / v["t"]

    if solve_for == "W":
        return v["P"] * v["t"]

    _require_nonzero(v["P"], "P")
    return v["W"] / v["P"]


def _solve_kinetic_energy(
    solve_for: str,
    v: dict[str, Decimal],
) -> Decimal:
    two = Decimal("2")

    if solve_for == "Ek":
        return v["m"] * v["v"] * v["v"] / two

    if solve_for == "m":
        denominator = v["v"] * v["v"]
        _require_nonzero(denominator, "v")
        return two * v["Ek"] / denominator

    _require_nonzero(v["m"], "m")
    value = two * v["Ek"] / v["m"]
    _require_positive_or_zero(value, "Ek")
    return value.sqrt()


def _solve_potential_energy(
    solve_for: str,
    v: dict[str, Decimal],
) -> Decimal:
    if solve_for == "Ep":
        return v["m"] * v["g"] * v["h"]

    if solve_for == "m":
        denominator = v["g"] * v["h"]
        _require_nonzero(denominator, "g*h")
        return v["Ep"] / denominator

    if solve_for == "g":
        denominator = v["m"] * v["h"]
        _require_nonzero(denominator, "m*h")
        return v["Ep"] / denominator

    denominator = v["m"] * v["g"]
    _require_nonzero(denominator, "m*g")
    return v["Ep"] / denominator


def _solve_thermal_energy(
    solve_for: str,
    v: dict[str, Decimal],
) -> Decimal:
    if solve_for == "Q":
        return v["m"] * v["c"] * v["dT"]

    if solve_for == "m":
        denominator = v["c"] * v["dT"]
        _require_nonzero(denominator, "c*dT")
        return v["Q"] / denominator

    if solve_for == "c":
        denominator = v["m"] * v["dT"]
        _require_nonzero(denominator, "m*dT")
        return v["Q"] / denominator

    denominator = v["m"] * v["c"]
    _require_nonzero(denominator, "m*c")
    return v["Q"] / denominator


def _solve_efficiency_energy(
    solve_for: str,
    v: dict[str, Decimal],
) -> Decimal:
    hundred = Decimal("100")

    if solve_for == "eta":
        _require_nonzero(v["Ein"], "Ein")
        return v["Eout"] / v["Ein"] * hundred

    if solve_for == "Eout":
        return v["eta"] / hundred * v["Ein"]

    _require_nonzero(v["eta"], "eta")
    return v["Eout"] * hundred / v["eta"]


def _solve_efficiency_power(
    solve_for: str,
    v: dict[str, Decimal],
) -> Decimal:
    hundred = Decimal("100")

    if solve_for == "eta":
        _require_nonzero(v["Pin"], "Pin")
        return v["Pout"] / v["Pin"] * hundred

    if solve_for == "Pout":
        return v["eta"] / hundred * v["Pin"]

    _require_nonzero(v["eta"], "eta")
    return v["Pout"] * hundred / v["eta"]


def _solve_density(
    solve_for: str,
    v: dict[str, Decimal],
) -> Decimal:
    if solve_for == "rho":
        _require_nonzero(v["V"], "V")
        return v["m"] / v["V"]

    if solve_for == "m":
        return v["rho"] * v["V"]

    _require_nonzero(v["rho"], "rho")
    return v["m"] / v["rho"]


def _solve_pressure(
    solve_for: str,
    v: dict[str, Decimal],
) -> Decimal:
    if solve_for == "p":
        _require_nonzero(v["A"], "A")
        return v["F"] / v["A"]

    if solve_for == "F":
        return v["p"] * v["A"]

    _require_nonzero(v["p"], "p")
    return v["F"] / v["p"]


def _solve_electric_power(
    solve_for: str,
    v: dict[str, Decimal],
) -> Decimal:
    if solve_for == "P":
        if "U" in v and "I" in v:
            return v["U"] * v["I"]
        if "U" in v and "R" in v:
            _require_nonzero(v["R"], "R")
            return v["U"] * v["U"] / v["R"]
        _require_nonzero(v["R"], "R")
        return v["I"] * v["I"] * v["R"]

    if solve_for == "U":
        if "I" in v:
            _require_nonzero(v["I"], "I")
            return v["P"] / v["I"]
        _require_nonzero(v["R"], "R")
        return (v["P"] * v["R"]).sqrt()

    if "U" in v:
        _require_nonzero(v["U"], "U")
        return v["P"] / v["U"]
    _require_nonzero(v["R"], "R")
    return (v["P"] / v["R"]).sqrt()


def _solve_ohm(
    solve_for: str,
    v: dict[str, Decimal],
) -> Decimal:
    if solve_for == "U":
        return v["R"] * v["I"]

    if solve_for == "R":
        _require_nonzero(v["I"], "I")
        return v["U"] / v["I"]

    _require_nonzero(v["R"], "R")
    return v["U"] / v["R"]


def _solve_wave_speed(solve_for: str, v: dict[str, Decimal]) -> Decimal:
    if solve_for == "v":
        return v["f"] * v["lambda"]
    if solve_for == "f":
        _require_nonzero(v["lambda"], "lambda")
        return v["v"] / v["lambda"]
    _require_nonzero(v["f"], "f")
    return v["v"] / v["f"]


def _solve_frequency_period(solve_for: str, v: dict[str, Decimal]) -> Decimal:
    if solve_for == "f":
        _require_nonzero(v["T"], "T")
        return Decimal("1") / v["T"]
    _require_nonzero(v["f"], "f")
    return Decimal("1") / v["f"]


def _solve_echo_distance(solve_for: str, v: dict[str, Decimal]) -> Decimal:
    if solve_for == "d":
        return v["v"] * v["t"] / Decimal("2")
    if solve_for == "v":
        _require_nonzero(v["t"], "t")
        return Decimal("2") * v["d"] / v["t"]
    _require_nonzero(v["v"], "v")
    return Decimal("2") * v["d"] / v["v"]


def _build_substitution(
    formula_key: str,
    solve_for: str,
    values: dict[str, Decimal],
    decimal_separator: str,
) -> str:
    formatted_values = {
        key: format_decimal(value, decimal_separator)
        for key, value in values.items()
    }

    s = display_symbol(solve_for)

    if formula_key == "motion":
        if solve_for == "v":
            return f"v = {formatted_values['s']} / {formatted_values['t']}"
        if solve_for == "s":
            return f"s = {formatted_values['v']} · {formatted_values['t']}"
        return f"t = {formatted_values['s']} / {formatted_values['v']}"

    if formula_key == "acceleration":
        if solve_for == "a":
            return f"a = {formatted_values['dv']} / {formatted_values['dt']}"
        if solve_for == "dv":
            return f"Δv = {formatted_values['a']} · {formatted_values['dt']}"
        return f"Δt = {formatted_values['dv']} / {formatted_values['a']}"

    if formula_key in ("constant_acceleration", "free_fall"):
        second_term = "a" if formula_key == "constant_acceleration" else "g"
        if solve_for == "v":
            return f"v = {formatted_values['v0']} + {formatted_values[second_term]} · {formatted_values['t']}"
        if solve_for == "v0":
            return f"v₀ = {formatted_values['v']} − {formatted_values[second_term]} · {formatted_values['t']}"
        if solve_for == second_term:
            return f"{display_symbol(second_term)} = ({formatted_values['v']} − {formatted_values['v0']}) / {formatted_values['t']}"
        return f"t = ({formatted_values['v']} − {formatted_values['v0']}) / {formatted_values[second_term]}"

    if formula_key == "force":
        if solve_for == "F":
            return f"F = {formatted_values['m']} · {formatted_values['a']}"
        if solve_for == "m":
            return f"m = {formatted_values['F']} / {formatted_values['a']}"
        return f"a = {formatted_values['F']} / {formatted_values['m']}"

    if formula_key == "weight":
        if solve_for == "Fg":
            return f"F_g = {formatted_values['m']} · {formatted_values['g']}"
        if solve_for == "m":
            return f"m = {formatted_values['Fg']} / {formatted_values['g']}"
        return f"g = {formatted_values['Fg']} / {formatted_values['m']}"

    if formula_key == "work":
        if solve_for == "W":
            return f"W = {formatted_values['F']} · {formatted_values['s']}"
        if solve_for == "F":
            return f"F = {formatted_values['W']} / {formatted_values['s']}"
        return f"s = {formatted_values['W']} / {formatted_values['F']}"

    if formula_key == "mechanical_power":
        if solve_for == "P":
            return f"P = {formatted_values['W']} / {formatted_values['t']}"
        if solve_for == "W":
            return f"W = {formatted_values['P']} · {formatted_values['t']}"
        return f"t = {formatted_values['W']} / {formatted_values['P']}"

    if formula_key == "kinetic_energy":
        if solve_for == "Ek":
            return (
                f"Eₖ = ½ · {formatted_values['m']} · "
                f"{formatted_values['v']}²"
            )
        if solve_for == "m":
            return (
                f"m = 2 · {formatted_values['Ek']} / "
                f"{formatted_values['v']}²"
            )
        return (
            f"v = √(2 · {formatted_values['Ek']} / "
            f"{formatted_values['m']})"
        )

    if formula_key == "potential_energy":
        if solve_for == "Ep":
            return (
                f"Eₚ = {formatted_values['m']} · "
                f"{formatted_values['g']} · {formatted_values['h']}"
            )
        if solve_for == "m":
            return (
                f"m = {formatted_values['Ep']} / "
                f"({formatted_values['g']} · {formatted_values['h']})"
            )
        if solve_for == "g":
            return (
                f"g = {formatted_values['Ep']} / "
                f"({formatted_values['m']} · {formatted_values['h']})"
            )
        return (
            f"h = {formatted_values['Ep']} / "
            f"({formatted_values['m']} · {formatted_values['g']})"
        )

    if formula_key == "thermal_energy":
        if solve_for == "Q":
            return (
                f"Q = {formatted_values['m']} · "
                f"{formatted_values['c']} · {formatted_values['dT']}"
            )
        if solve_for == "m":
            return (
                f"m = {formatted_values['Q']} / "
                f"({formatted_values['c']} · {formatted_values['dT']})"
            )
        if solve_for == "c":
            return (
                f"c = {formatted_values['Q']} / "
                f"({formatted_values['m']} · {formatted_values['dT']})"
            )
        return (
            f"ΔT = {formatted_values['Q']} / "
            f"({formatted_values['m']} · {formatted_values['c']})"
        )

    if formula_key == "efficiency_energy":
        if solve_for == "eta":
            return (
                f"η = {formatted_values['Eout']} / "
                f"{formatted_values['Ein']} · 100"
            )
        if solve_for == "Eout":
            return (
                f"E_out = {formatted_values['eta']} / 100 · "
                f"{formatted_values['Ein']}"
            )
        return (
            f"E_in = {formatted_values['Eout']} · 100 / "
            f"{formatted_values['eta']}"
        )

    if formula_key == "efficiency_power":
        if solve_for == "eta":
            return (
                f"η = {formatted_values['Pout']} / "
                f"{formatted_values['Pin']} · 100"
            )
        if solve_for == "Pout":
            return (
                f"P_out = {formatted_values['eta']} / 100 · "
                f"{formatted_values['Pin']}"
            )
        return (
            f"P_in = {formatted_values['Pout']} · 100 / "
            f"{formatted_values['eta']}"
        )

    if formula_key == "density":
        if solve_for == "rho":
            return f"ρ = {formatted_values['m']} / {formatted_values['V']}"
        if solve_for == "m":
            return f"m = {formatted_values['rho']} · {formatted_values['V']}"
        return f"V = {formatted_values['m']} / {formatted_values['rho']}"

    if formula_key == "pressure":
        if solve_for == "p":
            return f"p = {formatted_values['F']} / {formatted_values['A']}"
        if solve_for == "F":
            return f"F = {formatted_values['p']} · {formatted_values['A']}"
        return f"A = {formatted_values['F']} / {formatted_values['p']}"

    if formula_key == "electric_power":
        if solve_for == "P":
            if "I" in formatted_values:
                return f"P = {formatted_values['U']} · {formatted_values['I']}"
            if "R" in formatted_values:
                return f"P = {formatted_values['U']}² / {formatted_values['R']}"
            return f"P = {formatted_values['I']}² · {formatted_values['R']}"
        if solve_for == "U":
            if "I" in formatted_values:
                return f"U = {formatted_values['P']} / {formatted_values['I']}"
            return f"U = √({formatted_values['P']} · {formatted_values['R']})"
        if solve_for == "I":
            if "U" in formatted_values:
                return f"I = {formatted_values['P']} / {formatted_values['U']}"
            return f"I = √({formatted_values['P']} / {formatted_values['R']})"
        return f"R = {formatted_values['U']}² / {formatted_values['P']}"

    if formula_key == "ohm":
        if solve_for == "U":
            return f"U = {formatted_values['R']} · {formatted_values['I']}"
        if solve_for == "R":
            return f"R = {formatted_values['U']} / {formatted_values['I']}"
        return f"I = {formatted_values['U']} / {formatted_values['R']}"

    if formula_key == "wave_speed":
        if solve_for == "v":
            return f"v = {formatted_values['f']} · {formatted_values['lambda']}"
        if solve_for == "f":
            return f"f = {formatted_values['v']} / {formatted_values['lambda']}"
        return f"λ = {formatted_values['v']} / {formatted_values['f']}"

    if formula_key == "frequency_period":
        if solve_for == "f":
            return f"f = 1 / {formatted_values['T']}"
        return f"T = 1 / {formatted_values['f']}"

    if formula_key == "sound_distance":
        if solve_for == "s":
            return f"s = {formatted_values['v']} · {formatted_values['t']}"
        if solve_for == "v":
            return f"v = {formatted_values['s']} / {formatted_values['t']}"
        return f"t = {formatted_values['s']} / {formatted_values['v']}"

    if formula_key == "echo_distance":
        if solve_for == "d":
            return f"d = {formatted_values['v']} · {formatted_values['t']} / 2"
        if solve_for == "v":
            return f"v = 2 · {formatted_values['d']} / {formatted_values['t']}"
        return f"t = 2 · {formatted_values['d']} / {formatted_values['v']}"

    raise ValueError(f"unknown_formula:{s}")
