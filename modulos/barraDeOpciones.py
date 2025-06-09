import os.path

import cv2
from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QIcon, QAction, QPalette, QFont, QImage, QPixmap
from PyQt6.QtWidgets import QLabel, QToolButton, QListWidget, QPushButton, QFrame, QVBoxLayout, QScrollArea, QScrollBar, \
    QWidget, QHBoxLayout, QDialog, QLineEdit, QComboBox
import json

from scripts.ProcesamientoImagenes import mostrar_imagenes_rgb, conversion_grises, mostrar_histograma, \
    operaciones_aritmeticas_imagen, deteccion_objetos, operacion_not, operaciones_entre_2_imagenes, \
    operaciones_umbralizacion, operacion_umbral_otsu, operacion_ecualizacion_exponencial, operaciones_ruido, \
    operacion_filtro_mediana, operacion_operador_prewitt, operacion_filtro_segmentacion_completa_multiumbralizacion


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
        self.flecha_izquierda_icono.clicked.connect(lambda: self.deshacer_cambio())

        self.flecha_derecha_icono = QToolButton()
        self.flecha_derecha_icono.setIcon(flecha_derecha)
        self.flecha_derecha_icono.setText("Rehacer")
        self.flecha_derecha_icono.setDisabled(True)
        self.flecha_derecha_icono.setToolTip(self.flecha_derecha_icono.text())
        self.flecha_derecha_icono.setObjectName("btn_barra_opciones_iconos")
        self.flecha_derecha_icono.clicked.connect(lambda: self.rehacer_cambio())

        self.recargar_icon = QToolButton()
        self.recargar_icon.setIcon(recargar)
        self.recargar_icon.setText("Recargar")
        self.recargar_icon.setDisabled(True)
        self.recargar_icon.setToolTip(self.recargar_icon.text())
        self.recargar_icon.setObjectName("btn_barra_opciones_iconos")
        self.recargar_icon.clicked.connect(lambda: self.reiniciar_imagen())

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
        elif nombre == "Histograma":
            mostrar_histograma(self.ventana.objeto_actual)
        elif nombre == "Detección de objetos":
            deteccion_objetos(self.ventana.objeto_actual)
        elif nombre == "Suma":
            self.llamar_funciones(operaciones_aritmeticas_imagen, [self.ventana.objeto_actual, 1])
        elif nombre == "Resta":
            self.llamar_funciones(operaciones_aritmeticas_imagen, [self.ventana.objeto_actual, 2])
        elif nombre == "Multiplicación":
            self.llamar_funciones(operaciones_aritmeticas_imagen, [self.ventana.objeto_actual, 3])
        elif nombre == "NOT":
            imagen = operacion_not(self.ventana.objeto_actual)
            self.ventana.objeto_actual.realizar_cambio(imagen)
            self.ventana.barra_ventanas.mostrar_imagen(self.ventana.objeto_actual)
        elif nombre == "Suma 2 imagenes":
            self.llamar_funciones_entre_2_imagenes(operaciones_entre_2_imagenes, 1)
        elif nombre == "Resta 2 imagenes":
            self.llamar_funciones_entre_2_imagenes(operaciones_entre_2_imagenes, 2)
        elif nombre == "Multiplicación 2 imagenes":
            self.llamar_funciones_entre_2_imagenes(operaciones_entre_2_imagenes, 3)
        elif nombre == "OR":
            self.llamar_funciones_entre_2_imagenes(operaciones_entre_2_imagenes, 4)
        elif nombre == "AND":
            self.llamar_funciones_entre_2_imagenes(operaciones_entre_2_imagenes, 5)
        elif nombre == "XOR":
            self.llamar_funciones_entre_2_imagenes(operaciones_entre_2_imagenes, 6)
        elif nombre == "Umbral simple":
            self.llamar_funciones(operaciones_umbralizacion, [self.ventana.objeto_actual, 0])
        elif nombre == "Umbral adaptativo":
            self.llamar_funciones(operaciones_umbralizacion, [self.ventana.objeto_actual, 3])
        elif nombre == "Umbral Otsu":
            imagen = operacion_umbral_otsu(self.ventana.objeto_actual)
            self.ventana.objeto_actual.realizar_cambio(imagen)
            self.ventana.barra_ventanas.mostrar_imagen(self.ventana.objeto_actual)
        elif nombre == "Umbral binario inverso":
            self.llamar_funciones(operaciones_umbralizacion, [self.ventana.objeto_actual, 1])
        elif nombre == "Exponencial":
            self.llamar_funciones(operacion_ecualizacion_exponencial, [self.ventana.objeto_actual])
        elif nombre == "Mediana":
            self.llamar_funciones(operacion_filtro_mediana, [self.ventana.objeto_actual])
        elif nombre == "Operador de Prewitt":
            imagen = operacion_operador_prewitt(self.ventana.objeto_actual)
            self.ventana.objeto_actual.realizar_cambio(imagen)
            self.ventana.barra_ventanas.mostrar_imagen(self.ventana.objeto_actual)
        elif nombre == "Sal y Pimienta":
            imagen = operaciones_ruido(self.ventana.objeto_actual, 1)
            self.ventana.objeto_actual.realizar_cambio(imagen)
            self.ventana.barra_ventanas.mostrar_imagen(self.ventana.objeto_actual)
        elif nombre == "Gaussiano":
            imagen = operaciones_ruido(self.ventana.objeto_actual, 2)
            self.ventana.objeto_actual.realizar_cambio(imagen)
            self.ventana.barra_ventanas.mostrar_imagen(self.ventana.objeto_actual)
        elif nombre == "Segmentación completa mediante Multiumbralización":
            self.llamar_funciones(operacion_filtro_segmentacion_completa_multiumbralizacion, [self.ventana.objeto_actual])

    def deshacer_cambio(self):
        self.ventana.objeto_actual.imagen_actual = self.ventana.objeto_actual.imagen_actual - 1
        self.ventana.barra_ventanas.mostrar_imagen(self.ventana.objeto_actual)

    def rehacer_cambio(self):
        self.ventana.objeto_actual.imagen_actual = self.ventana.objeto_actual.imagen_actual + 1
        self.ventana.barra_ventanas.mostrar_imagen(self.ventana.objeto_actual)

    def reiniciar_imagen(self):
        self.ventana.objeto_actual.reiniciar_imagen()
        self.ventana.barra_ventanas.mostrar_imagen(self.ventana.objeto_actual)

    def llamar_funciones(self, funcion, parametros):

        self.ventana_flotante = QWidget()
        self.ventana_flotante.closeEvent = self.cerrando_widget_informacion
        self.ventana_flotante.setWindowTitle("Ingresar valores")
        self.ventana_flotante.resize(400, 70)
        ventana_flotante_layout = QHBoxLayout()
        entrada = QLineEdit()
        boton_confirmar_cambio = QPushButton("Confirmar cambio")

        ventana_flotante_layout.addWidget(QLabel("Ingrese el valor para modificar"))
        ventana_flotante_layout.addWidget(entrada)
        ventana_flotante_layout.addWidget(boton_confirmar_cambio)

        entrada.textChanged.connect(lambda: self.cambiar_cuando_cambia(funcion, parametros, entrada.text()))
        boton_confirmar_cambio.clicked.connect(lambda: self.guardar_cambio_cerrar_ventana())

        self.ventana_flotante.setLayout(ventana_flotante_layout)

        self.ventana_flotante.show()

    def cambiar_cuando_cambia(self, funcion, parametros, numero):

        try:
            if funcion == operaciones_entre_2_imagenes:
                imagen1 = parametros[0]
                imagen2 = self.seleccionador.itemData(parametros[1])

                parametros[0] = imagen1
                parametros[1] = imagen2

                print(parametros[0])
                print(parametros[1])
                print(numero)

            self.imagen_cambiada = funcion(*parametros, numero)
        except Exception as e:
            print(e)
            return

        if self.imagen_cambiada is None:
            return

        imagen_qimage = None

        if len(self.imagen_cambiada.shape) == 2:
            # Imagen en escala de grises
            h, w = self.imagen_cambiada.shape
            bytes_por_linea = w
            imagen_qimage = QImage(self.imagen_cambiada.data, w, h, bytes_por_linea, QImage.Format.Format_Grayscale8)
        else:
            # Imagen color BGR a RGB
            h, w, ch = self.imagen_cambiada.shape
            bytes_por_linea = ch * w
            imagen_rgb = cv2.cvtColor(self.imagen_cambiada, cv2.COLOR_BGR2RGB)
            imagen_qimage = QImage(imagen_rgb.data, w, h, bytes_por_linea, QImage.Format.Format_RGB888)

        imagen_pixmap = QPixmap.fromImage(imagen_qimage)

        self.ventana.label_imagen.setPixmap(imagen_pixmap)
        self.ventana.label_imagen.resize(imagen_pixmap.width(), imagen_pixmap.height())

    def guardar_cambio_cerrar_ventana(self):
        if self.imagen_cambiada is not None:
            self.ventana.objeto_actual.realizar_cambio(self.imagen_cambiada)
            self.ventana.barra_ventanas.mostrar_imagen(self.ventana.objeto_actual)
            self.ventana_flotante.close()
        else:
            return


    def llamar_funciones_entre_2_imagenes(self, funcion, numero):

        self.ventana_flotante = QWidget()
        self.ventana_flotante.closeEvent = self.cerrando_widget_informacion
        self.ventana_flotante.setWindowTitle("Seleccione la segunda imagen")
        self.ventana_flotante.resize(400, 70)
        ventana_flotante_layout = QHBoxLayout()
        self.seleccionador = QComboBox()
        self.seleccionador.addItem("Escoja una opcion", None)

        for objeto in self.ventana.imagenes_agregadas:

            if objeto == self.ventana.objeto_actual:
                continue
            ruta_imagen = objeto.imagen_linea_tiempo[objeto.imagen_actual]
            nombre = os.path.splitext(os.path.basename(ruta_imagen))[0]

            self.seleccionador.addItem(nombre)
            self.seleccionador.setItemData(self.seleccionador.count() - 1, objeto)

        boton_confirmar_cambio = QPushButton("Confirmar cambio")

        ventana_flotante_layout.addWidget(QLabel("Seleccione la segunda imagen"))
        ventana_flotante_layout.addWidget(self.seleccionador)
        ventana_flotante_layout.addWidget(boton_confirmar_cambio)

        self.seleccionador.currentIndexChanged.connect(lambda index: self.cambiar_cuando_cambia(funcion, [self.ventana.objeto_actual, index], numero))
        boton_confirmar_cambio.clicked.connect(lambda: self.guardar_cambio_cerrar_ventana())

        self.ventana_flotante.setLayout(ventana_flotante_layout)

        self.ventana_flotante.show()

    def cerrando_widget_informacion(self,event):
        self.ventana.barra_ventanas.mostrar_imagen(self.ventana.objeto_actual)
        event.accept()