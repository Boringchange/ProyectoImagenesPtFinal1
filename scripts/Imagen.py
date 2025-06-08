import shutil
from tkinter import filedialog

import cv2
import os

from PyQt6.QtWidgets import QFileDialog


class Imagen:

    def __init__(self, ruta_imagen:str, numero_imagen:str):

        self.ruta_carpeta = None
        self.imagen_linea_tiempo = []
        self.imagen_actual = None
        self.tam_imagen_linea_tiempo = None
        self.nombre_sin_extension = None

        imagenCopia = cv2.imread(ruta_imagen, cv2.IMREAD_UNCHANGED)

        nombre_con_extension = os.path.basename(ruta_imagen)
        self.nombre_sin_extension = os.path.splitext(nombre_con_extension)[0]

        self.ruta_carpeta = "imagenesGeneradas/" + self.nombre_sin_extension + "_" +numero_imagen
        os.makedirs(self.ruta_carpeta, exist_ok=True)

        ruta_imagen_copia = self.ruta_carpeta + "/" + nombre_con_extension

        cv2.imwrite(ruta_imagen_copia, imagenCopia)

        self.imagen_linea_tiempo.append(ruta_imagen_copia)
        self.imagen_actual = 0
        self.tam_imagen_linea_tiempo = 1

    def realizar_cambio(self, imagen):

        try:
            while(True):
                ruta_eliminar = self.imagen_linea_tiempo.pop(self.imagen_actual + 1)

                if os.path.exists(ruta_eliminar):
                    os.remove(ruta_eliminar)
                self.tam_imagen_linea_tiempo -= 1
        except:
            ruta_imagen = self.ruta_carpeta +"/"+self.nombre_sin_extension + "_" + str(self.imagen_actual + 1) + ".png"
            cv2.imwrite(ruta_imagen, imagen)
            self.imagen_linea_tiempo.append(ruta_imagen)
            self.tam_imagen_linea_tiempo += 1
            self.imagen_actual += 1

    def reiniciar_imagen(self):
        try:
            while(True):
                ruta_eliminar = self.imagen_linea_tiempo.pop(1)

                if(os.path.exists(ruta_eliminar)):
                    os.remove(ruta_eliminar)

                print(ruta_eliminar)
                self.tam_imagen_linea_tiempo -= 1
        except:
            self.imagen_actual = 0

    def eliminar_imagen(self):
        shutil.rmtree(self.ruta_carpeta)

    def descargar_imagen(self):

        nombre_imagen = os.path.basename(self.imagen_linea_tiempo[self.imagen_actual])

        ruta = filedialog.asksaveasfilename(initialfile= nombre_imagen, defaultextension=".png", filetypes=[("All files", "*.*")], title="Guardar imagen como")
        imagen = cv2.imread(self.imagen_linea_tiempo[self.imagen_actual], cv2.IMREAD_UNCHANGED)

        # Usar la ruta seleccionada
        if ruta:
            cv2.imwrite(ruta, imagen)
        else:
            return

    def descargar_carpeta(self):

        nombre_carpeta = filedialog.askdirectory(title="Guardar carpeta como")

        nombre_ultima_carpeta = os.path.basename(os.path.normpath(self.ruta_carpeta))

        nombre_carpeta_final = nombre_carpeta + "/" + nombre_ultima_carpeta

        shutil.make_archive(nombre_carpeta_final, 'zip', self.ruta_carpeta)