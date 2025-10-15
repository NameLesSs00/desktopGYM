from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QCompleter

class CustomWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.combo = QComboBox()
        self.combo.setEditable(True)
        layout.addWidget(self.combo)

# For backward compatibility with existing UI files
test = CustomWidget
