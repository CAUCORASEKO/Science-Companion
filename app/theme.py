THEME = """
QMainWindow, QWidget {
    background: #f6f7fb;
    color: #172033;
}

QLabel {
    background: transparent;
}

QLabel#subtitle,
QLabel#muted {
    color: #667085;
}

QLabel#eyebrow {
    color: #667085;
    font-size: 11px;
    font-weight: 700;
}

QLabel#pageTitle {
    color: #172033;
    font-size: 22px;
    font-weight: 700;
}

QLabel#sectionHeading {
    color: #243b80;
    font-size: 16px;
    font-weight: 700;
}

QFrame#card {
    background: #ffffff;
    border: 1px solid #e2e6ef;
    border-radius: 14px;
}

QFrame#navCard {
    background: #202b45;
    border-radius: 14px;
}

QLabel#navTitle {
    color: #f5f7ff;
    font-size: 15px;
    font-weight: 700;
    padding: 4px 8px 8px 8px;
}

QPushButton#navButton {
    background: transparent;
    color: #aeb9d2;
    border: none;
    border-radius: 8px;
    padding: 9px 10px;
    text-align: left;
    font-weight: 600;
}

QPushButton#navButton:hover {
    background: #2b3857;
    color: #ffffff;
}

QPushButton#navButton[active="true"] {
    background: #344365;
    color: #ffffff;
    font-weight: 700;
}

QPushButton#navButton:disabled {
    background: transparent;
    color: #697793;
}

QLabel#sectionTitle {
    color: #344054;
    font-size: 13px;
    font-weight: 700;
}

QLineEdit,
QComboBox {
    background: #ffffff;
    border: 1px solid #cfd6e4;
    border-radius: 8px;
    padding: 9px 10px;
    min-height: 20px;
}

QLineEdit:focus,
QComboBox:focus {
    border: 2px solid #4c6fff;
}

QComboBox QAbstractItemView {
    background: #ffffff;
    color: #172033;
    selection-background-color: #e8edff;
    selection-color: #172033;
}

QPushButton {
    background: #ffffff;
    border: 1px solid #cfd6e4;
    border-radius: 8px;
    padding: 9px 16px;
    font-weight: 600;
}

QPushButton:hover {
    background: #eef2f8;
}

QPushButton#primaryButton {
    background: #4c6fff;
    color: white;
    border: none;
}

QPushButton#primaryButton:hover {
    background: #3d5bd6;
}

QPushButton#iconButton {
    font-size: 18px;
    padding: 2px;
    min-width: 32px;
    max-width: 32px;
    min-height: 32px;
    max-height: 32px;
}

QLabel#resultValue {
    color: #243b80;
    font-size: 28px;
    font-weight: 700;
}

QLabel#note {
    background: #f0f4ff;
    color: #344054;
    border-radius: 8px;
    padding: 10px;
}

QFrame#quantityHeader {
    background: #f3f5f9;
    border-radius: 8px;
}

QFrame#quantityRow {
    background: #fbfcfe;
    border: 1px solid #edf0f5;
    border-radius: 9px;
}

QFrame#quantityRow:hover {
    background: #f5f7ff;
    border: 1px solid #dce4ff;
}

QLabel#tableHeader {
    color: #667085;
    font-size: 11px;
    font-weight: 700;
}

QLabel#quantityName {
    color: #172033;
    font-weight: 650;
}

QLabel#scienceSymbol {
    color: #243b80;
    font-size: 15px;
    font-weight: 700;
}

QScrollArea {
    background: transparent;
    border: none;
}

QScrollArea > QWidget > QWidget {
    background: transparent;
}


QFrame#formulaRow {
    background: #fbfcfe;
    border: 1px solid #edf0f5;
    border-radius: 9px;
}

QFrame#formulaRow:hover {
    background: #f5f7ff;
    border: 1px solid #dce4ff;
}

QLabel#formulaName {
    color: #344054;
    font-size: 13px;
    font-weight: 700;
}

QLabel#formulaExpression {
    color: #243b80;
    font-size: 18px;
    font-weight: 700;
}

QLabel#formulaDetails {
    color: #667085;
    font-size: 12px;
}

QStatusBar {
    color: #667085;
}
"""
