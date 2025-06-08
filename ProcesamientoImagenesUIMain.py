import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QLabel, QScrollArea
from modulos.barraDeOpciones import BarraHerramientas
from modulos.barraDeVentanas import BarraVentanas
from scripts.Imagen import Imagen

class ProcesamientoImagenesApp(QMainWindow):

    imagenes_agregadas = []
    label_imagen = None
    objeto_actual = None

    def __init__(self):
        super().__init__()

        self.widget_central = QWidget()
        self.widget_central_layout = QHBoxLayout(self.widget_central)

        self.setWindowTitle("Procesamiento de imagenes")

        self.label_imagen = QLabel()
        self.label_imagen.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.barra_herramientas = BarraHerramientas(self)
        self.barra_ventanas = BarraVentanas(self)

        self.widget_imagen_scroll = QScrollArea()
        self.widget_imagen_scroll.setWidget(self.label_imagen)
        self.widget_imagen_scroll.setWidgetResizable(True)


        self.widget_central_layout.addWidget(self.barra_ventanas)
        self.widget_central_layout.addWidget(self.widget_imagen_scroll)

        self.setCentralWidget(self.widget_central)

        self.statusBar().showMessage("XD")

def cargar_estilos(*archivos_css):
    estilos_combinados = ""
    for archivo in archivos_css:
        with open("css/"+archivo+".css", "r") as f:
            estilos_combinados += f.read() + "\n"
    return estilos_combinados

if __name__ == "__main__":
    app = QApplication(sys.argv)

    #Cargamos los estilos de cada clase y los compilamos
    estilos = cargar_estilos("barraDeOpciones", "barraDeVentanas", "ProcesamientoImagenesUIMain")

    #Añadimos el estilo compilado y lo añadimos a la app

    app.setStyleSheet(estilos)
    ventana = ProcesamientoImagenesApp()
    ventana.resize(600, 400)
    ventana.show()
    sys.exit(app.exec())