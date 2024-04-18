from qgis.PyQt.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QWidget
from qgis.PyQt.QtGui import QColor, QPainter, QPalette
import sys

class ColorWidget(QWidget):
    def __init__(self, color, parent=None):
        super().__init__(parent)
        self.color = QColor(*color)
        self.setFixedSize(20, 20)  # Define o tamanho fixo do widget de cor

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(event.rect(), self.color)

class CustomColorBox(QWidget):
    def __init__(self, color, text, parent=None):
        super().__init__(parent)
        self.color_widget = ColorWidget(color)
        self.text = text

        # Define o texto da caixa
        self.label = QLabel(self.text, self)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # Alinha o texto à esquerda

        # Define o layout da caixa
        layout = QHBoxLayout()  
        layout.addWidget(self.color_widget)
        layout.addWidget(self.label)
        self.setLayout(layout)

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

def run_color_dialog():
    app = QApplication(sys.argv)
    dialog = ColorDialog()
    dialog.exec_()  # Mostra o diálogo e aguarda até que ele seja fechado
    # O aplicativo continuará sendo executado aqui até que a janela seja fechada
    # Não precisamos mais da chamada sys.exit()

# Chamar a função para executar o diálogo de cores
run_color_dialog()
