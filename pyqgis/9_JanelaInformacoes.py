from qgis.PyQt.QtWidgets import QDialog, QVBoxLayout, QLabel, QListWidget, QListWidgetItem
from qgis.PyQt.QtGui import QPixmap
from qgis.core import QgsProject, QgsSymbol

class ClassInfoDialog(QDialog):
    def __init__(self, layer, parent=None):
        super(ClassInfoDialog, self).__init__(parent)
        self.setWindowTitle("Informações de Classe")
        self.layer = layer

        layout = QVBoxLayout()

        label = QLabel("Classes na camada:")
        layout.addWidget(label)

        list_widget = QListWidget()
        layout.addWidget(list_widget)

        # Obtenha as classes únicas da camada
        classes = set()
        for feature in layer.getFeatures():
            classes.add(feature['classe_isr'])

        # Crie itens na lista para cada classe
        for class_name in sorted(classes):
            item = QListWidgetItem(class_name)
            list_widget.addItem(item)

            # Obtenha o símbolo correspondente à classe e adicione à lista
            symbol = layer.renderer().symbolForFeature(feature)
            pixmap = QPixmap(symbol.previewImage(24, 24))
            label = QLabel()
            label.setPixmap(pixmap)
            list_widget.setItemWidget(item, label)

        self.setLayout(layout)

# Uso:
layer = QgsProject.instance().mapLayersByName('camada_ottobacias_montante')[0]
dialog = ClassInfoDialog(layer)
dialog.exec_()
