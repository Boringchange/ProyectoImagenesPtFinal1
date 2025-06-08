import customtkinter
from ProcesamientoImagenes import ProcesamientoDeImagenes
from PIL import Image, ImageTk
import tkinter as tk

#Objeto que nos ayudara al manejo del procesamiento de las imagenes
procesoDeImagenes = ProcesamientoDeImagenes()

imagenesTK = [None] * 2
referenciaCanvas = [None] * 2

btnAnteriorPresionado = None
btnTextoAnteriorPresionado = None

referenciaIntroducirDatos = [None] * 2
referenciaIntroducirLabelDatos = [None] * 2

variableModificar = [None] * 2
variableModificarString = [None] * 2

referenciaBttns = None

textoBoton = None
corriendoFuncion = None
referenciaSelf = None
referenciaSelfImages = None
referenciaBotonQuitar = [None] * 2
referenciaBotonRestablecer = [None] * 2
ultimoBotonPresionado = None

def mostrar_imagenes():

    global referenciaSelfImages

    if procesoDeImagenes.imagenesSeleccionadasMostrar[0] is None and procesoDeImagenes.imagenesSeleccionadasMostrar[1] is None:
        referenciaSelfImages.columnconfigure(0, weight=0)
    else:
        referenciaSelfImages.columnconfigure(0, weight=1)

    if procesoDeImagenes.imagenesSeleccionadasMostrar[0] is not None:
        referenciaSelfImages.rowconfigure(0, weight=1)
        referenciaSelfImages.canvas.grid(row = 0, column = 0)
    else:
        referenciaSelfImages.rowconfigure(0, weight=0)
        referenciaSelfImages.canvas.grid_remove()
    if procesoDeImagenes.imagenesSeleccionadasMostrar[1] is not None:
        referenciaSelfImages.rowconfigure(1, weight=1)
        referenciaSelfImages.canvas1.grid(row = 1, column = 0)
    else:
        referenciaSelfImages.rowconfigure(1, weight=0)
        referenciaSelfImages.canvas1.grid_remove()

    imagenesTK[0] = None
    imagenesTK[1] = None

    if imagenesTK[0] is None and procesoDeImagenes.imagenesSeleccionadasMostrar[0] is not None:
        imagen_pil = Image.fromarray(procesoDeImagenes.imagenesSeleccionadasMostrar[0])
        imagen_tk = ImageTk.PhotoImage(image=imagen_pil)
        imagenesTK[0] = imagen_tk
    if imagenesTK[1] is None and procesoDeImagenes.imagenesSeleccionadasMostrar[1] is not None:
        imagen_pil = Image.fromarray(procesoDeImagenes.imagenesSeleccionadasMostrar[1])
        imagen_tk = ImageTk.PhotoImage(image=imagen_pil)
        imagenesTK[1] = imagen_tk

    if  procesoDeImagenes.imagenesSeleccionadasMostrar[0] is not None:
        alto1, ancho1 = procesoDeImagenes.imagenesSeleccionadasMostrar[0].shape[:2]
        referenciaCanvas[0].config(width=ancho1, height=alto1)
        referenciaCanvas[0].create_image(ancho1/2, alto1/2, image=imagenesTK[0])

    if  procesoDeImagenes.imagenesSeleccionadasMostrar[1] is not None:
        alto2, ancho2= procesoDeImagenes.imagenesSeleccionadasMostrar[1].shape[:2]
        referenciaCanvas[1].config(width=ancho2, height=alto2)
        referenciaCanvas[1].create_image(ancho2/2, alto2/2, image=imagenesTK[1])

class images(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        global referenciaSelfImages

        self.rowconfigure(0, weight = 0)
        self.columnconfigure(0, weight = 6)
        self.rowconfigure(1, weight = 0)
        self.columnconfigure(1, weight = 0)
        self.columnconfigure(2, weight = 0)

        self.canvas = tk.Canvas(self, width=450, height=450, bg="#2b2b2b", highlightthickness=1)
        self.canvas1 = tk.Canvas(self, width=450, height=450, bg="#2b2b2b", highlightthickness=1)

        referenciaSelfImages = self

        self.labelImg1 = customtkinter.CTkLabel(self, text="IMG1")
        self.labelImg2 = customtkinter.CTkLabel(self, text="IMG2")
        self.entradaImg1 = customtkinter.CTkEntry(self, width=100)
        self.entradaImg2 = customtkinter.CTkEntry(self, width=100)

        variableModificar[0] = customtkinter.DoubleVar(value = 0)
        variableModificar[1] = customtkinter.DoubleVar(value = 0)
        variableModificarString[0] = customtkinter.StringVar(value = "80,160")
        variableModificarString[1] = customtkinter.StringVar(value = "80, 160")

        variableModificar[0].trace_add("write", lambda *args : llamar_operaciones())
        variableModificar[1].trace_add("write", lambda *args : llamar_operaciones())
        variableModificarString[0].trace_add("write", lambda *args : llamar_operaciones())
        variableModificarString[1].trace_add("write", lambda *args : llamar_operaciones())

        self.entradaImg1.configure(textvariable = variableModificar[0])
        self.entradaImg2.configure(textvariable = variableModificar[1])

        referenciaIntroducirDatos[0] = self.entradaImg1
        referenciaIntroducirDatos[1] = self.entradaImg2
        referenciaIntroducirLabelDatos[0] = self.labelImg1
        referenciaIntroducirLabelDatos[1] = self.labelImg2

        referenciaCanvas[0] = self.canvas
        referenciaCanvas[1] = self.canvas1

class btnsFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=1)
        self.grid_rowconfigure(7, weight=1)
        self.grid_rowconfigure(8, weight=1)
        self.grid_rowconfigure(9, weight=1)

        self.btn1 = customtkinter.CTkButton(self, text="RGB", command=lambda: self.button_callback(self.btn1))
        self.btn1.grid(row=0, column=0, padx=(20,20), pady=(20,10), sticky="nsew", columnspan=4)

        self.btn2 = customtkinter.CTkButton(self, text="Suma", command=lambda: self.button_callback(self.btn2))
        self.btn2.grid(row=1, column=0, padx=(20,0), pady=(10,10), sticky="nsew")
        self.btn6 = customtkinter.CTkButton(self, text="Resta", command=lambda: self.button_callback(self.btn6))
        self.btn6.grid(row=1, column=1, padx=(10,10), pady=(10,10), sticky="nsew", columnspan=2)
        self.btn7 = customtkinter.CTkButton(self, text="Multiplicacion", command=lambda: self.button_callback(self.btn7))
        self.btn7.grid(row=1, column=3, padx=(0,20), pady=(10, 10), sticky="nsew")

        self.btn3 = customtkinter.CTkButton(self, text="Or", command=lambda: self.button_callback(self.btn3))
        self.btn3.grid(row=2, column=0, padx=(20,0), pady=(10,10), sticky="nsew")
        self.btn8 = customtkinter.CTkButton(self, text="And", command=lambda: self.button_callback(self.btn8))
        self.btn8.grid(row=2, column=1, padx=(10, 5), pady=(10, 10), sticky="nsew")
        self.btn9 = customtkinter.CTkButton(self, text="XOR", command=lambda: self.button_callback(self.btn9))
        self.btn9.grid(row=2, column=2, padx=(5, 10), pady=(10, 10), sticky="nsew")
        self.btn10 = customtkinter.CTkButton(self, text="Not", command=lambda: self.button_callback(self.btn10))
        self.btn10.grid(row=2, column=3, padx=(0, 20), pady=(10, 10), sticky="nsew")

        self.btn4 = customtkinter.CTkButton(self, text="Umbralizado", command=lambda: self.button_callback(self.btn4))
        self.btn4.grid(row=3, column=0, padx=(20,20), pady=(10,10), sticky="nsew", columnspan=4)
        self.btn5 = customtkinter.CTkButton(self, text="Conversion grises", command=lambda: self.button_callback(self.btn5))
        self.btn5.grid(row=4, column=0, padx=(20,20), pady=(10,20), sticky="nsew", columnspan=4)
        self.btn11 = customtkinter.CTkButton(self, text="Histograma", command=lambda: self.button_callback(self.btn11))
        self.btn11.grid(row=5, column=0, padx=(20,20), pady=(10,20), sticky="nsew", columnspan=4)
        self.btn12 = customtkinter.CTkButton(self, text="Ecualizacion exponencial", command=lambda: self.button_callback(self.btn12))
        self.btn12.grid(row=6, column=0, padx=(20, 20), pady=(10, 20), sticky="nsew", columnspan=4)
        self.btn13 = customtkinter.CTkButton(self, text="Filtro mediana", command=lambda: self.button_callback(self.btn13))
        self.btn13.grid(row=7, column=0, padx=(20, 20), pady=(10, 20), sticky="nsew", columnspan=4)
        self.btn14 = customtkinter.CTkButton(self, text="Filtro Operador de Prewitt", command=lambda: self.button_callback(self.btn14))
        self.btn14.grid(row=8, column=0, padx=(20, 20), pady=(10, 20), sticky="nsew", columnspan=4)
        self.btn15 = customtkinter.CTkButton(self, text="Segmentación completa mediante Multiumbralizacion", command=lambda: self.button_callback(self.btn15))
        self.btn15.grid(row=9, column=0, padx=(20, 20), pady=(10, 20), sticky="nsew", columnspan=4)

    def button_callback(self, btn):
        global btnAnteriorPresionado
        global btnTextoAnteriorPresionado
        global textoBoton
        global ultimoBotonPresionado

        ultimoBotonPresionado = btn

        if procesoDeImagenes.rescalarImagenes[0] is None and procesoDeImagenes.rescalarImagenes[1] is None:
            ventana_flotante(self, "Ingresa al menos una imagen")
            return

        textoBoton = btn.cget("text")

        if textoBoton == "Or" or textoBoton == "And" or textoBoton == "XOR":
            if not (procesoDeImagenes.comprobar_imagen_existe(0) and procesoDeImagenes.comprobar_imagen_existe(1)):
                ventana_flotante(self, "Para esta operacion se necesita ingresar 2 imagenes")
                return

        operaciones()

        if btnAnteriorPresionado is not None and btnTextoAnteriorPresionado is not None:
            auxText = btn.cget("text")
            btnAnteriorPresionado.configure(text=btnTextoAnteriorPresionado)
            btnTextoAnteriorPresionado = auxText

        if btnTextoAnteriorPresionado != "Revertir cambio":
            btnAnteriorPresionado = btn
            btnTextoAnteriorPresionado = btn.cget("text")
            btn.configure(text="Revertir cambio")
        else:
            btnAnteriorPresionado = None
            btnTextoAnteriorPresionado = None


class MyCheckboxFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.boton_cargar = customtkinter.CTkButton(self, text="Seleccionar imagen", command=lambda: self.seleccionar_imagen("img1"))
        self.boton_cargar.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")

        self.boton_cargar1 = customtkinter.CTkButton(self, text="Seleccionar imagen", command=lambda: self.seleccionar_imagen("img2"))
        self.boton_cargar1.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")

        self.boton_quitar_imagen = customtkinter.CTkButton(self, text="Quitar imagen", command=lambda: self.quitar_imagen(0))
        referenciaBotonQuitar[0] = self.boton_quitar_imagen
        self.boton_quitar_imagen1 = customtkinter.CTkButton(self, text="Quitar imagen", command=lambda: self.quitar_imagen(1))
        referenciaBotonQuitar[1] = self.boton_quitar_imagen1
        self.boton_restablecer = customtkinter.CTkButton(self, text="Restablecer", command=lambda: self.restablecer_imagen(0))
        referenciaBotonRestablecer[0] = self.boton_restablecer
        self.boton_restablecer_1 = customtkinter.CTkButton(self, text="Restablecer", command=lambda: self.restablecer_imagen(1))
        referenciaBotonRestablecer[1] = self.boton_restablecer_1



    def seleccionar_imagen(self, destino:str):
        if destino == "img1":
            numeroImagen = 0
        else:
            numeroImagen = 1

        procesoDeImagenes.ruta_imagenes[numeroImagen] = None
        procesoDeImagenes.seleccionar_imagen(numeroImagen)
        procesoDeImagenes.comprobar_imagen_existe_original(numeroImagen)
        if procesoDeImagenes.imagenes[numeroImagen] is not None:
            procesoDeImagenes.rescalarImagenes[numeroImagen] = procesoDeImagenes.reescalar_imagen(procesoDeImagenes.imagenes[numeroImagen])
            if numeroImagen == 0:
                self.boton_quitar_imagen.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="w")
                self.boton_restablecer.grid(row=0, column=2, padx=10, pady=(10, 0), sticky="w")
            if numeroImagen == 1:
                self.boton_quitar_imagen1.grid(row=1, column=1, padx=10, pady=(10, 0), sticky="w")
                self.boton_restablecer_1.grid(row=1, column=2, padx=10, pady=(10, 0), sticky="w")

        procesoDeImagenes.imagenesSeleccionadasMostrar[0] = procesoDeImagenes.rescalarImagenes[0]
        procesoDeImagenes.imagenesSeleccionadasMostrar[1] = procesoDeImagenes.rescalarImagenes[1]

        mostrar_imagenes()

    def quitar_imagen(self, imagen):
        procesoDeImagenes.ruta_imagenes[imagen] = None
        procesoDeImagenes.imagenesSeleccionadasMostrar[imagen] = None
        procesoDeImagenes.imagenesSeleccionadasAnteriorMostrar[imagen] = None
        procesoDeImagenes.rescalarImagenes[imagen] = None
        procesoDeImagenes.imagenes[imagen] = None
        referenciaBotonRestablecer[imagen].grid_remove()
        referenciaBotonQuitar[imagen].grid_remove()
        desactivar_inputs_imagenes()
        mostrar_imagenes()

    def restablecer_imagen(self, imagen):
        global btnAnteriorPresionado
        global btnTextoAnteriorPresionado

        procesoDeImagenes.imagenesSeleccionadasAnteriorMostrar[imagen] = None
        procesoDeImagenes.imagenesSeleccionadasMostrar[imagen] = procesoDeImagenes.rescalarImagenes[imagen]
        desactivar_inputs_imagenes()

        if btnAnteriorPresionado is not None and btnTextoAnteriorPresionado is not None:
            auxText = ultimoBotonPresionado.cget("text")
            btnAnteriorPresionado.configure(text=btnTextoAnteriorPresionado)
            btnTextoAnteriorPresionado = auxText

        if btnTextoAnteriorPresionado == "Revertir cambio":
            btnAnteriorPresionado = None
            btnTextoAnteriorPresionado = None

        mostrar_imagenes()

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Procesamiento de imagenes")
        self.geometry("1000x1000")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=9)
        self.grid_rowconfigure(1, weight=1)

        self.checkbox_frame = MyCheckboxFrame(self)
        self.checkbox_frame.grid(row=0, column=0, padx=(10,5), pady=(10, 5), sticky="nsew")

        self.bttns = btnsFrame(self)
        self.bttns.grid(row=1, column=0, padx=(10,5), pady=(5,10), sticky="nsew")

        self.imageFrame = images(self)
        self.imageFrame.grid(row=0, column=1, padx=(5,10), pady=(10,10), rowspan=2, sticky="nsew")

        referenciaSelf = self

    def button_callback(self):
        print("button pressed")

def ventana_flotante(self, mensaje):
    ventana_flotante = customtkinter.CTkToplevel(self)
    ventana_flotante.geometry("300x200")
    ventana_flotante.title(mensaje)

    etiqueta = customtkinter.CTkLabel(ventana_flotante, text = mensaje)
    etiqueta.pack(pady=20)

    boton_cerrar = customtkinter.CTkButton(ventana_flotante, text="Cerrar", command=ventana_flotante.destroy)
    boton_cerrar.pack(pady=20)

    ventana_flotante.overrideredirect(True)
    ventana_flotante.grab_set()
    self.wait_window(ventana_flotante)

def llamar_operaciones(*args):
    try:
        valor = variableModificar[0].get()

        if procesoDeImagenes.imagenesSeleccionadasAnteriorMostrar[0] is not None:
            procesoDeImagenes.imagenesSeleccionadasMostrar[0] = procesoDeImagenes.imagenesSeleccionadasAnteriorMostrar[0]
            procesoDeImagenes.imagenesSeleccionadasMostrar[1] = procesoDeImagenes.imagenesSeleccionadasAnteriorMostrar[1]

        operaciones()
    except tk.TclError:
        print("JAJA, miren, se murio")

def operaciones():

    if textoBoton == "Segmentación completa mediante Multiumbralizacion":
        referenciaIntroducirDatos[0].configure(textvariable=variableModificarString[0])
        referenciaIntroducirDatos[1].configure(textvariable=variableModificarString[1])
    else:
        referenciaIntroducirDatos[0].configure(textvariable=variableModificar[0])
        referenciaIntroducirDatos[1].configure(textvariable=variableModificar[1])

    if textoBoton == "RGB":
        procesoDeImagenes.mostrar_imagenes_rgb(0)
        procesoDeImagenes.mostrar_imagenes_rgb(1)
        desactivar_inputs_imagenes()
    else:
        if textoBoton == "Suma":
            procesoDeImagenes.operaciones_aritmeticas_imagen(variableModificar[0].get(), 0, 1)
            procesoDeImagenes.operaciones_aritmeticas_imagen(variableModificar[1].get(), 1, 1)
            activar_inputs_imagenes()
        else:
            if textoBoton == "Resta":
                procesoDeImagenes.operaciones_aritmeticas_imagen(variableModificar[0].get(), 0, 2)
                procesoDeImagenes.operaciones_aritmeticas_imagen(variableModificar[1].get(), 1, 2)
                activar_inputs_imagenes()
            else:
                if textoBoton == "Multiplicacion":
                    procesoDeImagenes.operaciones_aritmeticas_imagen(variableModificar[0].get(), 0, 3)
                    procesoDeImagenes.operaciones_aritmeticas_imagen(variableModificar[1].get(), 1, 3)
                    activar_inputs_imagenes()
                else:
                    if textoBoton == "Or":
                        desactivar_inputs_imagenes()
                        procesoDeImagenes.operaciones_logicas_imagenes(1)
                    else:
                        if textoBoton == "And":
                            desactivar_inputs_imagenes()
                            procesoDeImagenes.operaciones_logicas_imagenes(2)
                        else:
                            if textoBoton == "XOR":
                                desactivar_inputs_imagenes()
                                procesoDeImagenes.operaciones_logicas_imagenes(3)
                            else:
                                if textoBoton == "Not":
                                    desactivar_inputs_imagenes()
                                    procesoDeImagenes.operaciones_logicas_imagenes(4)
                                else:
                                    if textoBoton == "Umbralizado":
                                        procesoDeImagenes.umbralizado(0, variableModificar[0].get())
                                        procesoDeImagenes.umbralizado(1, variableModificar[1].get())
                                        activar_inputs_imagenes()
                                    else:
                                        if textoBoton == "Conversion grises":
                                            desactivar_inputs_imagenes()
                                            procesoDeImagenes.conversion_grises(0)
                                            procesoDeImagenes.conversion_grises(1)
                                        else:
                                            if textoBoton == "Histograma":
                                                desactivar_inputs_imagenes()

                                                procesoDeImagenes.comprobar_imagen_existe(0)
                                                procesoDeImagenes.comprobar_imagen_existe(1)

                                                procesoDeImagenes.histogramaPedido = True

                                                procesoDeImagenes.imagenesSeleccionadasMostrar[0] = procesoDeImagenes.histograma(procesoDeImagenes.imagenesSeleccionadasAnteriorMostrar[0])
                                                procesoDeImagenes.imagenesSeleccionadasMostrar[1] = procesoDeImagenes.histograma(procesoDeImagenes.imagenesSeleccionadasAnteriorMostrar[1])
                                            else:
                                                if textoBoton == "Ecualizacion exponencial":
                                                    procesoDeImagenes.comprobar_imagen_existe(0)
                                                    procesoDeImagenes.comprobar_imagen_existe(1)

                                                    procesoDeImagenes.imagenesSeleccionadasMostrar[0] = procesoDeImagenes.ecualizacion_exponencial(procesoDeImagenes.imagenesSeleccionadasAnteriorMostrar[0], variableModificar[0].get())
                                                    procesoDeImagenes.imagenesSeleccionadasMostrar[1] = procesoDeImagenes.ecualizacion_exponencial(procesoDeImagenes.imagenesSeleccionadasAnteriorMostrar[1], variableModificar[1].get())

                                                    activar_inputs_imagenes()
                                                else:
                                                    if textoBoton == "Filtro mediana":

                                                        if (int(variableModificar[0].get()) % 2) != 0 and int(variableModificar[0].get()) > 0:
                                                            procesoDeImagenes.filtro_mediana(0, variableModificar[0].get())
                                                        if (int(variableModificar[1].get()) % 2) != 0 and int(variableModificar[1].get()) > 0:
                                                            procesoDeImagenes.filtro_mediana(1, variableModificar[1].get())
                                                        activar_inputs_imagenes()

                                                    else:
                                                        if textoBoton == "Filtro Operador de Prewitt":
                                                            desactivar_inputs_imagenes()
                                                            procesoDeImagenes.filtro_operador_prewitt(0)
                                                            procesoDeImagenes.filtro_operador_prewitt(1)
                                                        else:
                                                            if textoBoton == "Segmentación completa mediante Multiumbralizacion":
                                                                procesoDeImagenes.filtro_segmentacion_completa_multiumbralizacion(0,variableModificarString[0].get())
                                                                procesoDeImagenes.filtro_segmentacion_completa_multiumbralizacion(1,variableModificarString[1].get())
                                                                activar_inputs_imagenes()
                                                    if textoBoton == "Revertir cambio":
                                                        desactivar_inputs_imagenes()

                                                        procesoDeImagenes.imagenesSeleccionadasMostrar[0] = procesoDeImagenes.imagenesSeleccionadasAnteriorMostrar[0]
                                                        procesoDeImagenes.imagenesSeleccionadasMostrar[1] = procesoDeImagenes.imagenesSeleccionadasAnteriorMostrar[1]

    mostrar_imagenes()

def activar_inputs_imagenes():
    referenciaSelfImages.columnconfigure(1, weight = 1)
    referenciaSelfImages.columnconfigure(2, weight = 1)
    if procesoDeImagenes.imagenesSeleccionadasMostrar[0] is not None:
        referenciaIntroducirLabelDatos[0].grid(row = 0, column = 1)
        referenciaIntroducirDatos[0].grid(row = 0, column = 2)

    if procesoDeImagenes.rescalarImagenes[1] is not None:
        referenciaIntroducirLabelDatos[1].grid(row=1, column=1)
        referenciaIntroducirDatos[1].grid(row=1, column=2)

def desactivar_inputs_imagenes():
    referenciaSelfImages.columnconfigure(1, weight = 0)
    referenciaSelfImages.columnconfigure(2, weight = 0)
    if procesoDeImagenes.imagenesSeleccionadasMostrar[0] is not None:
        referenciaIntroducirDatos[0].grid_remove()
        referenciaIntroducirLabelDatos[0].grid_remove()

    if procesoDeImagenes.rescalarImagenes[1] is not None:
        referenciaIntroducirDatos[1].grid_remove()
        referenciaIntroducirLabelDatos[1].grid_remove()

app = App()
app.mainloop()