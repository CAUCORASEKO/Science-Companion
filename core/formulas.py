from dataclasses import dataclass


@dataclass(frozen=True)
class Formula:
    key: str
    category: str
    expression: str
    variables: tuple[tuple[str, str, str], ...]


FORMULAS = (
    # Motion
    Formula(
        key="speed",
        category="motion",
        expression="v = s / t",
        variables=(
            ("v", "speed", "m/s"),
            ("s", "distance", "m"),
            ("t", "time", "s"),
        ),
    ),
    Formula(
        key="distance",
        category="motion",
        expression="s = v · t",
        variables=(
            ("s", "distance", "m"),
            ("v", "speed", "m/s"),
            ("t", "time", "s"),
        ),
    ),
    Formula(
        key="time_from_motion",
        category="motion",
        expression="t = s / v",
        variables=(
            ("t", "time", "s"),
            ("s", "distance", "m"),
            ("v", "speed", "m/s"),
        ),
    ),
    Formula(
        key="acceleration",
        category="motion",
        expression="a = Δv / Δt",
        variables=(
            ("a", "acceleration", "m/s²"),
            ("Δv", "change_in_speed", "m/s"),
            ("Δt", "time_interval", "s"),
        ),
    ),
    Formula(
        key="constant_acceleration_velocity",
        category="motion",
        expression="v = v₀ + a · t",
        variables=(
            ("v", "speed", "m/s"),
            ("v₀", "initial_speed", "m/s"),
            ("a", "acceleration", "m/s²"),
            ("t", "time", "s"),
        ),
    ),
    Formula(
        key="free_fall",
        category="motion",
        expression="v = v₀ + g · t",
        variables=(
            ("v", "speed", "m/s"),
            ("v₀", "initial_speed", "m/s"),
            ("g", "gravity", "m/s²"),
            ("t", "time", "s"),
        ),
    ),

    # Forces
    Formula(
        key="newton_second_law",
        category="forces",
        expression="F = m · a",
        variables=(
            ("F", "force", "N"),
            ("m", "mass", "kg"),
            ("a", "acceleration", "m/s²"),
        ),
    ),
    Formula(
        key="acceleration_from_force",
        category="forces",
        expression="a = F / m",
        variables=(
            ("a", "acceleration", "m/s²"),
            ("F", "force", "N"),
            ("m", "mass", "kg"),
        ),
    ),
    Formula(
        key="mass_from_force",
        category="forces",
        expression="m = F / a",
        variables=(
            ("m", "mass", "kg"),
            ("F", "force", "N"),
            ("a", "acceleration", "m/s²"),
        ),
    ),
    Formula(
        key="weight",
        category="forces",
        expression="F_g = m · g",
        variables=(
            ("F_g", "weight", "N"),
            ("m", "mass", "kg"),
            ("g", "gravity", "m/s²"),
        ),
    ),

    # Work and energy
    Formula(
        key="work",
        category="energy",
        expression="W = F · s",
        variables=(
            ("W", "work", "J"),
            ("F", "force", "N"),
            ("s", "distance", "m"),
        ),
    ),
    Formula(
        key="power",
        category="energy",
        expression="P = W / t",
        variables=(
            ("P", "power", "W"),
            ("W", "work", "J"),
            ("t", "time", "s"),
        ),
    ),
    Formula(
        key="kinetic_energy",
        category="energy",
        expression="Eₖ = ½ · m · v²",
        variables=(
            ("Eₖ", "kinetic_energy", "J"),
            ("m", "mass", "kg"),
            ("v", "speed", "m/s"),
        ),
    ),
    Formula(
        key="potential_energy",
        category="energy",
        expression="Eₚ = m · g · h",
        variables=(
            ("Eₚ", "potential_energy", "J"),
            ("m", "mass", "kg"),
            ("g", "gravity", "m/s²"),
            ("h", "height", "m"),
        ),
    ),

    Formula(
        key="thermal_energy",
        category="energy",
        expression="Q = m · c · ΔT",
        variables=(
            ("Q", "thermal_energy", "J"),
            ("m", "mass", "kg"),
            ("c", "specific_heat_capacity", "J/(kg·K)"),
            ("ΔT", "temperature_change", "K"),
        ),
    ),
    Formula(
        key="efficiency_energy",
        category="energy",
        expression="η = E_out / E_in · 100 %",
        variables=(
            ("η", "efficiency", "%"),
            ("E_out", "useful_energy", "J"),
            ("E_in", "input_energy", "J"),
        ),
    ),
    Formula(
        key="efficiency_power",
        category="energy",
        expression="η = P_out / P_in · 100 %",
        variables=(
            ("η", "efficiency", "%"),
            ("P_out", "useful_power", "W"),
            ("P_in", "input_power", "W"),
        ),
    ),

    # Matter
    Formula(
        key="density",
        category="matter",
        expression="ρ = m / V",
        variables=(
            ("ρ", "density", "kg/m³"),
            ("m", "mass", "kg"),
            ("V", "volume", "m³"),
        ),
    ),
    Formula(
        key="pressure",
        category="matter",
        expression="p = F / A",
        variables=(
            ("p", "pressure", "Pa"),
            ("F", "force", "N"),
            ("A", "area", "m²"),
        ),
    ),

    # Electricity
    Formula(
        key="electric_power",
        category="electricity",
        expression="P = U · I",
        variables=(
            ("P", "power", "W"),
            ("U", "voltage", "V"),
            ("I", "electric_current", "A"),
        ),
    ),
    Formula(
        key="ohms_law",
        category="electricity",
        expression="U = R · I",
        variables=(
            ("U", "voltage", "V"),
            ("R", "resistance", "Ω"),
            ("I", "electric_current", "A"),
        ),
    ),
    Formula(
        key="current",
        category="electricity",
        expression="I = U / R",
        variables=(
            ("I", "electric_current", "A"),
            ("U", "voltage", "V"),
            ("R", "resistance", "Ω"),
        ),
    ),
    Formula(
        key="resistance",
        category="electricity",
        expression="R = U / I",
        variables=(
            ("R", "resistance", "Ω"),
            ("U", "voltage", "V"),
            ("I", "electric_current", "A"),
        ),
    ),
)
