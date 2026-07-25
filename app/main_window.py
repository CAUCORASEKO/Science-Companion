import json
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QComboBox, QFrame, QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QMessageBox, QPushButton, QVBoxLayout, QWidget,
)

from app.theme import THEME
from core.conversion_engine import convert
from core.conversion_registry import CATEGORIES, category_codes
from core.explanations import build_explanation
from core.decimal_utils import parse_decimal

BASE_DIR = Path(__file__).resolve().parent.parent
LOCALES_DIR = BASE_DIR / "locales"


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.current_language = "es"
        self.translations: dict = {}
        self.unit_codes = []
        self.current_category = "length"
        self._build_ui()
        self._load_language("es")

    def _card(self, name: str = "card") -> QFrame:
        card = QFrame()
        card.setObjectName(name)
        return card

    def _build_ui(self) -> None:
        self.setMinimumSize(820, 600)
        self.resize(980, 720)
        self.setStyleSheet(THEME)
        root = QWidget(); self.setCentralWidget(root)
        outer = QVBoxLayout(root); outer.setContentsMargins(28, 20, 28, 18); outer.setSpacing(14)

        header = QHBoxLayout()
        title_box = QVBoxLayout()
        self.title_label = QLabel(); self.title_label.setFont(self.font())
        self.title_label.setStyleSheet("font-size: 25px; font-weight: 700;")
        self.subtitle_label = QLabel(); self.subtitle_label.setObjectName("subtitle")
        title_box.addWidget(self.title_label); title_box.addWidget(self.subtitle_label)
        header.addLayout(title_box); header.addStretch()
        language_box = QVBoxLayout(); self.language_label = QLabel(); self.language_label.setObjectName("eyebrow")
        self.language_combo = QComboBox(); self.language_combo.addItem("Español", "es"); self.language_combo.addItem("Suomi", "fi")
        self.language_combo.currentIndexChanged.connect(self._on_language_changed)
        language_box.addWidget(self.language_label); language_box.addWidget(self.language_combo); header.addLayout(language_box)
        outer.addLayout(header)

        body = QHBoxLayout(); body.setSpacing(18)
        nav = self._card("navCard"); nav.setFixedWidth(166); nav_layout = QVBoxLayout(nav); nav_layout.setContentsMargins(14, 16, 14, 14); nav_layout.setSpacing(6)
        self.nav_title = QLabel(); self.nav_title.setObjectName("navTitle"); self.nav_title.setStyleSheet("font-size: 16px; font-weight: 700;")
        self.nav_conversions = QLabel(); self.nav_conversions.setObjectName("navItem"); self.nav_conversions.setProperty("active", True)
        self.nav_physics = QLabel(); self.nav_physics.setObjectName("navItem"); self.nav_chemistry = QLabel(); self.nav_chemistry.setObjectName("navItem")
        for item in (self.nav_title, self.nav_conversions, self.nav_physics, self.nav_chemistry): nav_layout.addWidget(item)
        nav_layout.addStretch(); body.addWidget(nav)

        content = QVBoxLayout(); content.setSpacing(14); body.addLayout(content, 1)
        controls = self._card(); grid = QGridLayout(controls); grid.setContentsMargins(20, 18, 20, 18); grid.setHorizontalSpacing(12); grid.setVerticalSpacing(10)
        self.category_label = QLabel(); self.category_label.setObjectName("eyebrow"); self.category_combo = QComboBox()
        self.category_combo.currentIndexChanged.connect(self._on_category_changed)
        grid.addWidget(self.category_label, 0, 0); grid.addWidget(self.category_combo, 0, 1, 1, 3)
        self.value_label = QLabel(); self.value_label.setObjectName("eyebrow"); self.value_input = QLineEdit(); self.value_input.returnPressed.connect(self.calculate)
        grid.addWidget(self.value_label, 1, 0); grid.addWidget(self.value_input, 1, 1, 1, 3)
        self.from_label = QLabel(); self.to_label = QLabel(); self.from_label.setObjectName("eyebrow"); self.to_label.setObjectName("eyebrow"); self.from_combo = QComboBox(); self.to_combo = QComboBox()
        self.swap_button = QPushButton("⇄"); self.swap_button.setObjectName("iconButton")
        grid.addWidget(self.from_label, 2, 0); grid.addWidget(self.to_label, 2, 2)
        grid.addWidget(self.from_combo, 3, 0, 1, 2); grid.addWidget(self.swap_button, 3, 2); grid.addWidget(self.to_combo, 3, 3)
        actions = QHBoxLayout(); self.clear_button = QPushButton(); self.calculate_button = QPushButton(); self.calculate_button.setObjectName("primaryButton")
        actions.setContentsMargins(0, 8, 0, 0); actions.addStretch(); actions.addWidget(self.clear_button); actions.addWidget(self.calculate_button); grid.addLayout(actions, 4, 0, 1, 4)
        grid.setColumnStretch(0, 1); grid.setColumnStretch(1, 1); grid.setColumnStretch(3, 1)
        self.swap_button.clicked.connect(self.swap_units); self.calculate_button.clicked.connect(self.calculate); self.clear_button.clicked.connect(self.clear)
        content.addWidget(controls)

        result = self._card(); rl = QVBoxLayout(result); rl.setContentsMargins(20, 16, 20, 16); rh = QHBoxLayout()
        self.result_heading = QLabel(); self.result_heading.setObjectName("eyebrow"); self.copy_button = QPushButton(); self.copy_button.setEnabled(False); self.copy_button.clicked.connect(self.copy_result)
        rh.addWidget(self.result_heading); rh.addStretch(); rh.addWidget(self.copy_button); rl.addLayout(rh)
        self.result_value = QLabel(); self.result_value.setObjectName("resultValue"); self.result_value.setTextInteractionFlags(Qt.TextSelectableByMouse); rl.addWidget(self.result_value)
        content.addWidget(result)

        explanation = self._card(); el = QVBoxLayout(explanation); el.setContentsMargins(20, 16, 20, 16); el.setSpacing(8)
        self.formula_heading = QLabel(); self.formula_heading.setObjectName("sectionTitle"); self.formula_value = QLabel("—"); self.formula_value.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.calculation_heading = QLabel(); self.calculation_value = QLabel("—"); self.note_heading = QLabel(); self.note_heading.setObjectName("sectionTitle"); self.note_value = QLabel(); self.note_value.setObjectName("note"); self.note_value.setWordWrap(True)
        for widget in (self.formula_heading, self.formula_value, self.calculation_heading, self.calculation_value, self.note_heading, self.note_value): el.addWidget(widget)
        content.addWidget(explanation); outer.addLayout(body); self.statusBar()

    def _load_language(self, language: str) -> None:
        with (LOCALES_DIR / f"{language}.json").open(encoding="utf-8") as file: self.translations = json.load(file)
        self.current_language = language; self._apply_translations()

    def _apply_translations(self) -> None:
        t = self.translations; self.setWindowTitle(t["app_title"]); self.title_label.setText(t["app_title"]); self.subtitle_label.setText(t["subtitle"]); self.language_label.setText(t["language"])
        self.nav_title.setText(t["navigation"]); self.nav_conversions.setText(t["conversions"]); self.nav_physics.setText(t["physics"]); self.nav_chemistry.setText(t["chemistry"])
        self.category_label.setText(t["category"]); self.value_label.setText(t["value"]); self.value_input.setPlaceholderText(t["enter_value"]); self.from_label.setText(t["from_unit"]); self.to_label.setText(t["to_unit"])
        self.calculate_button.setText(t["calculate"]); self.clear_button.setText(t["clear"]); self.copy_button.setText(t["copy"]); self.copy_button.setToolTip(t["copy"]); self.swap_button.setToolTip(t["swap_tooltip"])
        self.result_heading.setText(t["result"]); self.formula_heading.setText(t["relationship"]); self.calculation_heading.setText(t["calculation"]); self.note_heading.setText(t["learning_note"])
        selected_category = self.current_category
        self.category_combo.blockSignals(True); self.category_combo.clear()
        for code in category_codes(): self.category_combo.addItem(t["categories"][code], code)
        self.category_combo.setCurrentIndex(self.category_combo.findData(selected_category)); self.category_combo.blockSignals(False)
        self.unit_codes = list(CATEGORIES[selected_category].unit_codes)
        defaults = CATEGORIES[selected_category].defaults
        selected_from = self.from_combo.currentData() if self.from_combo.currentData() in self.unit_codes else defaults[0]
        selected_to = self.to_combo.currentData() if self.to_combo.currentData() in self.unit_codes else defaults[1]
        self._populate(self.from_combo, selected_from); self._populate(self.to_combo, selected_to)
        if not self.result_value.text(): self.result_value.setText(t["result_empty"]); self.note_value.setText(t["empty_state"])
        elif self.value_input.text().strip() and self.copy_button.isEnabled(): self.calculate()
        self.statusBar().showMessage(t["ready"])

    def _populate(self, combo: QComboBox, selected: str) -> None:
        combo.blockSignals(True); combo.clear()
        for code in self.unit_codes: combo.addItem(self.translations["units"][code], code)
        index = combo.findData(selected); combo.setCurrentIndex(index if index >= 0 else 0); combo.blockSignals(False)

    def _on_language_changed(self) -> None:
        code = self.language_combo.currentData()
        if code: self._load_language(code)

    def _on_category_changed(self) -> None:
        self.current_category = self.category_combo.currentData() or "length"
        self.unit_codes = list(CATEGORIES[self.current_category].unit_codes)
        source, target = CATEGORIES[self.current_category].defaults
        self._populate(self.from_combo, source); self._populate(self.to_combo, target); self.clear()

    def calculate(self) -> None:
        try:
            value = parse_decimal(self.value_input.text()); source = self.from_combo.currentData(); target = self.to_combo.currentData()
            result = convert(value, self.current_category, source, target)
            self.result_value.setText(f"{result.formatted_value} {target}"); self.copy_button.setEnabled(True); self.formula_value.setText(result.formula); self.calculation_value.setText(result.steps[0])
            _, _, note = build_explanation(value, self.current_category, source, target, result.value, self.current_language); self.note_value.setText(note); self.statusBar().showMessage(self.translations["result"])
        except ValueError as exc:
            QMessageBox.warning(self, self.translations["app_title"], self.translations.get(str(exc), self.translations["unexpected_error"]))

    def swap_units(self) -> None:
        source, target = self.from_combo.currentData(), self.to_combo.currentData(); self._populate(self.from_combo, target); self._populate(self.to_combo, source)
        if self.value_input.text().strip(): self.calculate()

    def copy_result(self) -> None:
        if self.copy_button.isEnabled():
            QApplication.clipboard().setText(self.result_value.text()); self.statusBar().showMessage(self.translations["copied"])

    def clear(self) -> None:
        self.value_input.clear(); self.result_value.setText(self.translations["result_empty"]); self.copy_button.setEnabled(False); self.formula_value.setText("—"); self.calculation_value.setText("—"); self.note_value.setText(self.translations["empty_state"]); self.statusBar().showMessage(self.translations["ready"]); self.value_input.setFocus()
