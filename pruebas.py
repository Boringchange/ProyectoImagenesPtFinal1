from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QVBoxLayout, QLabel
import sys

class VentanaEmergente(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana Emergente")
        self.setFixedSize(200, 100)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("¡Hola desde la ventana emergente!"))
        self.setLayout(layout)

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana Principal")
        self.setFixedSize(300, 200)

        boton = QPushButton("Abrir Emergente", self)
        boton.clicked.connect(self.mostrar_emergente)
        boton.resize(200, 40)
        boton.move(50, 80)

    def mostrar_emergente(self):
        dialogo = VentanaEmergente()
        dialogo.exec()  # Bloquea hasta que se cierra la ventana emergente

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())
