from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from core.formulas import FORMULAS


CATEGORY_ORDER = (
    "motion",
    "forces",
    "energy",
    "matter",
    "electricity",
    "waves",
)


class FormulasView(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.translations: dict = {}

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(12)

        self.title = QLabel()
        self.title.setObjectName("pageTitle")

        self.intro = QLabel()
        self.intro.setObjectName("muted")
        self.intro.setWordWrap(True)

        root.addWidget(self.title)
        root.addWidget(self.intro)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.scroll_content = QWidget()

        self.content_layout = QVBoxLayout(
            self.scroll_content
        )
        self.content_layout.setContentsMargins(
            0, 4, 8, 8
        )
        self.content_layout.setSpacing(14)

        scroll.setWidget(self.scroll_content)
        root.addWidget(scroll, 1)

    def set_translations(self, translations: dict) -> None:
        self.translations = translations

        self.title.setText(
            translations["formulas_title"]
        )

        self.intro.setText(
            translations["formulas_intro"]
        )

        self._rebuild()

    def _clear(self) -> None:
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

    def _rebuild(self) -> None:
        self._clear()

        for category in CATEGORY_ORDER:
            formulas = [
                formula
                for formula in FORMULAS
                if formula.category == category
            ]

            if formulas:
                self.content_layout.addWidget(
                    self._build_category(
                        category,
                        formulas,
                    )
                )

        reference = self.translations.get("wave_reference")
        if reference:
            card = QFrame()
            card.setObjectName("card")
            layout = QVBoxLayout(card)
            layout.setContentsMargins(18, 16, 18, 18)
            heading = QLabel(reference["title"])
            heading.setObjectName("sectionHeading")
            layout.addWidget(heading)
            layout.setSpacing(10)
            for section in reference["sections"]:
                section_card = QFrame()
                section_card.setObjectName("referenceSection")
                section_layout = QVBoxLayout(section_card)
                section_layout.setContentsMargins(12, 10, 12, 10)
                section_layout.setSpacing(4)
                section_heading = QLabel(section["title"])
                section_heading.setObjectName("referenceHeading")
                body = QLabel(section["text"])
                body.setWordWrap(True)
                body.setObjectName("formulaDetails")
                section_layout.addWidget(section_heading)
                section_layout.addWidget(body)
                layout.addWidget(section_card)
            self.content_layout.addWidget(card)

        self.content_layout.addStretch()

    def _build_category(
        self,
        category: str,
        formulas,
    ) -> QFrame:
        card = QFrame()
        card.setObjectName("card")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 16, 18, 18)
        layout.setSpacing(10)

        heading = QLabel(
            self.translations["formula_categories"].get(
                category,
                self.translations.get("formula_categories_extra", {}).get(category, category),
            )
        )
        heading.setObjectName("sectionHeading")

        layout.addWidget(heading)

        for formula in formulas:
            layout.addWidget(
                self._build_formula_row(formula)
            )

        return card

    def _build_formula_row(self, formula) -> QFrame:
        row = QFrame()
        row.setObjectName("formulaRow")

        layout = QVBoxLayout(row)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(8)

        top = QGridLayout()
        top.setHorizontalSpacing(14)

        name = QLabel(
            self.translations["formula_names"].get(
                formula.key,
                self.translations.get("formula_names_extra", {}).get(formula.key, formula.key),
            )
        )
        name.setObjectName("formulaName")

        expression = QLabel(formula.expression)
        expression.setObjectName("formulaExpression")
        expression.setTextInteractionFlags(
            Qt.TextSelectableByMouse
        )

        top.addWidget(name, 0, 0)
        top.addWidget(expression, 0, 1)

        top.setColumnStretch(0, 2)
        top.setColumnStretch(1, 3)

        layout.addLayout(top)

        variables = []

        for symbol, key, unit in formula.variables:
            translated_name = self.translations[
                "formula_variables"
            ].get(key, key)

            variables.append(
                f"{symbol} = {translated_name} — {unit}"
            )

        details = QLabel("\n".join(variables))
        details.setObjectName("formulaDetails")
        details.setTextInteractionFlags(
            Qt.TextSelectableByMouse
        )

        layout.addWidget(details)

        return row
