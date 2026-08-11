from decimal import Decimal

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from core.decimal_utils import parse_decimal
from core.physics_calculator import (
    FORMULA_LABELS,
    RESULT_UNITS,
    VARIABLES,
    display_symbol,
    solve_physics,
)
from app.physics_units import to_si, units_for


FORMULA_ORDER = (
    "motion",
    "acceleration",
    "constant_acceleration",
    "free_fall",
    "force",
    "weight",
    "work",
    "mechanical_power",
    "kinetic_energy",
    "potential_energy",
    "thermal_energy",
    "efficiency_energy",
    "efficiency_power",
    "density",
    "pressure",
    "electric_power",
    "ohm",
    "wave_speed",
    "frequency_period",
    "sound_distance",
    "echo_distance",
)

FORMULA_GROUPS = {
    "mechanics": (
        "motion", "acceleration", "constant_acceleration", "free_fall",
        "force", "weight", "work", "mechanical_power", "kinetic_energy",
        "potential_energy",
    ),
    "matter_energy": (
        "thermal_energy", "efficiency_energy", "efficiency_power", "density", "pressure",
    ),
    "electricity": ("ohm", "electric_power"),
    "waves": ("wave_speed", "frequency_period", "sound_distance", "echo_distance"),
}

FORMULA_GROUP_ORDER = tuple(FORMULA_GROUPS)


class PhysicsView(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.translations: dict = {}
        self.current_formula = "motion"
        self.current_target = "v"
        self.input_fields: dict[str, QLineEdit] = {}
        self.input_units: dict[str, QComboBox] = {}

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(14)

        self.title = QLabel()
        self.title.setObjectName("pageTitle")

        self.intro = QLabel()
        self.intro.setObjectName("muted")
        self.intro.setWordWrap(True)

        root.addWidget(self.title)
        root.addWidget(self.intro)

        controls = QFrame()
        controls.setObjectName("card")

        grid = QGridLayout(controls)
        grid.setContentsMargins(18, 16, 18, 18)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(9)

        self.area_label = QLabel()
        self.area_label.setObjectName("eyebrow")

        self.area_combo = QComboBox()
        self.area_combo.currentIndexChanged.connect(self._on_area_changed)

        self.formula_label = QLabel()
        self.formula_label.setObjectName("eyebrow")

        self.formula_combo = QComboBox()
        self.formula_combo.currentIndexChanged.connect(
            self._on_formula_changed
        )

        self.expression_label = QLabel()
        self.expression_label.setObjectName("eyebrow")

        self.expression_value = QLabel()
        self.expression_value.setObjectName("formulaExpression")

        self.target_label = QLabel()
        self.target_label.setObjectName("eyebrow")

        self.target_combo = QComboBox()
        self.target_combo.currentIndexChanged.connect(
            self._on_target_changed
        )

        grid.addWidget(self.area_label, 0, 0)
        grid.addWidget(self.area_combo, 0, 1, 1, 3)

        grid.addWidget(self.formula_label, 1, 0)
        grid.addWidget(self.formula_combo, 1, 1, 1, 3)

        grid.addWidget(self.expression_label, 2, 0)
        grid.addWidget(self.expression_value, 2, 1, 1, 3)

        grid.addWidget(self.target_label, 3, 0)
        grid.addWidget(self.target_combo, 3, 1, 1, 3)

        self.inputs_container = QWidget()
        self.inputs_layout = QGridLayout(self.inputs_container)
        self.inputs_layout.setContentsMargins(0, 5, 0, 0)
        self.inputs_layout.setHorizontalSpacing(12)
        self.inputs_layout.setVerticalSpacing(10)

        grid.addWidget(
            self.inputs_container,
            4,
            0,
            1,
            4,
        )

        actions = QHBoxLayout()

        self.clear_button = QPushButton()
        self.calculate_button = QPushButton()
        self.calculate_button.setObjectName("primaryButton")

        self.clear_button.clicked.connect(self.clear)
        self.calculate_button.clicked.connect(self.calculate)

        actions.addStretch()
        actions.addWidget(self.clear_button)
        actions.addWidget(self.calculate_button)

        actions.setContentsMargins(0, 12, 0, 0)
        grid.addLayout(actions, 5, 0, 1, 4)

        root.addWidget(controls)

        result = QFrame()
        result.setObjectName("card")

        result_layout = QVBoxLayout(result)
        result_layout.setContentsMargins(20, 16, 20, 16)
        result_layout.setSpacing(8)

        self.result_heading = QLabel()
        self.result_heading.setObjectName("eyebrow")

        self.result_value = QLabel()
        self.result_value.setObjectName("resultValue")
        self.result_value.setTextInteractionFlags(
            Qt.TextSelectableByMouse
        )

        self.process_heading = QLabel()
        self.process_heading.setObjectName("sectionTitle")

        self.process_formula = QLabel()
        self.process_substitution = QLabel()
        self.process_result = QLabel()

        for widget in (
            self.result_heading,
            self.result_value,
            self.process_heading,
            self.process_formula,
            self.process_substitution,
            self.process_result,
        ):
            result_layout.addWidget(widget)

        root.addWidget(result)
        root.addStretch()

    def set_translations(self, translations: dict) -> None:
        self.translations = translations

        self.title.setText(translations["physics_title"])
        self.intro.setText(translations["physics_intro"])
        self.area_label.setText(translations["physics_area"])
        self.formula_label.setText(translations["physics_calculation"])
        self.expression_label.setText(
            translations["physics_expression"]
        )
        self.target_label.setText(translations["physics_solve_for"])
        self.clear_button.setText(translations["clear"])
        self.calculate_button.setText(translations["calculate"])
        self.result_heading.setText(translations["result"])
        self.process_heading.setText(
            translations["physics_process"]
        )

        current_formula = self.current_formula
        current_target = self.current_target

        group = next((key for key, formulas in FORMULA_GROUPS.items() if current_formula in formulas), FORMULA_GROUP_ORDER[0])
        self.area_combo.blockSignals(True)
        self.area_combo.clear()
        for key in FORMULA_GROUP_ORDER:
            self.area_combo.addItem(translations["physics_formula_groups"][key], key)
        self.area_combo.setCurrentIndex(self.area_combo.findData(group))
        self.area_combo.blockSignals(False)
        self._populate_formula_combo(current_formula)

        self._populate_targets(current_target)
        self._rebuild_inputs()

        if not self.result_value.text():
            self._reset_result()

    def _populate_formula_combo(self, preferred: str | None = None) -> None:
        group = self.area_combo.currentData() or FORMULA_GROUP_ORDER[0]
        formulas = FORMULA_GROUPS[group]
        self.formula_combo.blockSignals(True)
        self.formula_combo.clear()
        for key in formulas:
            name = self.translations["physics_formula_names"].get(
                key, self.translations.get("physics_formula_names_extra", {}).get(key, key)
            )
            self.formula_combo.addItem(name, key)
        index = self.formula_combo.findData(preferred)
        self.formula_combo.setCurrentIndex(index if index >= 0 else 0)
        self.formula_combo.blockSignals(False)
        self.current_formula = self.formula_combo.currentData() or formulas[0]

    def _on_area_changed(self) -> None:
        if not self.area_combo.currentData():
            return
        previous_target = self.current_target
        self._populate_formula_combo()
        self._populate_targets(previous_target)
        self._rebuild_inputs()
        self._reset_result()

    def _populate_targets(self, preferred: str | None = None) -> None:
        self.target_combo.blockSignals(True)
        self.target_combo.clear()

        variables = VARIABLES[self.current_formula]

        for variable in variables:
            symbol = display_symbol(variable)

            label = self.translations["physics_variables"].get(
                variable,
                self.translations.get("physics_variables_extra", {}).get(variable, variable),
            )

            unit = RESULT_UNITS[
                (self.current_formula, variable)
            ]

            self.target_combo.addItem(
                f"{label} ({symbol}) — {unit}",
                variable,
            )

        if preferred in variables:
            index = self.target_combo.findData(preferred)
        else:
            index = 0

        self.target_combo.setCurrentIndex(
            index if index >= 0 else 0
        )

        self.current_target = (
            self.target_combo.currentData()
            or variables[0]
        )

        self.target_combo.blockSignals(False)

    def _clear_inputs_layout(self) -> None:
        while self.inputs_layout.count():
            item = self.inputs_layout.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

        self.input_fields = {}
        self.input_units = {}

    def _rebuild_inputs(self) -> None:
        self._clear_inputs_layout()

        variables = VARIABLES[self.current_formula]

        row = 0

        for variable in variables:
            if variable == self.current_target:
                continue

            symbol = display_symbol(variable)

            name = self.translations["physics_variables"].get(
                variable,
                self.translations.get("physics_variables_extra", {}).get(variable, variable),
            )

            unit = RESULT_UNITS[
                (self.current_formula, variable)
            ]

            label = QLabel(
                f"{name} ({symbol}) — {unit}"
            )
            label.setObjectName("eyebrow")

            field = QLineEdit()
            field.setPlaceholderText(
                self.translations["physics_enter_value"]
            )
            field.returnPressed.connect(self.calculate)

            self.inputs_layout.addWidget(
                label,
                row,
                0,
            )

            self.inputs_layout.addWidget(
                field,
                row,
                1,
            )

            units = units_for(variable)
            if units:
                unit_combo = QComboBox()
                unit_combo.addItems(units)
                unit_combo.setCurrentIndex(0)
                unit_combo.setToolTip(
                    self.translations.get("physics_unit", "Unit")
                )
                self.inputs_layout.addWidget(
                    unit_combo,
                    row,
                    2,
                )
                self.input_units[variable] = unit_combo

            self.input_fields[variable] = field

            row += 1

        self.expression_value.setText(
            FORMULA_LABELS[self.current_formula]
        )

    def _on_formula_changed(self) -> None:
        key = self.formula_combo.currentData()

        if not key:
            return

        self.current_formula = key
        self._populate_targets()
        self._rebuild_inputs()
        self._reset_result()

    def _on_target_changed(self) -> None:
        target = self.target_combo.currentData()

        if not target:
            return

        self.current_target = target
        self._rebuild_inputs()
        self._reset_result()

    def calculate(self) -> None:
        try:
            values: dict[str, Decimal] = {}

            for variable, field in self.input_fields.items():
                if not field.text().strip():
                    continue
                values[variable] = parse_decimal(field.text())
                unit_combo = self.input_units.get(variable)
                if unit_combo is not None:
                    values[variable] = to_si(
                        values[variable],
                        variable,
                        unit_combo.currentData() or unit_combo.currentText(),
                    )

            result = solve_physics(
                self.current_formula,
                self.current_target,
                values,
            )

            self.result_value.setText(
                f"{result.formatted_value} {result.unit}"
            )

            self.process_formula.setText(
                result.formula
            )

            self.process_substitution.setText(
                result.substituted
            )

            self.process_result.setText(
                result.calculation
            )

        except ValueError as exc:
            key = str(exc)

            if key.startswith("missing_value:"):
                message = self.translations[
                    "physics_missing_value"
                ]

            elif key.startswith("zero_division:"):
                message = self.translations[
                    "physics_zero_division"
                ]

            elif key.startswith("negative_value:"):
                message = self.translations[
                    "physics_negative_value"
                ]

            else:
                message = self.translations.get(
                    key,
                    self.translations[
                        "unexpected_error"
                    ],
                )

            QMessageBox.warning(
                self,
                self.translations["app_title"],
                message,
            )

    def clear(self) -> None:
        for field in self.input_fields.values():
            field.clear()

        self._reset_result()

        if self.input_fields:
            next(iter(self.input_fields.values())).setFocus()

    def _reset_result(self) -> None:
        if not self.translations:
            return

        self.result_value.setText(
            self.translations["result_empty"]
        )

        self.process_formula.setText("—")
        self.process_substitution.setText("—")
        self.process_result.setText("—")
