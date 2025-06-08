from tkinter import filedialog
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
