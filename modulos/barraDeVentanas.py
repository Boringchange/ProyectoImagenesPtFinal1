import os.path
from pprint import pformat
import time

import cv2
from PyQt6.QtCore import Qt, QSize, QEvent, QTimer
from PyQt6.QtGui import QIcon, QPixmap, QImage
from PyQt6.QtWidgets import QDockWidget, QWidget, QVBoxLayout, QScrollArea, QToolButton, QLabel, QSizePolicy, QFrame, \
    QHBoxLayout, QMenu
import scripts.ProcesamientoImagenes
from scripts.Imagen import Imagen
from scripts.ProcesamientoImagenes import seleccionar_imagen


class BarraVentanas(QWidget):
    def __init__(self, referenciaPadre):
        super().__init__()

        self.referenciaPadre = referenciaPadre

        self.setContentsMargins(0,0,0,0)
        self.barra_ventana = QVBoxLayout()
        self.setLayout(self.barra_ventana)
        self.barra_ventana.setContentsMargins(0,0,0,0)
        self.barra_ventana.setSpacing(0)

        self.imagen = QIcon("img/imagen.png")
        self.imagen_cerrar = QIcon("img/imagen_cerrar.png")
        self.barra_ventana_original = self.crear_scroll_default(referenciaPadre)
        self.barra_ventana_remplazo = self.crear_scroll_remplazo(referenciaPadre)

        self.barra_ventana.addWidget(self.barra_ventana_original)

    def mostrar_context_menu(self, pos):
        menu = QMenu(self)
        accion = menu.addAction("Descargar imagen")
        accion2 = menu.addAction("Descargar paquete de imagenes")
        accion.triggered.connect(lambda: print("Hola desde el menú!"))
        accion2.triggered.connect(lambda: )
        menu.exec(self.mapToGlobal(pos))

    def crear_scroll_default(self, referenciaPadre):

        scroll = QScrollArea()

        scroll.setObjectName("btn_scroll_area")
        scroll.verticalScrollBar().setObjectName("btn_scroll_horizontal")
        scroll.setWidgetResizable(True)

        scroll_content = QWidget()
        scroll_content.setContentsMargins(0,0,0,0)
        scroll_content.setObjectName("btn_contenedor")
        scroll_layout = QVBoxLayout()
        scroll_layout.setContentsMargins(0,0,0,0)
        scroll_layout.setSpacing(0)
        scroll_layout.setObjectName("btn_layout")
        scroll_content.setLayout(scroll_layout)
        scroll.setWidget(scroll_content)

        self.lista_botones_ventanas = []

        for imagen_objeto in referenciaPadre.imagenes_agregadas:
            imagen_icono = QToolButton()
            imagen_icono.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            imagen_icono.customContextMenuRequested.connect()
            imagen_icono.setIcon(self.imagen)

            ruta_imagen = imagen_objeto.imagen_linea_tiempo[imagen_objeto.imagen_actual]
            nombre = os.path.split(os.path.basename(ruta_imagen))[0]

            imagen_icono.setText(nombre)
            imagen_icono.setToolTip(imagen_icono.text())
            imagen_icono.setObjectName("btn_ventanas")
            imagen_icono.setIconSize(QSize(39, 39))
            imagen_icono.setFixedSize(QSize(39, 39))
            imagen_icono.clicked.connect(lambda _,objeto = imagen_objeto : self.mostrar_imagen(objeto))

            scroll_layout.addWidget(imagen_icono)

            self.lista_botones_ventanas.append(imagen_icono)

            imagen_icono.installEventFilter(self)


        add_imagen = QIcon("img/add_imagen.png")
        add_imagen_icono = QToolButton()
        add_imagen_icono.setIcon(add_imagen)
        add_imagen_icono.setIconSize(QSize(39, 39))
        add_imagen_icono.setFixedSize(QSize(39, 39))
        add_imagen_icono.setText("Añadir imagen")
        add_imagen_icono.setToolTip(add_imagen_icono.text())
        add_imagen_icono.setObjectName("btn_ventanas")
        add_imagen_icono.clicked.connect(lambda: self.add_image(referenciaPadre))

        divisor = QFrame()
        divisor.setFrameShape(QFrame.Shape.HLine)
        divisor.setFrameShadow(QFrame.Shadow.Plain)

        scroll_layout.addWidget(divisor)
        scroll_layout.addWidget(add_imagen_icono)
        scroll.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)

        return scroll
    def crear_scroll_remplazo(self, referenciaPadre):

        scroll = QScrollArea()

        scroll.setObjectName("btn_scroll_area")
        scroll.verticalScrollBar().setObjectName("btn_scroll_horizontal")
        scroll.setWidgetResizable(True)

        lista_imagenes_objetos = referenciaPadre.imagenes_agregadas

        scroll_content = QWidget()
        scroll_content.setObjectName("btn_contenedor")
        scroll_layout = QVBoxLayout()
        scroll_layout.setObjectName("btn_layout")
        scroll_content.setLayout(scroll_layout)
        scroll.setWidget(scroll_content)

        for imagen_objeto in lista_imagenes_objetos:

            ventana_contenedor = QWidget()
            ventana_layout = QHBoxLayout()

            ventana_contenedor.setContentsMargins(0,0,0,0)
            ventana_layout.setContentsMargins(0,0,0,0)
            ventana_layout.setSpacing(0)
            ventana_contenedor.setLayout(ventana_layout)

            ruta_imagen = imagen_objeto.imagen_linea_tiempo[imagen_objeto.imagen_actual]
            nombre = os.path.splitext(os.path.basename(ruta_imagen))[0]

            imagen_icono = QToolButton()
            imagen_icono.setIcon(self.imagen)
            imagen_icono.setText(nombre)
            imagen_icono.setToolTip(imagen_icono.text())
            imagen_icono.setObjectName("btn_ventanas")
            imagen_icono.setIconSize(QSize(39, 39))
            imagen_icono.setFixedSize(QSize(39, 39))
            imagen_icono.clicked.connect(lambda _,objeto = imagen_objeto : self.mostrar_imagen(objeto))

            label = QLabel(nombre)
            label.setObjectName("label_imagen_ventana")

            imagen_eliminar_icono = QToolButton()
            imagen_eliminar_icono.setIcon(self.imagen_cerrar)
            imagen_eliminar_icono.setText("Cerrar")
            imagen_eliminar_icono.setToolTip(imagen_icono.text())
            imagen_eliminar_icono.setObjectName("btn_ventanas")
            imagen_eliminar_icono.setIconSize(QSize(39, 39))
            imagen_eliminar_icono.setFixedSize(QSize(39, 39))
            imagen_eliminar_icono.clicked.connect(lambda _, objeto = imagen_objeto : self.eliminar_imagen(objeto))

            ventana_layout.addWidget(imagen_icono)
            ventana_layout.addWidget(label)
            ventana_layout.addWidget(imagen_eliminar_icono)

            scroll_layout.addWidget(ventana_contenedor)

        add_imagen = QIcon("img/add_imagen.png")
        add_imagen_icono = QToolButton()
        add_imagen_icono.setIcon(add_imagen)
        add_imagen_icono.setIconSize(QSize(39, 39))
        add_imagen_icono.setFixedSize(QSize(39, 39))
        add_imagen_icono.setText("Añadir imagen")
        add_imagen_icono.setToolTip(add_imagen_icono.text())
        add_imagen_icono.setObjectName("btn_ventanas")
        add_imagen_icono.clicked.connect(lambda: self.add_image(referenciaPadre))

        divisor = QFrame()
        divisor.setFrameShape(QFrame.Shape.HLine)
        divisor.setFrameShadow(QFrame.Shadow.Plain)

        scroll_layout.addWidget(divisor)
        scroll_layout.addWidget(add_imagen_icono)
        scroll.viewport().installEventFilter(self)
        scroll.hide()

        scroll.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)

        return scroll

    def eventFilter(self, source, event):
        try:
            self.lista_botones_ventanas.index(source)
            if event.type() == QEvent.Type.Enter:
                self.switchToReplacement()
        except:
            if source == self.barra_ventana_remplazo.viewport():
                if event.type() == QEvent.Type.Leave:
                    QTimer.singleShot(200, self.switchToOriginal)
        return super().eventFilter(source, event)

    def switchToReplacement(self):

        widgetActual = self.barra_ventana.itemAt(0).widget()
        self.barra_ventana_remplazo = self.crear_scroll_remplazo(self.referenciaPadre)

        self.barra_ventana.replaceWidget(widgetActual, self.barra_ventana_remplazo)
        widgetActual.hide()
        self.barra_ventana_remplazo.show()

    def switchToOriginal(self):

        self.barra_ventana_original = self.crear_scroll_default(self.referenciaPadre)
        widgetActual = self.barra_ventana.itemAt(0).widget()

        self.barra_ventana.replaceWidget(widgetActual, self.barra_ventana_original)
        widgetActual.hide()
        self.barra_ventana_original.show()

    def add_image(self, referenciaPadre):
        ruta_imagen = seleccionar_imagen(referenciaPadre.imagenes_agregadas.__len__())

        if ruta_imagen is None:
            return

        objeto_imagen = Imagen(ruta_imagen, str(referenciaPadre.imagenes_agregadas.__len__() + 1))

        referenciaPadre.imagenes_agregadas.append(objeto_imagen)

        self.mostrar_imagen(objeto_imagen)


    def mostrar_imagen(self, objeto):

        self.referenciaPadre.objeto_actual = objeto

        imagen_rapida = QImage(objeto.imagen_linea_tiempo[objeto.imagen_actual])
        imagen = QPixmap.fromImage(imagen_rapida)
        self.referenciaPadre.label_imagen.setPixmap(imagen)
        self.referenciaPadre.label_imagen.resize(imagen.width(), imagen.height())

        barra_ventana_original = self.crear_scroll_default(self.referenciaPadre)

        widgetActual = self.barra_ventana.itemAt(0).widget()

        self.barra_ventana.replaceWidget(widgetActual, barra_ventana_original)
        widgetActual.hide()

        self.activar_desactivar_botones_general()
        barra_ventana_original.show()

    def eliminar_imagen(self, objeto):
        self.referenciaPadre.imagenes_agregadas.remove(objeto)
        objeto.eliminar_imagen()

        try:
            ultimo_objeto = self.referenciaPadre.imagenes_agregadas[-1]
            self.mostrar_imagen(ultimo_objeto)
            self.referenciaPadre.objeto_actual = ultimo_objeto
        except:
            barra_ventana_original = self.crear_scroll_default(self.referenciaPadre)

            widgetActual = self.barra_ventana.itemAt(0).widget()

            self.referenciaPadre.label_imagen.clear()

            self.barra_ventana.replaceWidget(widgetActual, barra_ventana_original)
            self.referenciaPadre.objeto_actual = None
            widgetActual.hide()
            barra_ventana_original.show()
            self.activar_desactivar_botones_general()


    def activar_desactivar_botones_general(self):
        if self.referenciaPadre.objeto_actual is None:
            self.referenciaPadre.barra_herramientas.barra_herramientas.setDisabled(True)
        else:
            self.referenciaPadre.barra_herramientas.barra_herramientas.setDisabled(False)
            self.activar_desactivar_botones_funcionalidad()

    def activar_desactivar_botones_funcionalidad(self):
        try:
            if self.referenciaPadre.objeto_actual.imagen_actual <= 0:
                self.referenciaPadre.barra_herramientas.flecha_izquierda_icono.setDisabled(True)
            else:
                self.referenciaPadre.barra_herramientas.flecha_izquierda_icono.setDisabled(False)
            if self.referenciaPadre.objeto_actual.imagen_actual >= (self.referenciaPadre.objeto_actual.imagen_linea_tiempo.__len__() - 1):
                self.referenciaPadre.barra_herramientas.flecha_derecha_icono.setDisabled(True)
            else:
                self.referenciaPadre.barra_herramientas.flecha_derecha_icono.setDisabled(False)
            if self.referenciaPadre.objeto_actual.imagen_linea_tiempo.__len__() > 1:
                self.referenciaPadre.barra_herramientas.recargar_icon.setDisabled(False)
            else:
                self.referenciaPadre.barra_herramientas.recargar_icon.setDisabled(True)
        except:
            return