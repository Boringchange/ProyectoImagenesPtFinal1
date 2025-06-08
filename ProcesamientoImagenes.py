import tkinter as tk
from io import BytesIO
from tkinter import filedialog
import cv2
import numpy as np
import ctypes
import matplotlib.pyplot as plt
from PIL import Image
from fontTools.misc.textTools import tostr


class ProcesamientoDeImagenes:
    imagenes = [None] * 2
    ruta_imagenes = [None] * 2
    imagen1 = None
    imagen2 = None
    ruta_imagen1 = ""
    ruta_imagen2 = ""
    rescalarImagenes = [None] * 2
    imagenesSeleccionadasMostrar = [None] * 2
    imagenesSeleccionadasAnteriorMostrar = [None] * 2
    histogramaPedido = False

    imagen1_roja = None
    imagen1_verde = None
    imagen1_azul = None
    imagen2_roja = None
    imagen2_verde = None
    imagen2_azul = None

    imagen_actual = None
    titulo_imagen_actual = ""

    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    ancho = user32.GetSystemMetrics(0)
    alto = user32.GetSystemMetrics(1)

    def seleccionar_imagen(self, imagen):
        self.ruta_imagenes[imagen] = filedialog.askopenfilename(title="Seleccionar imagen " + str(imagen + 1), filetypes=(("JPG", "*.jpg"), ("JPEG", "*.jpeg"), ("PNG", "*png")))
        self.imagenes[imagen] = None

    def comprobar_imagen_existe(self, imagen):
        if self.imagenesSeleccionadasMostrar[imagen] is None:
            if self.imagenesSeleccionadasAnteriorMostrar[imagen] is None:
                return False
            else:
                self.imagenesSeleccionadasMostrar[imagen] = self.imagenesSeleccionadasAnteriorMostrar[imagen].copy()
                return True
        if self.histogramaPedido:
            self.histogramaPedido = False
            return True
        self.imagenesSeleccionadasAnteriorMostrar[imagen] = self.imagenesSeleccionadasMostrar[imagen].copy()
        return True

    def comprobar_imagen_existe_original(self, imagen):
        if self.ruta_imagenes[imagen] == "" or self.ruta_imagenes[imagen] is None:
            return False
        self.imagenes[imagen] = cv2.imread(self.ruta_imagenes[imagen])
        self.imagenes[imagen] = cv2.cvtColor(self.imagenes[imagen], cv2.COLOR_BGR2RGB)
        return True
    def reescalar_imagen(self, imagen):
        if imagen is None:
            print(imagen)
            exit(-1)
        altura, anchura = imagen.shape[:2]

        escala_ancho = (self.ancho / 4) / anchura
        escala_alto = (self.alto / 3) / altura

        escala = min(escala_ancho, escala_alto)

        if escala >= 1:
            return imagen

        return cv2.resize(imagen, (int(anchura * escala), int(altura * escala)), interpolation=cv2.INTER_AREA)

    def mostrar_imagenes_rgb(self, imagen):

        if not self.comprobar_imagen_existe(imagen):
            self.imagenesSeleccionadasMostrar[imagen] = None
            return
        collage = None

        r_intensidad, g_intensidad, b_intensidad = cv2.split(self.imagenesSeleccionadasAnteriorMostrar[imagen])
        negros = np.zeros_like(r_intensidad)
        imagen_roja = cv2.merge([r_intensidad,negros, negros])
        imagen_verde = cv2.merge([negros,g_intensidad, negros])
        imagen_azul = cv2.merge([negros,negros, b_intensidad])


        collage = np.hstack((imagen_roja,imagen_verde,imagen_azul))
        self.imagenesSeleccionadasMostrar[imagen] = cv2.cvtColor(collage, cv2.COLOR_BGR2RGB)

    def operaciones_aritmeticas_imagen(self, numero, imagen, operacion):

        if not self.comprobar_imagen_existe(imagen):
            return

        if operacion == 1:
            self.imagenesSeleccionadasMostrar[imagen] = cv2.add(self.imagenesSeleccionadasAnteriorMostrar[imagen], int(numero))
            titulo = "Suma"
        if operacion == 2:
            self.imagenesSeleccionadasMostrar[imagen] = cv2.subtract(self.imagenesSeleccionadasAnteriorMostrar[imagen],int(numero))
            titulo = "Resta"
        if operacion == 3:
            self.imagenesSeleccionadasMostrar[imagen] = cv2.multiply(self.imagenesSeleccionadasAnteriorMostrar[imagen], numero)
            titulo = "Multiplicacion"

    def operaciones_logicas_imagenes(self, operacion):
        if not self.comprobar_imagen_existe(0):
            print("No existe, pero no hay pex")
        if not self.comprobar_imagen_existe(1):
            print("No existe, pero no hay pex")

        if operacion != 4:
            imagen1_copia = self.imagenesSeleccionadasAnteriorMostrar[0]
            imagen2_copia = cv2.resize(self.imagenes[1], (imagen1_copia.shape[:2][1], imagen1_copia.shape[:2][0]))
        else:
            if self.imagenesSeleccionadasAnteriorMostrar[0] is not None:
                imagen1negada = cv2.bitwise_not(self.imagenesSeleccionadasAnteriorMostrar[0])
                self.imagenesSeleccionadasMostrar[0] = imagen1negada
            if self.imagenesSeleccionadasAnteriorMostrar[1] is not None:
                imagen2negada = cv2.bitwise_not(self.imagenesSeleccionadasAnteriorMostrar[1])
                self.imagenesSeleccionadasMostrar[1] = imagen2negada
            return

        operacion_imagen = None

        if operacion == 1:
            operacion_imagen = cv2.bitwise_or(imagen1_copia, imagen2_copia)
        if operacion == 2:
            operacion_imagen = cv2.bitwise_and(imagen1_copia, imagen2_copia)
        if operacion == 3:
            operacion_imagen = cv2.bitwise_xor(imagen1_copia, imagen2_copia)

        self.imagenesSeleccionadasMostrar[0] = operacion_imagen
        self.imagenesSeleccionadasMostrar[1] = None

    def umbralizado(self, imagen, umbral):

        if not self.comprobar_imagen_existe(imagen):
            return

        try:
            imagen_escala_grises = cv2.cvtColor(self.imagenesSeleccionadasAnteriorMostrar[imagen], cv2.COLOR_RGB2GRAY)
        except:
            return
        _, self.imagenesSeleccionadasMostrar[imagen] = cv2.threshold(imagen_escala_grises, int(umbral), 255, cv2.THRESH_BINARY)

    def conversion_grises(self, imagen):

        if not self.comprobar_imagen_existe(imagen):
            return

        if len(self.imagenesSeleccionadasAnteriorMostrar[imagen].shape) == 3 and self.imagenesSeleccionadasAnteriorMostrar[imagen].shape[2] == 3:
            self.imagenesSeleccionadasMostrar[imagen] = cv2.cvtColor(self.imagenesSeleccionadasAnteriorMostrar[imagen], cv2.COLOR_RGB2GRAY)
        else:
            print("La imagen ya está en escala de grises.")
            return self.imagenesSeleccionadasAnteriorMostrar[imagen]


    def grafica_a_imagen(self, fig):
        buf = BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)
        img = Image.open(buf)
        img_np = np.array(img)
        if img_np.shape[2] == 4:
            img_np = cv2.cvtColor(img_np, cv2.COLOR_RGBA2RGB)
        plt.close(fig)
        return img_np

    def histograma(self, imagen):

        if imagen is None:
            return None

        try:
            imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        except:
            imagen_gris = imagen.copy()

        fig1, ax1 = plt.subplots()
        ax1.hist(imagen_gris.ravel(), bins=256, range = (0, 256), color = 'gray')
        ax1.set_title("Histograma de grises")

        histogramaGris = self.grafica_a_imagen(fig1)
        try:
            fig2, ax2 = plt.subplots()
            color = ('b', 'g', 'r')
            for i, col in enumerate(color):
                hist = cv2.calcHist([imagen], [i], None, [256], [0, 256])
                ax2.plot(hist, color=col)
                ax2.set_xlim([0, 256])
            ax2.set_title("Histograma de colores")
        except:
            return histogramaGris

        histogramaColores = self.grafica_a_imagen(fig2)
        collage = np.hstack((histogramaGris, histogramaColores))

        return collage

    def obtener_valores_ecualizacion(self, intensidad):
        if intensidad is None:
            return
        hist = cv2.calcHist([intensidad], [0], None, [256], [0, 256]).flatten()

        probabilidad = hist / hist.sum()
        probabilidad_acumulada = np.cumsum(probabilidad)
        valor_minimo = np.min(intensidad)

        return valor_minimo, probabilidad_acumulada

    def ecualizacion_exponencial(self, imagen, variable):

        if imagen is None:
            return None

        if variable <= 0:
            return imagen

        imagen_ycrcb = cv2.cvtColor(imagen, cv2.COLOR_RGB2YCrCb)

        y, cr, cb = cv2.split(imagen_ycrcb)

        valor_minimo, probabilidad_acumulada = self.obtener_valores_ecualizacion(y)

        y_nueva = np.zeros_like(y)

        filas, columnas = y.shape

        for i in range(filas):
            for j in range(columnas):
                epsilon = 1e-8
                valor = 1 - probabilidad_acumulada[y[i][j]]
                valor = max(valor, epsilon)
                y_nueva[i , j] = valor_minimo - (1 / variable) * np.log(valor)

        y_nueva = np.clip(y_nueva, 0, 255)
        y_nueva = y_nueva.astype(np.uint8)

        imagen_modificada = cv2.merge((y_nueva, cr, cb))
        imagen_resultado = cv2.cvtColor(imagen_modificada, cv2.COLOR_YCrCb2RGB)

        return imagen_resultado

    def filtro_mediana(self, imagen, variable):
        #Validación de que la imagen exista

        print("Hola demonio")

        print(self.imagenesSeleccionadasMostrar[imagen])

        if not self.comprobar_imagen_existe(imagen):
            return

        #Función para hacer el filtro mediana
        self.imagenesSeleccionadasMostrar[imagen] = cv2.medianBlur(self.imagenesSeleccionadasAnteriorMostrar[imagen], int(variable))

    def filtro_operador_prewitt(self, imagen):
        if not self.comprobar_imagen_existe(imagen):
            return

        kernel_prewitt_x = np.array([[1,0,-1],[1,0,-1],[1,0,-1]], dtype = np.float32)
        kernel_prewitt_y = np.array([[1,1,1], [0,0,0], [-1,-1,-1]], dtype= np.float32)

        bordes_prewitt_x = cv2.filter2D(self.imagenesSeleccionadasAnteriorMostrar[imagen], -1, kernel_prewitt_x)
        bordes_prewitt_y = cv2.filter2D(self.imagenesSeleccionadasAnteriorMostrar[imagen], -1, kernel_prewitt_y)

        self.imagenesSeleccionadasMostrar[imagen] = cv2.addWeighted(bordes_prewitt_x, 0.5, bordes_prewitt_y, 0.5, 0)

    def filtro_segmentacion_completa_multiumbralizacion(self, imagen, texto):
        if not self.comprobar_imagen_existe(imagen) or texto is None or texto == "":
            return

        try:
            variables = [int(x) for x in texto.split(',')]
        except ValueError:
            return

        variables.sort()

        self.conversion_grises(imagen)
        imagenCopiaGris = self.imagenesSeleccionadasMostrar[imagen].copy()
        separacionGrises = 255/(len(variables)+1)
        segmentacion = np.zeros_like(imagenCopiaGris)


        for i in range(len(variables)):
            if i == 0:
                segmentacion[imagenCopiaGris <= variables[i]] = separacionGrises * (i + 1)
                continue
            if i == len(variables):
                segmentacion[imagenCopiaGris > variables[i - 1]] = separacionGrises * (i + 1)
                continue
            segmentacion[(imagenCopiaGris > variables[i - 1]) & (imagenCopiaGris <= variables[i])] = separacionGrises * (i + 1)

        self.imagenesSeleccionadasMostrar[imagen] = segmentacion.copy()