from PyQt6.QtWidgets import QApplication, QWidget, QMenu, QLabel
from PyQt6.QtCore import Qt
import sys

class MyWidget(QLabel):
    def __init__(self):
        super().__init__("Haz clic derecho aquí")
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, pos):
        menu = QMenu(self)
        accion = menu.addAction("Saludar")
        accion.triggered.connect(lambda: print("Hola desde el menú!"))
        menu.exec(self.mapToGlobal(pos))

app = QApplication(sys.argv)
widget = MyWidget()
widget.resize(300, 200)
widget.show()
sys.exit(app.exec())