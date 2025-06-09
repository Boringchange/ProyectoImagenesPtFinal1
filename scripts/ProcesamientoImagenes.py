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

    return cv2.cvtColor(cv2.imread(ruta_imagen, cv2.IMREAD_UNCHANGED), cv2.COLOR_BGR2RGB)

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

def operaciones_aritmeticas_imagen(objeto, operacion, numero):

    imagen = obtener_imagen_objeto(objeto)

    imagen_resultado = None

    if operacion == 1:
        imagen_resultado = cv2.add(imagen, int(numero))
    elif operacion == 2:
        imagen_resultado = cv2.subtract(imagen, int(numero))
    elif operacion == 3:
        imagen_resultado = cv2.multiply(imagen, float(numero))

    return imagen_resultado

def operacion_not(objeto:Imagen):
    imagen = obtener_imagen_objeto(objeto)
    imagen_resultado = cv2.bitwise_not(imagen)

    return cv2.cvtColor(imagen_resultado, cv2.COLOR_BGR2RGB)

def deteccion_objetos(objeto:Imagen):
    imagen1 = obtener_imagen_objeto(objeto)

    hsv = cv2.cvtColor(imagen1, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 30, 255])

    mascara = cv2.inRange(hsv, lower_white, upper_white)

    contornos, _ = cv2.findContours(mascara, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for c in contornos:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(imagen1, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv2.imshow("Detección de objetos por bordes", imagen1)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def operaciones_entre_2_imagenes(objeto1, objeto2, operacion):
    imagen1 = obtener_imagen_objeto(objeto1)

    imagen2 = obtener_imagen_objeto(objeto2)

    imagen2 = cv2.resize(imagen2, (imagen1.shape[:2][1], imagen1.shape[:2][0]))

    operacion_imagen = None

    if operacion == 1:
        operacion_imagen = cv2.add(imagen1, imagen2)
    elif operacion == 2:
        operacion_imagen = cv2.subtract(imagen1, imagen2)
    elif operacion == 3:
        operacion_imagen = cv2.multiply(imagen1, imagen2)
    elif operacion == 4:
        operacion_imagen = cv2.bitwise_or(imagen1, imagen2)
    elif operacion == 5:
        operacion_imagen = cv2.bitwise_and(imagen1, imagen2)
    elif operacion == 6:
        operacion_imagen = cv2.bitwise_xor(imagen1, imagen2)

    return cv2.cvtColor(operacion_imagen, cv2.COLOR_BGR2RGB)

def operaciones_umbralizacion(objeto:Imagen, operacion, numero):
    numero = int(numero)

    imagen = obtener_imagen_objeto(objeto)

    if len(imagen.shape) == 3:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    resultado = None

    if operacion == 0:  # Umbral binario simple
        _, resultado = cv2.threshold(imagen, numero, 255, cv2.THRESH_BINARY)

    elif operacion == 1:  # Umbral binario inverso
        _, resultado = cv2.threshold(imagen, numero, 255, cv2.THRESH_BINARY_INV)

    elif operacion == 3:  # Umbral adaptativo (media)
        resultado = cv2.adaptiveThreshold(imagen, 255,
                                          cv2.ADAPTIVE_THRESH_MEAN_C,
                                          cv2.THRESH_BINARY, 11, numero)

    elif operacion == 4:  # Umbral adaptativo (gaussiano)
        resultado = cv2.adaptiveThreshold(imagen, 255,
                                          cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          cv2.THRESH_BINARY, 11, numero)

    else:
        raise ValueError("Operación no válida (debe ser 0 a 4)")

    # Guardar la imagen resultante en el objeto
    return resultado

def operacion_umbral_otsu(objeto:Imagen):
    imagen = obtener_imagen_objeto(objeto)

    if len(imagen.shape) == 3:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    _, resultado = cv2.threshold(imagen, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return resultado

def obtener_valores_ecualizacion(intensidad):
    if intensidad is None:
        return
    hist = cv2.calcHist([intensidad], [0], None, [256], [0, 256]).flatten()

    probabilidad = hist / hist.sum()
    probabilidad_acumulada = np.cumsum(probabilidad)
    valor_minimo = np.min(intensidad)

    return valor_minimo, probabilidad_acumulada

def operacion_ecualizacion_exponencial(objeto:Imagen, numero):

    imagen = obtener_imagen_objeto(objeto)

    numero = float(numero)

    if numero <= 0:
        return None

    imagen_ycrcb = cv2.cvtColor(imagen, cv2.COLOR_RGB2YCrCb)

    y, cr, cb = cv2.split(imagen_ycrcb)

    valor_minimo, probabilidad_acumulada = obtener_valores_ecualizacion(y)

    y_nueva = np.zeros_like(y)

    filas, columnas = y.shape

    for i in range(filas):
        for j in range(columnas):
            epsilon = 1e-8
            valor = 1 - probabilidad_acumulada[y[i][j]]
            valor = max(valor, epsilon)
            y_nueva[i, j] = valor_minimo - (1 / numero) * np.log(valor)

    y_nueva = np.clip(y_nueva, 0, 255)
    y_nueva = y_nueva.astype(np.uint8)

    imagen_modificada = cv2.merge((y_nueva, cr, cb))
    imagen_resultado = cv2.cvtColor(imagen_modificada, cv2.COLOR_YCrCb2RGB)

    return imagen_resultado

def operacion_filtro_mediana(objeto:Imagen, numero):
    imagen = obtener_imagen_objeto(objeto)

    print("Hola")
    print(numero)

    numero = int(numero)

    if (numero % 2) == 0:
        return None

    # Función para hacer el filtro mediana
    imagen_resultado = cv2.medianBlur(imagen, int(numero))

    return cv2.cvtColor(imagen_resultado, cv2.COLOR_BGR2RGB)

def operacion_operador_prewitt(objeto:Imagen):
    imagen = obtener_imagen_objeto(objeto)

    kernel_prewitt_x = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]], dtype=np.float32)
    kernel_prewitt_y = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=np.float32)

    bordes_prewitt_x = cv2.filter2D(imagen, -1, kernel_prewitt_x)
    bordes_prewitt_y = cv2.filter2D(imagen, -1, kernel_prewitt_y)

    imagen_resultado = cv2.addWeighted(bordes_prewitt_x, 0.5, bordes_prewitt_y, 0.5, 0)

    return imagen_resultado

def operaciones_ruido(objeto: Imagen, opcion: int):
    imagen = obtener_imagen_objeto(objeto)
    imagen_resultado = imagen.copy()

    if opcion == 1:
        # --- Ruido sal y pimienta ---
        prob = 0.02  # proporción de píxeles con ruido
        output = imagen_resultado.copy()
        if len(imagen.shape) == 2:
            # Imagen en gris
            black = 0
            white = 255
        else:
            # Imagen en color
            black = [0, 0, 0]
            white = [255, 255, 255]

        total_pixels = imagen_resultado.shape[0] * imagen_resultado.shape[1]
        num_salt = int(total_pixels * prob / 2)
        num_pepper = int(total_pixels * prob / 2)

        # Sal (blanco)
        for _ in range(num_salt):
            i = np.random.randint(0, imagen_resultado.shape[0])
            j = np.random.randint(0, imagen_resultado.shape[1])
            output[i, j] = white

        # Pimienta (negro)
        for _ in range(num_pepper):
            i = np.random.randint(0, imagen_resultado.shape[0])
            j = np.random.randint(0, imagen_resultado.shape[1])
            output[i, j] = black

        imagen_resultado = output

    elif opcion == 2:
        # --- Ruido gaussiano ---
        mean = 0
        std = 25  # desviación estándar
        gauss = np.random.normal(mean, std, imagen.shape).astype(np.float32)
        noisy = imagen.astype(np.float32) + gauss
        imagen_resultado = np.clip(noisy, 0, 255).astype(np.uint8)

    return cv2.cvtColor(imagen_resultado, cv2.COLOR_BGR2RGB)

def operacion_filtro_segmentacion_completa_multiumbralizacion(objeto:Imagen, texto):
    if texto is None or texto == "":
        return None

    try:
        variables = [int(x) for x in texto.split(',')]
    except ValueError:
        return

    variables.sort()

    imagen = obtener_imagen_objeto(objeto)

    if len(imagen.shape) == 3:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    imagenCopiaGris = imagen.copy()
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

    imagen_resultado = segmentacion.copy()

    return imagen_resultado