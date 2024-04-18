from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QPushButton, QLineEdit, QMessageBox

class ClassInfoDialog(QDialog):
    def __init__(self, layer, parent=None):
        super(ClassInfoDialog, self).__init__(parent)
        self.setWindowTitle("Informações de Classe")
        self.layer = layer

        layout = QVBoxLayout()

        label = QLabel("Classes na camada:")
        layout.addWidget(label)

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        self.populate_class_list()

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

        self.setLayout(layout)

    def populate_class_list(self):
        classes = set()
        for feature in self.layer.getFeatures():
            classes.add(feature['classe_isr'])

        for class_name in sorted(classes):
            item = QListWidgetItem(class_name)
            self.list_widget.addItem(item)

    def exec_(self):
        result = super(ClassInfoDialog, self).exec_()
        if result:
            QMessageBox.information(self, "Ação", "Você clicou em OK")

# Uso:
layer = QgsProject.instance().mapLayersByName('camada_ottobacias_montante')[0]
dialog = ClassInfoDialog(layer)
dialog.exec_()
