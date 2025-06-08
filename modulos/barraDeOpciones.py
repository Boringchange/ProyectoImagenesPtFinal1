from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QIcon, QAction, QPalette, QFont
from PyQt6.QtWidgets import QLabel, QToolButton, QListWidget, QPushButton, QFrame, QVBoxLayout, QScrollArea, QScrollBar, \
    QWidget, QHBoxLayout
import json

from scripts.ProcesamientoImagenes import mostrar_imagenes_rgb, conversion_grises


class DesplegableBotones(QFrame):
    def __init__(self, nombres, funcionLlamar, parent=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.WindowType.Popup)
        layout = QVBoxLayout(self)

        self.botones = []

        for nombre in nombres:
            boton = QPushButton(nombre)
            boton.setObjectName("btn_desplegable")
            boton.clicked.connect(lambda _, n=nombre: self.opcion_seleccionada(n, funcionLlamar))
            layout.addWidget(boton)
            self.botones.append(boton)

    def opcion_seleccionada(self, nombre, funcionLlamar):
        self.hide()
        funcionLlamar(nombre)

class BarraHerramientas:
    def __init__(self, ventana):

        self.ventana = ventana

        #Abrimos el CSS de esta clase.
        botones_categorias = []

        #Creamos y agregamos la barra de herramientas a la app principal
        self.barra_herramientas = ventana.addToolBar("Herramientas")
        self.barra_herramientas.setAllowedAreas(Qt.ToolBarArea.TopToolBarArea | Qt.ToolBarArea.BottomToolBarArea)
        self.barra_herramientas.setDisabled(True)
        #Inicalizamos las imagenes para las opciones

        flecha_izquierda = QIcon("img/flecha_izquierda.png")
        flecha_derecha = QIcon("img/flecha_derecha.png")
        recargar = QIcon("img/recargar.png")

        #Inicializamos los botones para las herramientas

        self.flecha_izquierda_icono = QToolButton()
        self.flecha_izquierda_icono.setIcon(flecha_izquierda)
        self.flecha_izquierda_icono.setText("Deshacer")
        self.flecha_izquierda_icono.setDisabled(True)
        self.flecha_izquierda_icono.setToolTip(self.flecha_izquierda_icono.text())
        self.flecha_izquierda_icono.setObjectName("btn_barra_opciones_iconos")

        self.flecha_derecha_icono = QToolButton()
        self.flecha_derecha_icono.setIcon(flecha_derecha)
        self.flecha_derecha_icono.setText("Rehacer")
        self.flecha_derecha_icono.setDisabled(True)
        self.flecha_derecha_icono.setToolTip(self.flecha_derecha_icono.text())
        self.flecha_derecha_icono.setObjectName("btn_barra_opciones_iconos")

        self.recargar_icon = QToolButton()
        self.recargar_icon.setIcon(recargar)
        self.recargar_icon.setText("Recargar")
        self.recargar_icon.setDisabled(True)
        self.recargar_icon.setToolTip(self.recargar_icon.text())
        self.recargar_icon.setObjectName("btn_barra_opciones_iconos")

        #Agregamos los botones a la barra

        self.barra_herramientas.addWidget(self.flecha_izquierda_icono)
        self.barra_herramientas.addWidget(self.flecha_derecha_icono)
        self.barra_herramientas.addWidget(self.recargar_icon)

        #Crear el contenedor del widget
        contenedorFiltroBotones = QWidget()
        contenedorFiltroBotones.setObjectName("btn_contenedor")

        contenedorFiltroBotonesLayout = QHBoxLayout()
        contenedorFiltroBotonesLayout.setObjectName("btn_layout")

        contenedorFiltroBotones.setLayout(contenedorFiltroBotonesLayout)

        #Agregamos un scroll vertical para que podamos ver todos los botones

        scrollFiltrosBotones = QScrollArea()
        scrollFiltrosBotones.horizontalScrollBar().setObjectName("btn_scroll_horizontal")
        scrollFiltrosBotones.setObjectName("btn_scroll_area")
        scrollFiltrosBotones.setWidgetResizable(True)


        #Abrimos el archivo que contendra la información de todas la categorias de filtros y sus filtros

        with open("JSON/filtros.json", "r", encoding="utf-8") as archivo:
            categorias = json.load(archivo)

        #Inicializamos los botones de las categorias y les agregamos la funcion de mostrar lista de filtros

        for categoria in categorias:

            categoria_boton = QPushButton(categoria["nombre"])
            categoria_boton.setObjectName("btn_barra_opciones_texto")
            botones_categorias.append(categoria_boton)
            categoria_boton.clicked.connect(lambda _, n = categoria_boton, f = categoria: self.mostrar_lista_filtros(n, f, ventana))

            contenedorFiltroBotonesLayout.addWidget(categoria_boton)

        scrollFiltrosBotones.setWidget(contenedorFiltroBotones)

        self.barra_herramientas.addWidget(scrollFiltrosBotones)

    def mostrar_lista_filtros(self, botonPresionado, categoria, ventana):
        # Mostrar debajo del botón
        boton_pos = botonPresionado.mapToGlobal(QPoint(0, botonPresionado.height()))

        self.panel_desplegable = DesplegableBotones(categoria["filtros"], self.operaciones, ventana)
        self.panel_desplegable.move(boton_pos)
        self.panel_desplegable.show()


    def operaciones(self, nombre):
        if nombre == "RGB":
            mostrar_imagenes_rgb(self.ventana.objeto_actual)
        elif nombre == "Conversión grises":
            imagen = conversion_grises(self.ventana.objeto_actual)
            self.ventana.objeto_actual.realizar_cambio(imagen)
            self.ventana.barra_ventanas.mostrar_imagen(self.ventana.objeto_actual)