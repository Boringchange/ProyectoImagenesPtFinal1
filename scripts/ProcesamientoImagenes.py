from io import BytesIO
from tkinter import filedialog
from PIL import Image

from matplotlib import pyplot as plt

from scripts.Imagen import Imagen
import cv2
import numpy as np

def seleccionar_imagen(imagen):
    ruta = filedialog.askopenfilename(title="Seleccionar imagen " + str(imagen + 1),filetypes=(("JPG", "*.jpg"), ("JPEG", "*.jpeg"),("PNG", "*png")))
    if not ruta:
        ruta = None
    return ruta

def obtener_imagen_objeto(objeto:Imagen):
    ruta_imagen = objeto.imagen_linea_tiempo[objeto.imagen_actual]

    return cv2.imread(ruta_imagen, cv2.IMREAD_UNCHANGED)

def mostrar_imagenes_rgb(objeto: Imagen):

    imagen = obtener_imagen_objeto(objeto)

    r_intensidad, g_intensidad, b_intensidad = cv2.split(imagen)
    negros = np.zeros_like(r_intensidad)
    imagen_roja = cv2.merge([r_intensidad,negros, negros])
    imagen_verde = cv2.merge([negros,g_intensidad, negros])
    imagen_azul = cv2.merge([negros,negros, b_intensidad])

    cv2.imshow("Canal Rojo", imagen_roja)
    cv2.imshow("Canal Verde", imagen_verde)
    cv2.imshow("Canal Azul", imagen_azul)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def conversion_grises(objeto:Imagen):
    imagen = obtener_imagen_objeto(objeto)

    if len(imagen.shape) == 3 and imagen.shape[2] == 3:
        return cv2.cvtColor(imagen,cv2.COLOR_RGB2GRAY)
    else:
        print("La imagen ya está en escala de grises.")
        return imagen

def grafica_a_imagen(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    img = Image.open(buf)
    img_np = np.array(img)
    if img_np.shape[2] == 4:
        img_np = cv2.cvtColor(img_np, cv2.COLOR_RGBA2RGB)
    plt.close(fig)
    return img_np

def mostrar_histograma(objeto:Imagen):
    imagen = obtener_imagen_objeto(objeto)
    try:
        imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    except:
        imagen_gris = imagen.copy()

    fig1, ax1 = plt.subplots()
    ax1.hist(imagen_gris.ravel(), bins=256, range=(0, 256), color='gray')
    ax1.set_title("Histograma de grises")

    histogramaGris = grafica_a_imagen(fig1)
    try:
        fig2, ax2 = plt.subplots()
        color = ('b', 'g', 'r')
        for i, col in enumerate(color):
            hist = cv2.calcHist([imagen], [i], None, [256], [0, 256])
            ax2.plot(hist, color=col)
            ax2.set_xlim([0, 256])
        ax2.set_title("Histograma de colores")
    except:
        cv2.imshow("Histograma gris", histogramaGris)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return

    histogramaColores = grafica_a_imagen(fig2)

    cv2.imshow("Histograma gris", histogramaGris)
    cv2.imshow("Histograma colores", histogramaColores)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
