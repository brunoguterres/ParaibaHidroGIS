import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QWidget
from PyQt5.QtGui import QColor, QPainter, QFont, QPalette
from PyQt5.QtCore import Qt

class CustomColorBox(QWidget):
    def __init__(self, color, text, parent=None):
        super().__init__(parent)
        self.color = QColor(*color)
        self.text = text

        # Define a cor de fundo da caixa
        palette = self.palette()
        palette.setColor(QPalette.Background, self.color)
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        # Define o texto da caixa
        self.label = QLabel(self.text, self)
        self.label.setAlignment(Qt.AlignCenter)

        # Define o layout da caixa
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        # Define o tamanho mínimo da caixa
        self.setMinimumSize(200, 30)

class ColorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Caixa de Diálogo de Cores")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        color_texts = [
            (QColor(80, 150, 162), "Sem criticidade"),
            (QColor(105, 217, 114), "Baixo potencial de comprometimento"),
            (QColor(255, 255, 116), "Médio potencial de comprometimento"),
            (QColor(253, 144, 64), "Alto potencial de comprometimento"),
            (QColor(215, 61, 125), "Déficit de atendimento às demandas")
        ]

        for color, text in color_texts:
            box = CustomColorBox(color.getRgb(), text)
            layout.addWidget(box)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = ColorDialog()
    dialog.exec_()
    sys.exit(app.exec_())
