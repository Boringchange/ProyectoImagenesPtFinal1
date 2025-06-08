from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QDockWidget, QTextEdit, QTabWidget
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
import sys

# Ventana secundaria que se abre desde el botón
class VentanaSecundaria(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana secundaria")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()
        etiqueta = QLabel("¡Hola! Soy otra ventana.")
        cerrar = QPushButton("Cerrar")
        cerrar.clicked.connect(self.close)

        layout.addWidget(etiqueta)
        layout.addWidget(cerrar)
        self.setLayout(layout)

# Barra de menú
class BarraMenu:
    def __init__(self, ventana):
        menubar = ventana.menuBar()
        archivo_menu = menubar.addMenu("Archivo")
        salir_accion = QAction("Salir", ventana)
        salir_accion.triggered.connect(ventana.close)
        archivo_menu.addAction(salir_accion)
        self.salir_accion = salir_accion

# Barra de herramientas
class BarraHerramientas:
    def __init__(self, ventana, accion_salir):
        toolbar = ventana.addToolBar("Principal")
        toolbar.addAction(accion_salir)

# Panel con el botón que abre la ventana secundaria
class PanelCentral(QWidget):
    def __init__(self, ventana_principal):
        super().__init__()
        self.ventana_principal = ventana_principal
        self.ventana_secundaria = None  # Mantener referencia

        layout = QVBoxLayout()

        label = QLabel("Contenido de la pestaña con botón")
        label.setObjectName("miLabel")

        boton = QPushButton("Abrir ventana secundaria")
        boton.setObjectName("miBoton")
        boton.clicked.connect(self.abrir_ventana)

        layout.addWidget(label)
        layout.addWidget(boton)
        self.setLayout(layout)

    def abrir_ventana(self):
        if self.ventana_secundaria is None or not self.ventana_secundaria.isVisible():
            self.ventana_secundaria = VentanaSecundaria()
            self.ventana_secundaria.show()

# Panel lateral (dock)
class PanelDock(QDockWidget):
    def __init__(self, ventana):
        super().__init__("Panel lateral", ventana)
        self.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea | Qt.DockWidgetArea.TopDockWidgetArea)
        texto_dock = QTextEdit()
        texto_dock.setPlainText("Contenido del dock widget")
        self.setWidget(texto_dock)

# Widget central con pestañas
class PanelConPestañas(QWidget):
    def __init__(self, ventana_principal):
        super().__init__()
        layout = QVBoxLayout()
        tabs = QTabWidget()

        # Pestaña 1: incluye el PanelCentral con el botón
        pestaña1 = PanelCentral(ventana_principal)
        pestaña2 = QWidget()

        layout2 = QVBoxLayout()
        layout2.addWidget(QLabel("Contenido de la pestaña 2"))
        pestaña2.setLayout(layout2)

        tabs.addTab(pestaña1, "Principal")
        tabs.addTab(pestaña2, "Opciones")

        layout.addWidget(tabs)
        self.setLayout(layout)

# Ventana principal
class MiVentana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplicación PyQt6 con pestañas y ventanas")

        self.panel_central = PanelConPestañas(self)
        self.setCentralWidget(self.panel_central)

        self.barra_menu = BarraMenu(self)
        self.barra_herramientas = BarraHerramientas(self, self.barra_menu.salir_accion)
        self.statusBar().showMessage("Listo")

        self.dock = PanelDock(self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock)

        # Cargar CSS externo
        try:
            with open("img/estilos.css", "r") as f:
                estilo = f.read()
                self.setStyleSheet(estilo)
        except FileNotFoundError:
            print("⚠️ Archivo estilos.css no encontrado.")

# Main
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MiVentana()
    ventana.resize(700, 500)
    ventana.show()
    sys.exit(app.exec())
