import json
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.formulas_view import FormulasView
from app.physics_view import PhysicsView
from app.quantities_view import QuantitiesView
from app.theme import THEME
from core.conversion_engine import convert
from core.conversion_registry import CATEGORIES, category_codes
from core.decimal_utils import parse_decimal
from core.explanations import build_explanation
from core.exercise_solver import solve_conversion_exercise


BASE_DIR = Path(__file__).resolve().parent.parent
LOCALES_DIR = BASE_DIR / "locales"


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.current_language = "es"
        self.translations: dict = {}
        self.unit_codes: list[str] = []
        self.current_category = "length"

        self._build_ui()
        self._load_language("es")

    def _card(self, name: str = "card") -> QFrame:
        card = QFrame()
        card.setObjectName(name)
        return card

    def _build_ui(self) -> None:
        self.setMinimumSize(900, 640)
        self.resize(1080, 760)
        self.setStyleSheet(THEME)

        root = QWidget()
        self.setCentralWidget(root)

        outer = QVBoxLayout(root)
        outer.setContentsMargins(28, 20, 28, 18)
        outer.setSpacing(14)

        header = QHBoxLayout()

        title_box = QVBoxLayout()

        self.title_label = QLabel()
        self.title_label.setStyleSheet(
            "font-size: 25px; font-weight: 700;"
        )

        self.subtitle_label = QLabel()
        self.subtitle_label.setObjectName("subtitle")

        title_box.addWidget(self.title_label)
        title_box.addWidget(self.subtitle_label)

        header.addLayout(title_box)
        header.addStretch()

        language_box = QVBoxLayout()

        self.language_label = QLabel()
        self.language_label.setObjectName("eyebrow")

        self.language_combo = QComboBox()
        self.language_combo.addItem("Español", "es")
        self.language_combo.addItem("Suomi", "fi")
        self.language_combo.currentIndexChanged.connect(
            self._on_language_changed
        )

        language_box.addWidget(self.language_label)
        language_box.addWidget(self.language_combo)

        header.addLayout(language_box)
        outer.addLayout(header)

        body = QHBoxLayout()
        body.setSpacing(18)

        nav = self._card("navCard")
        nav.setFixedWidth(188)

        nav_layout = QVBoxLayout(nav)
        nav_layout.setContentsMargins(14, 16, 14, 14)
        nav_layout.setSpacing(6)

        self.nav_title = QLabel()
        self.nav_title.setObjectName("navTitle")

        self.nav_conversions = QPushButton()
        self.nav_conversions.setObjectName("navButton")
        self.nav_conversions.setProperty("active", True)
        self.nav_conversions.clicked.connect(
            lambda: self._show_page(0)
        )

        self.nav_quantities = QPushButton()
        self.nav_quantities.setObjectName("navButton")
        self.nav_quantities.clicked.connect(
            lambda: self._show_page(1)
        )

        self.nav_formulas = QPushButton()
        self.nav_formulas.setObjectName("navButton")
        self.nav_formulas.clicked.connect(
            lambda: self._show_page(2)
        )

        self.nav_physics = QPushButton()
        self.nav_physics.setObjectName("navButton")
        self.nav_physics.clicked.connect(
            lambda: self._show_page(3)
        )

        self.nav_chemistry = QPushButton()
        self.nav_chemistry.setObjectName("navButton")
        self.nav_chemistry.setEnabled(False)

        for item in (
            self.nav_title,
            self.nav_conversions,
            self.nav_quantities,
            self.nav_formulas,
            self.nav_physics,
            self.nav_chemistry,
        ):
            nav_layout.addWidget(item)

        nav_layout.addStretch()
        body.addWidget(nav)

        self.pages = QStackedWidget()

        page_scroll = QScrollArea()
        page_scroll.setObjectName("pageScroll")
        page_scroll.setWidgetResizable(True)
        page_scroll.setFrameShape(QFrame.NoFrame)
        page_scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )
        page_scroll.setWidget(self.pages)
        body.addWidget(page_scroll, 1)

        self.conversion_page = self._build_conversion_page()
        self.quantities_page = QuantitiesView()
        self.formulas_page = FormulasView()
        self.physics_page = PhysicsView()

        self.pages.addWidget(self.conversion_page)
        self.pages.addWidget(self.quantities_page)
        self.pages.addWidget(self.formulas_page)
        self.pages.addWidget(self.physics_page)

        outer.addLayout(body, 1)

        self.statusBar()

    def _build_conversion_page(self) -> QWidget:
        page = QWidget()

        content = QVBoxLayout(page)
        content.setContentsMargins(0, 0, 0, 0)
        content.setSpacing(14)

        exercise_card = self._card()
        exercise_layout = QVBoxLayout(exercise_card)
        exercise_layout.setContentsMargins(20, 16, 20, 16)
        exercise_layout.setSpacing(8)

        self.exercise_heading = QLabel()
        self.exercise_heading.setObjectName("sectionTitle")

        exercise_row = QHBoxLayout()
        exercise_row.setSpacing(10)

        self.exercise_input = QLineEdit()
        self.exercise_input.returnPressed.connect(
            self.solve_exercise
        )

        self.exercise_button = QPushButton()
        self.exercise_button.setObjectName("primaryButton")
        self.exercise_button.clicked.connect(
            self.solve_exercise
        )

        exercise_row.addWidget(self.exercise_input, 1)
        exercise_row.addWidget(self.exercise_button)

        self.exercise_examples = QLabel()
        self.exercise_examples.setObjectName("muted")
        self.exercise_examples.setWordWrap(True)

        exercise_layout.addWidget(self.exercise_heading)
        exercise_layout.addLayout(exercise_row)
        exercise_layout.addWidget(self.exercise_examples)

        content.addWidget(exercise_card)

        controls = self._card()

        grid = QGridLayout(controls)
        grid.setContentsMargins(18, 16, 18, 18)
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(6)
        controls.setMinimumHeight(280)

        self.category_label = QLabel()
        self.category_label.setObjectName("eyebrow")

        self.category_combo = QComboBox()
        self.category_combo.currentIndexChanged.connect(
            self._on_category_changed
        )

        grid.addWidget(self.category_label, 0, 0, 1, 5)
        grid.addWidget(self.category_combo, 1, 0, 1, 5)

        self.value_label = QLabel()
        self.value_label.setObjectName("eyebrow")

        self.value_input = QLineEdit()
        self.value_input.returnPressed.connect(self.calculate)

        grid.addWidget(self.value_label, 2, 0, 1, 5)
        grid.addWidget(self.value_input, 3, 0, 1, 5)

        self.from_label = QLabel()
        self.to_label = QLabel()
        self.from_label.setObjectName("eyebrow")
        self.to_label.setObjectName("eyebrow")

        self.from_combo = QComboBox()
        self.to_combo = QComboBox()

        self.swap_button = QPushButton("⇄")
        self.swap_button.setObjectName("iconButton")
        self.swap_button.clicked.connect(self.swap_units)

        grid.addWidget(self.from_label, 4, 0, 1, 2)
        grid.addWidget(self.to_label, 4, 3, 1, 2)

        grid.addWidget(self.from_combo, 5, 0, 1, 2)
        grid.addWidget(self.swap_button, 5, 2)
        grid.addWidget(self.to_combo, 5, 3, 1, 2)

        actions = QHBoxLayout()
        actions.setContentsMargins(0, 12, 0, 0)

        self.clear_button = QPushButton()

        self.calculate_button = QPushButton()
        self.calculate_button.setObjectName("primaryButton")

        self.clear_button.clicked.connect(self.clear)
        self.calculate_button.clicked.connect(self.calculate)

        actions.addStretch()
        actions.addWidget(self.clear_button)
        actions.addWidget(self.calculate_button)

        grid.addLayout(actions, 6, 0, 1, 5)

        for column in (0, 1, 3, 4):
            grid.setColumnStretch(column, 1)
        grid.setColumnMinimumWidth(2, 34)

        # Keep the label/control rhythm stable when the page is resized.
        # The card can grow, but these rows must never collapse into one
        # another.
        for row in (0, 2, 4):
            grid.setRowMinimumHeight(row, 18)
        for row in (1, 3, 5):
            grid.setRowMinimumHeight(row, 38)
        grid.setRowMinimumHeight(6, 46)

        content.addWidget(controls)

        result = self._card()

        result_layout = QVBoxLayout(result)
        result_layout.setContentsMargins(18, 12, 18, 12)

        result_header = QHBoxLayout()

        self.result_heading = QLabel()
        self.result_heading.setObjectName("eyebrow")

        self.copy_button = QPushButton()
        self.copy_button.setEnabled(False)
        self.copy_button.clicked.connect(self.copy_result)

        result_header.addWidget(self.result_heading)
        result_header.addStretch()
        result_header.addWidget(self.copy_button)

        result_layout.addLayout(result_header)

        self.result_value = QLabel()
        self.result_value.setObjectName("resultValue")
        self.result_value.setTextInteractionFlags(
            Qt.TextSelectableByMouse
        )

        result_layout.addWidget(self.result_value)

        content.addWidget(result)

        explanation = self._card()

        explanation_layout = QVBoxLayout(explanation)
        explanation_layout.setContentsMargins(18, 12, 18, 12)
        explanation_layout.setSpacing(6)

        self.formula_heading = QLabel()
        self.formula_heading.setObjectName("sectionTitle")

        self.formula_value = QLabel("—")
        self.formula_value.setTextInteractionFlags(
            Qt.TextSelectableByMouse
        )

        self.calculation_heading = QLabel()
        self.calculation_heading.setObjectName("sectionTitle")

        self.calculation_value = QLabel("—")

        self.note_heading = QLabel()
        self.note_heading.setObjectName("sectionTitle")

        self.note_value = QLabel()
        self.note_value.setObjectName("note")
        self.note_value.setWordWrap(True)

        for widget in (
            self.formula_heading,
            self.formula_value,
            self.calculation_heading,
            self.calculation_value,
            self.note_heading,
            self.note_value,
        ):
            explanation_layout.addWidget(widget)

        content.addWidget(explanation)
        content.addStretch()

        return page

    def _show_page(self, index: int) -> None:
        self.pages.setCurrentIndex(index)

        for button, active in (
            (self.nav_conversions, index == 0),
            (self.nav_quantities, index == 1),
            (self.nav_formulas, index == 2),
            (self.nav_physics, index == 3),
        ):
            button.setProperty("active", active)
            button.style().unpolish(button)
            button.style().polish(button)

    def _load_language(self, language: str) -> None:
        with (
            LOCALES_DIR / f"{language}.json"
        ).open(encoding="utf-8") as file:
            self.translations = json.load(file)

        self.current_language = language
        self._apply_translations()

    def _apply_translations(self) -> None:
        t = self.translations

        self.setWindowTitle(t["app_title"])
        self.title_label.setText(t["app_title"])
        self.subtitle_label.setText(t["subtitle"])
        self.language_label.setText(t["language"])

        self.nav_title.setText(t["navigation"])
        self.nav_conversions.setText(t["conversions"])
        self.nav_quantities.setText(t["quantities_nav"])
        self.nav_formulas.setText(t["formulas_nav"])
        self.nav_physics.setText(t["physics"])
        self.nav_chemistry.setText(t["chemistry"])

        self.category_label.setText(t["category"])
        self.value_label.setText(t["value"])
        self.value_input.setPlaceholderText(t["enter_value"])
        self.from_label.setText(t["from_unit"])
        self.to_label.setText(t["to_unit"])

        self.calculate_button.setText(t["calculate"])
        self.clear_button.setText(t["clear"])

        self.copy_button.setText(t["copy"])
        self.copy_button.setToolTip(t["copy"])

        self.swap_button.setToolTip(t["swap_tooltip"])

        self.result_heading.setText(t["result"])
        self.formula_heading.setText(t["relationship"])
        self.calculation_heading.setText(t["calculation"])
        self.note_heading.setText(t["learning_note"])

        self.exercise_heading.setText(t["exercise_solver"])
        self.exercise_input.setPlaceholderText(
            t["exercise_placeholder"]
        )
        self.exercise_button.setText(t["solve"])
        self.exercise_examples.setText(t["exercise_examples"])

        selected_category = self.current_category

        self.category_combo.blockSignals(True)
        self.category_combo.clear()

        for code in category_codes():
            self.category_combo.addItem(
                t["categories"][code],
                code,
            )

        self.category_combo.setCurrentIndex(
            self.category_combo.findData(selected_category)
        )
        self.category_combo.blockSignals(False)

        self.unit_codes = list(
            CATEGORIES[selected_category].unit_codes
        )

        defaults = CATEGORIES[selected_category].defaults

        current_from = self.from_combo.currentData()
        current_to = self.to_combo.currentData()

        selected_from = (
            current_from
            if current_from in self.unit_codes
            else defaults[0]
        )

        selected_to = (
            current_to
            if current_to in self.unit_codes
            else defaults[1]
        )

        self._populate(self.from_combo, selected_from)
        self._populate(self.to_combo, selected_to)

        self.quantities_page.set_translations(t)
        self.formulas_page.set_translations(t)
        self.physics_page.set_translations(t)

        if not self.result_value.text():
            self.result_value.setText(t["result_empty"])
            self.note_value.setText(t["empty_state"])
        elif (
            self.value_input.text().strip()
            and self.copy_button.isEnabled()
        ):
            self.calculate()

        self.statusBar().showMessage(t["ready"])

    def _populate(
        self,
        combo: QComboBox,
        selected: str,
    ) -> None:
        combo.blockSignals(True)
        combo.clear()

        for code in self.unit_codes:
            combo.addItem(
                self.translations["units"][code],
                code,
            )

        index = combo.findData(selected)
        combo.setCurrentIndex(
            index if index >= 0 else 0
        )

        combo.blockSignals(False)

    def _on_language_changed(self) -> None:
        code = self.language_combo.currentData()

        if code:
            self._load_language(code)

    def _on_category_changed(self) -> None:
        self.current_category = (
            self.category_combo.currentData()
            or "length"
        )

        self.unit_codes = list(
            CATEGORIES[self.current_category].unit_codes
        )

        source, target = (
            CATEGORIES[self.current_category].defaults
        )

        self._populate(self.from_combo, source)
        self._populate(self.to_combo, target)
        self.clear()

    def calculate(self) -> None:
        try:
            value = parse_decimal(
                self.value_input.text()
            )

            source = self.from_combo.currentData()
            target = self.to_combo.currentData()

            result = convert(
                value,
                self.current_category,
                source,
                target,
            )

            self.result_value.setText(
                f"{result.formatted_value} {target}"
            )

            self.copy_button.setEnabled(True)
            self.formula_value.setText(result.formula)
            self.calculation_value.setText(
                result.steps[0]
            )

            _, _, note = build_explanation(
                value,
                self.current_category,
                source,
                target,
                result.value,
                self.current_language,
            )

            self.note_value.setText(note)

            self.statusBar().showMessage(
                self.translations["result"]
            )

        except ValueError as exc:
            QMessageBox.warning(
                self,
                self.translations["app_title"],
                self.translations.get(
                    str(exc),
                    self.translations[
                        "unexpected_error"
                    ],
                ),
            )

    def solve_exercise(self) -> None:
        try:
            solution = solve_conversion_exercise(
                self.exercise_input.text()
            )

            self.current_category = solution.category

            category_index = self.category_combo.findData(
                solution.category
            )

            self.category_combo.blockSignals(True)

            if category_index >= 0:
                self.category_combo.setCurrentIndex(
                    category_index
                )

            self.category_combo.blockSignals(False)

            self.unit_codes = list(
                CATEGORIES[solution.category].unit_codes
            )

            self._populate(
                self.from_combo,
                solution.source_unit,
            )

            self._populate(
                self.to_combo,
                solution.target_unit,
            )

            input_text = str(solution.input_value).replace(
                ".",
                ",",
            )

            self.value_input.setText(input_text)

            self.result_value.setText(
                f"{solution.formatted_value} "
                f"{solution.target_unit}"
            )

            self.copy_button.setEnabled(True)

            self.formula_value.setText(
                solution.formula
            )

            self.calculation_value.setText(
                solution.calculation
            )

            _, _, note = build_explanation(
                solution.input_value,
                solution.category,
                solution.source_unit,
                solution.target_unit,
                solution.result_value,
                self.current_language,
            )

            self.note_value.setText(note)

            self.statusBar().showMessage(
                self.translations["result"]
            )

        except ValueError as exc:
            key = str(exc)

            QMessageBox.warning(
                self,
                self.translations["app_title"],
                self.translations.get(
                    key,
                    self.translations["unexpected_error"],
                ),
            )

    def swap_units(self) -> None:
        source = self.from_combo.currentData()
        target = self.to_combo.currentData()

        self._populate(self.from_combo, target)
        self._populate(self.to_combo, source)

        if self.value_input.text().strip():
            self.calculate()

    def copy_result(self) -> None:
        if not self.copy_button.isEnabled():
            return

        QApplication.clipboard().setText(
            self.result_value.text()
        )

        self.statusBar().showMessage(
            self.translations["copied"]
        )

    def clear(self) -> None:
        self.value_input.clear()

        self.result_value.setText(
            self.translations["result_empty"]
        )

        self.copy_button.setEnabled(False)

        self.formula_value.setText("—")
        self.calculation_value.setText("—")

        self.note_value.setText(
            self.translations["empty_state"]
        )

        self.statusBar().showMessage(
            self.translations["ready"]
        )

        self.value_input.setFocus()
