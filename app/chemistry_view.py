from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox, QFrame, QLabel, QLineEdit, QScrollArea, QVBoxLayout, QWidget

from core.chemistry import ELEMENTS, Element, find_element


class ChemistryView(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.translations: dict = {}
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(12)
        self.title = QLabel(); self.title.setObjectName("pageTitle")
        self.intro = QLabel(); self.intro.setObjectName("muted"); self.intro.setWordWrap(True)
        root.addWidget(self.title); root.addWidget(self.intro)
        scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.content = QWidget(); self.layout = QVBoxLayout(self.content); self.layout.setContentsMargins(0, 4, 8, 8); self.layout.setSpacing(12)
        scroll.setWidget(self.content); root.addWidget(scroll, 1)

    def set_translations(self, translations: dict) -> None:
        self.translations = translations
        data = translations["chemistry"]
        self.title.setText(data["title"]); self.intro.setText(data["intro"])
        self._rebuild()

    def _card(self, title: str, text: str) -> QFrame:
        card = QFrame(); card.setObjectName("card")
        layout = QVBoxLayout(card); layout.setContentsMargins(18, 14, 18, 16); layout.setSpacing(7)
        heading = QLabel(title); heading.setObjectName("sectionHeading")
        body = QLabel(text); body.setWordWrap(True); body.setObjectName("formulaDetails")
        layout.addWidget(heading); layout.addWidget(body)
        return card

    def _rebuild(self) -> None:
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        data = self.translations["chemistry"]
        self.layout.addWidget(self._card(data["topic_title"], data["topic_text"]))
        self.layout.addWidget(self._card(data["mixtures_title"], data["mixtures_text"]))
        self._build_explorer(data)
        self.layout.addWidget(self._card(data["periodic_title"], data["periodic_text"]))
        self.layout.addWidget(self._card(data["families_title"], data["families_text"]))
        self.layout.addWidget(self._card(data["classification_title"], data["classification_text"]))
        self.layout.addStretch()

    def _build_explorer(self, data: dict) -> None:
        card = QFrame(); card.setObjectName("card")
        layout = QVBoxLayout(card); layout.setContentsMargins(18, 14, 18, 16); layout.setSpacing(8)
        heading = QLabel(data["explorer_title"]); heading.setObjectName("sectionHeading")
        hint = QLabel(data["explorer_hint"]); hint.setObjectName("muted"); hint.setWordWrap(True)
        self.element_combo = QComboBox(); self.element_combo.setEditable(True)
        self.element_combo.setInsertPolicy(QComboBox.NoInsert)
        self.element_combo.addItems([f"{e.symbol} — {e.name_es} / {e.name_fi}" for e in ELEMENTS])
        self.element_combo.currentTextChanged.connect(self._show_element)
        self.element_info = QLabel(); self.element_info.setWordWrap(True); self.element_info.setObjectName("formulaDetails")
        layout.addWidget(heading); layout.addWidget(hint); layout.addWidget(self.element_combo); layout.addWidget(self.element_info)
        self.layout.addWidget(card)
        self._show_element(self.element_combo.currentText())

    def _show_element(self, query: str) -> None:
        element = find_element(query.split(" — ", 1)[0]) or find_element(query)
        if not element or not self.translations:
            return
        labels = self.translations["chemistry"]["element_labels"]
        value = lambda key: labels.get(key, "—")
        family = self.translations["chemistry"]["families"].get(element.family or "", "—")
        classification = self.translations["chemistry"]["classifications"].get(element.classification, "—")
        valence = str(element.valence_electrons) if element.valence_electrons is not None else "—"
        ion = element.common_ion or "—"
        self.element_info.setText(
            f"{value('symbol')}: {element.symbol}\n{value('atomic_number')}: {element.atomic_number}\n"
            f"{value('period')}: {element.period}\n{value('group')}: {element.group or '—'}\n"
            f"{value('classification')}: {classification}\n{value('family')}: {family}\n"
            f"{value('valence')}: {valence}\n{value('common_ion')}: {ion}"
        )
