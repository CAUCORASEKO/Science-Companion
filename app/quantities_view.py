from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from core.quantities import QUANTITIES


class QuantitiesView(QWidget):
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
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scroll_content = QWidget()
        self.content_layout = QVBoxLayout(self.scroll_content)
        self.content_layout.setContentsMargins(0, 4, 8, 8)
        self.content_layout.setSpacing(14)

        scroll.setWidget(self.scroll_content)
        root.addWidget(scroll, 1)

    def set_translations(self, translations: dict) -> None:
        self.translations = translations
        self.title.setText(translations["quantities_title"])
        self.intro.setText(translations["quantities_intro"])
        self._rebuild()

    def _clear_layout(self) -> None:
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

    def _rebuild(self) -> None:
        self._clear_layout()

        self.content_layout.addWidget(
            self._build_section(
                "basic",
                self.translations["basic_quantities"],
            )
        )

        self.content_layout.addWidget(
            self._build_section(
                "derived",
                self.translations["derived_quantities"],
            )
        )

        self.content_layout.addStretch()

    def _build_section(self, category: str, title: str) -> QFrame:
        card = QFrame()
        card.setObjectName("card")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 16, 18, 18)
        layout.setSpacing(10)

        heading = QLabel(title)
        heading.setObjectName("sectionHeading")
        layout.addWidget(heading)

        header = QFrame()
        header.setObjectName("quantityHeader")

        header_grid = QGridLayout(header)
        header_grid.setContentsMargins(12, 8, 12, 8)
        header_grid.setHorizontalSpacing(10)

        headers = (
            self.translations["quantity"],
            self.translations["quantity_symbol"],
            self.translations["si_unit"],
            self.translations["unit_symbol"],
            self.translations["equivalence"],
        )

        for column, text in enumerate(headers):
            label = QLabel(text)
            label.setObjectName("tableHeader")
            header_grid.addWidget(label, 0, column)

        header_grid.setColumnStretch(0, 3)
        header_grid.setColumnStretch(1, 1)
        header_grid.setColumnStretch(2, 3)
        header_grid.setColumnStretch(3, 1)
        header_grid.setColumnStretch(4, 4)

        layout.addWidget(header)

        items = [
            quantity
            for quantity in QUANTITIES
            if quantity.category == category
        ]

        for quantity in items:
            row = QFrame()
            row.setObjectName("quantityRow")

            grid = QGridLayout(row)
            grid.setContentsMargins(12, 10, 12, 10)
            grid.setHorizontalSpacing(10)

            name = QLabel(
                self.translations["quantities"][quantity.key]
            )
            name.setObjectName("quantityName")

            symbol = QLabel(quantity.symbol)
            symbol.setObjectName("scienceSymbol")

            si_unit = QLabel(
                self.translations["si_units"][quantity.key]
            )

            unit_symbol = QLabel(quantity.unit_symbol)
            unit_symbol.setObjectName("scienceSymbol")

            equivalence = QLabel(
                quantity.si_equivalence
                or self.translations["base_si_unit"]
            )
            equivalence.setObjectName("muted")
            equivalence.setWordWrap(True)

            grid.addWidget(name, 0, 0)
            grid.addWidget(symbol, 0, 1)
            grid.addWidget(si_unit, 0, 2)
            grid.addWidget(unit_symbol, 0, 3)
            grid.addWidget(equivalence, 0, 4)

            grid.setColumnStretch(0, 3)
            grid.setColumnStretch(1, 1)
            grid.setColumnStretch(2, 3)
            grid.setColumnStretch(3, 1)
            grid.setColumnStretch(4, 4)

            layout.addWidget(row)

        return card
