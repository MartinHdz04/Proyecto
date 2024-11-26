#Importaciones
import tensorflow as tf
import cv2
import numpy as np
import os

#Visual
import tkinter as tk
from tkinter import ttk

#Tamaño predeterminado de las imágenes
TAMANO_IMG = 224

#Función para redimensionar una imágen y garantizar que tiene 3 canales
def preprocess_input(input_image):
    # Redimensionar la imagen
    imagen = cv2.resize(input_image, (TAMANO_IMG, TAMANO_IMG))
    # Asegurarse de que la imagen tenga tres canales (color)
    if len(imagen.shape) == 2:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_GRAY2RGB)
    elif imagen.shape[2] == 1:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_GRAY2RGB)
    # Expandir las dimensiones para que sea compatible con el modelo
    imagen = imagen.reshape(1, TAMANO_IMG, TAMANO_IMG, 3)
    return imagen

#Función para redimensionar una imágen y garantizar que tiene 3 canales
def preprocess_input1(input_image1):
    imagen = cv2.resize(input_image1, (TAMANO_IMG, TAMANO_IMG))
    imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    imagen = imagen.reshape(1, TAMANO_IMG, TAMANO_IMG, 3)
    imagen = tf.keras.applications.mobilenet_v2.preprocess_input(imagen)
    return imagen

######   Variables ######
#Matriz de resultado
resultado = []

#Matriz mostrar
mostrar = []

#Nuestros posibles resultados
labels = ['aguacate', 'alverja', 'arroz', 'cebollaBlanca', 'cebollaMorada', 'chile', 'chontaduro', 'cilantro', 'coco', 'garbanzo', 'guanabana', 'guatila', 'lima', 'limon', 'MangoAzucar', 'mangoHilacha', 'mangoKeitt', 'mangoTommy', 'mangoYulima', 'mazorca', 'moriche', 'papaCriolla', 'papaPastusa', 'papaSabanera', 'papaya', 'pimentonAmarillo', 'pimentonRojo', 'pimentonVerde', 'platanoVerde', 'remolacha', 'sandia', 'tomateDeArbol', 'uvas', 'yuca']

#Codigo de referencia de cada producto que se agrega al final
codigo = []

productosTotales = {'MangoAzucar': 1234, 'guatila': 5678, 'mangoHilacha': 9012,
                     'mangoKeitt': 2468, 'mangoTommy': 1357, 'mangoYulima': 2461,
                       'papaCriolla': 2462, 'papaPastusa': 2463, 'papaSabanera': 2464,
                         'papaya': 2465, 'sandia': 2466, 'yuca': 2467, 'Granny_Smith': 2469,
                           'pineapple': 2460, 'lemon': 2161, 'banana': 2262, 'strawberry': 2363,
                           'pomegranate': 2362, 'orange': 2762}

# Cargar el modelo desde el archivo .h5
model = tf.keras.models.load_model('modelos/MimodelFruver6.h5')

# ahora hacer prediccion con el modelo MobileNetV2 y mostrar el top 2
model1 = tf.keras.applications.MobileNetV2()

#Model: Nuestro ----- Model1:MoibileNet o global

#Ruta de imágen prueba
image_path = "imagenes/banano.jpg"

# Verificar si el archivo de la imagen existe
if not os.path.isfile(image_path):
    raise FileNotFoundError(f"No se pudo encontrar el archivo: {image_path}")

#Imágen de prueba
input_image = cv2.imread(image_path)

# Verificar si la imagen se leyó correctamente
if input_image is None:
    raise ValueError(f"No se pudo leer la imagen en la ruta: {image_path}")


# #Que la imagen venga de la camara
# cap = cv2.VideoCapture(0)
# ret, input_image = cap.read()
# cv2.imshow('imagen', input_image)
# cap.release()

#Redimensionas con ambas funciones
input_image_preprocessed = preprocess_input(input_image)
input_image_preprocessed1 = preprocess_input1(input_image)

# Realizar la inferencia con el modelo cargado
predictions = model.predict(input_image_preprocessed)
predictions1 = model1.predict(input_image_preprocessed1)

# Decodificar las predicciones del modelo global, además escogemos las 2 mejores predicciones
decoded_predictions1 = tf.keras.applications.imagenet_utils.decode_predictions(predictions1, top=2)[0]

##### Mostrar el porcentaje de todas las clases ####

#Añade a resultado las coincidencias que encuentra nuestro modelos en nuestros posibles resultados
for i, label in enumerate(labels):
    resultado.append(predictions[0][i])
    
# Toma la posicion de los numeros más altos en resultado
posicion1 = resultado.index(max(resultado))
# Resultado más probable de nuestro modelo
score1 = predictions[0][posicion1] 

#Poner en cero la primera posición para encontrar la segunda más probable
resultado[posicion1] = 0

# Posición del segundo resultado más probable
posicion2 = resultado.index(max(resultado))
# Segundo resultado más probable
score2 = predictions[0][posicion2]  # score de la clase predicha

#Añade a la matriz de mostrar:
#En primer lugar los dos nombres de los resultados más cercanos de nuestro modela
#En segundo lugar los dos valores más probables del modelo global
mostrar.append((labels[posicion1],score1))
mostrar.append((labels[posicion2],score2))
mostrar.append((decoded_predictions1[0][1],decoded_predictions1[0][2]))
mostrar.append((decoded_predictions1[1][1],decoded_predictions1[1][2]))

print('\nlas opciones más probables son:\n')

# ordenar de mayor a menor segun el score
mostrar.sort(key=lambda x: x[1], reverse=True)

#Agrega los códigos de los productos, e imprime los resultados
for i in mostrar:
    # si el producto no esta en el diccionario no lo agrega
    if i[0] in productosTotales:
        codigo.append(productosTotales[i[0]])
    print(f'{i[0]} con {i[1] * 100:.2f}%')

#Imprime la referencia de inventario
print(f'Estos son los codigos de los productos: {codigo}')






#Lista de los productos que estarán en pantalla
mostrarProdPant = []

# Crear la ventana principal
ventana = tk.Tk()

#Le añadimos un título
ventana.title("Productos a comprar")

#Añadimos un tamaño
espacio_frame = tk.Frame(ventana, height=12)
espacio_frame.pack()

#Matriz de productos
productos = []

# Crear la lista de datos
# datos1 = [[1234, "Dato 222", 1000],
#          [5678, "Dato B", 2000],
#          [9012, "Dato Y", 3000],
#          [2468, "Dato", 4000]]

# crear la lista de datos con frutas y verduras esta lista debe tener el mismo formato que la lista de datos1
datos = [[1234, "mango Azucar", 1000],
         [5678, "guatila", 2000],
         [9012, "mango Hilacha", 3000],
         [2468, "mango Keitt", 4000],
         [1357, "mango Tommy", 5000],
         [2461, "mango Yulima", 6000],
         [2462, "papa Criolla", 7000],
         [2463, "papa Pastusa", 8000],
         [2464, "papa Sabanera", 9000],
         [2465, "papaya", 10000],
         [2466, "sandia", 11000],
         [2467, "yuca", 12000],
         [2469, "manzana verde", 12000],
         [2460, "pinia", 13000],
         [2161, "limon", 14000],
         [2262, "banano", 15000],
         [2363, "fresa", 16000],
         [2362, "granada", 17000],
         [2762, "naranja", 18000]]

# agregar a mostrarProdPant los datos que tienen los codigos de los productos
for i in codigo:
    for j in datos:
        if i == j[0]:
            mostrarProdPant.append(j)

print(f'Estos son los productos a mostrar en la pantalla: {mostrarProdPant}')



# Crear la lista seleccionable
lista = tk.Listbox(ventana)
lista.pack()

#definir anchura y altura de la lista
lista.config(width=150, height=7)

# Agregar encabezado a la lista seleccionable con el primer elemento al lado izquierdo, el segundo al centro y el tercero al lado derecho y que no se pueda seleccionar
lista.insert(tk.END, f"   {'Código':<120}{'Nombre':^20}{'PrecioXlibra':>120}")
lista.itemconfig(0, {"bg": "lightgrey"})

# Agregar una línea divisoria
lista.insert(tk.END, "-" * 260)


# Agregar los datos a la lista seleccionable con el primer elemento de cada lista al lado izquierdo con un poco de espacio entre la ventana y el inicio del texto, el segundo al centro y el tercero al lado derecho
espacios = 0

#Añadimos los productos a la lista que se va a ver en pantalla
for dato in mostrarProdPant:
    espacios = (len(dato[1])-6)*2
    lista.insert(tk.END, f"   {dato[0]:<130}{dato[1]}{dato[2]:>{130 - espacios}}")


# Función para obtener el dato seleccionado
def obtener_dato_seleccionado(event):
    #El valor de la selección en la lista
    seleccion = lista.curselection()

    if seleccion:
        indice = seleccion[0]
        dato_seleccionado = lista.get(indice)
        print("Dato seleccionado:", dato_seleccionado.split())
        codigo_producto = dato_seleccionado.split()[0]  # Obtener el código del producto
        codigo_entry.delete(0, tk.END)  # Borrar el contenido actual del Entry widget
        codigo_entry.insert(0, codigo_producto)  # Insertar el código del producto en el Entry widget

        nombre_producto = dato_seleccionado.split()[1]  # Obtener el código del producto
        if len(dato_seleccionado.split()) > 3:
            nombre_producto = nombre_producto + " " + dato_seleccionado.split()[2]
        nombre_entry.delete(0, tk.END)  # Borrar el contenido actual del Entry widget
        nombre_entry.insert(0, nombre_producto)  # Insertar el código del producto en el Entry widget

        costo_producto = dato_seleccionado.split()[2]  # Obtener el código del producto
        if len(dato_seleccionado.split()) > 3:
            costo_producto = dato_seleccionado.split()[3]
        costo_entry.delete(0, tk.END)  # Borrar el contenido actual del Entry widget
        costo_entry.insert(0, costo_producto)  # Insertar el código del producto en el Entry widget

# Asociar el evento <<ListboxSelect>> a la función obtener_dato_seleccionado
lista.bind("<<ListboxSelect>>", obtener_dato_seleccionado)

#Redimensionamos la pantalla
espacio_frame = tk.Frame(ventana, height=15)
espacio_frame.pack()

# Agregar editText para el codigo
codigo_frame = tk.Frame(ventana)
codigo_label = tk.Label(codigo_frame, text="Codigo", anchor="e")
codigo_entry = tk.Entry(codigo_frame)
codigo_label.pack(side="left")
codigo_entry.pack()
codigo_frame.pack()

# Configurar el ancho del código Entry widget para que coincida con el ancho de la lista seleccionable
codigo_entry.config(width=120)

# Agregar espacio entre el código y el nombre
espacio_frame = tk.Frame(ventana, height=15)
espacio_frame.pack()

# Agregar editText para el nombre
nombre_frame = tk.Frame(ventana)
nombre_label = tk.Label(nombre_frame, text="Producto", anchor="e")
nombre_entry = tk.Entry(nombre_frame)
nombre_label.pack(side="left")
nombre_entry.pack()
nombre_frame.pack()

# Configurar el ancho del nombre Entry widget para que coincida con el ancho de la lista seleccionable
nombre_entry.config(width=120)

espacio_frame = tk.Frame(ventana, height=15)
espacio_frame.pack()

# Agregar editText para el peso y el costo por libra
peso_frame = tk.Frame(ventana)
peso_label = tk.Label(peso_frame, text="Peso", anchor="e")
peso_entry = tk.Entry(peso_frame)
# Configurar el ancho del peso Entry widget para que coincida con el ancho de la lista seleccionable
peso_entry.config(width=120)

# Función para validar la entrada del peso
def validar_peso(input):
    if input.isdigit():
        calcular_subtotal(int(input))  # Calcular el subtotal al ingresar un peso válido
        return True
    elif input == "":
        calcular_subtotal(0)  # Calcular el subtotal al dejar el campo de peso vacío
        return True
    else:
        return False

# Configurar la validación de la entrada del peso
validar_peso = ventana.register(validar_peso)
peso_entry.config(validate="key", validatecommand=(validar_peso, "%P"))

peso_label.pack(side="left")
peso_entry.pack(side="left")  # Place the entry widget on the right side of the label

def calcular_subtotal(peso):
    costo = float(costo_entry.get())
    subtotal = peso * costo
    subtotal_value.config(text=f"{subtotal:.2f}")

# Función para obtener el dato seleccionado
def obtener_dato_seleccionado(event):
    seleccion = lista.curselection()
    if seleccion:
        indice = seleccion[0]
        dato_seleccionado = lista.get(indice)
        print("Dato seleccionado:", dato_seleccionado.split())
        codigo_producto = dato_seleccionado.split()[0]  # Obtener el código del producto
        codigo_entry.delete(0, tk.END)  # Borrar el contenido actual del Entry widget
        codigo_entry.insert(0, codigo_producto)  # Insertar el código del producto en el Entry widget

        nombre_producto = dato_seleccionado.split()[1]  # Obtener el código del producto
        if len(dato_seleccionado.split()) > 3:
            nombre_producto = nombre_producto + " " + dato_seleccionado.split()[2]
        nombre_entry.delete(0, tk.END)  # Borrar el contenido actual del Entry widget
        nombre_entry.insert(0, nombre_producto)  # Insertar el código del producto en el Entry widget

        costo_producto = dato_seleccionado.split()[2]  # Obtener el código del producto
        if len(dato_seleccionado.split()) > 3:
            costo_producto = dato_seleccionado.split()[3]
        costo_entry.delete(0, tk.END)  # Borrar el contenido actual del Entry widget
        costo_entry.insert(0, costo_producto)  # Insertar el código del producto en el Entry widget
        calcular_subtotal(int(peso_entry.get()))  # Calcular el subtotal al seleccionar un dato

# Asociar el evento <<ListboxSelect>> a la función obtener_dato_seleccionado
lista.bind("<<ListboxSelect>>", obtener_dato_seleccionado)

# Agregar espacio entre el peso y el costo
# espacio_frame = tk.Frame(ventana, height=15)
# espacio_frame.pack()

costo_frame = tk.Frame(ventana)
costo_label = tk.Label(costo_frame, text="Costo por libra", anchor="e")
costo_entry = tk.Entry(costo_frame)
# Configurar el ancho del costo Entry widget para que coincida con el ancho de la lista seleccionable
costo_entry.config(width=120)

costo_label.pack(side="left")
costo_entry.pack(side="right")  # Place the entry widget on the right side of the label

peso_frame.pack()
# Agregar espacio entre el peso y el costo
espacio_frame = tk.Frame(ventana, height=15)
espacio_frame.pack()
costo_frame.pack()

# Agregar espacio entre el subtotal y el botón de añadir
espacio_frame = tk.Frame(ventana, height=15)
espacio_frame.pack()

def calcular_total(productos):
    total = 0
    if len(productos) != 0:
        for i in productos:
            valor = int(i[2])*int(i[3])
            total += valor         
    return total


def agregar_producto():
    codigo = codigo_entry.get()
    producto = nombre_entry.get()
    peso = peso_entry.get()
    costo = costo_entry.get()

    # Validar que todos los campos estén completos
    if codigo and producto and peso and costo:
        # Agregar el producto a la lista de datos
        productos.append([codigo, producto, peso, costo])
        print(f'Esto son producto {productos}')

        # # Actualizar la lista seleccionable con el nuevo producto
        # espacios = (len(producto)-6)*2
        # lista.insert(tk.END, f"   {codigo:<130}{producto}{peso:>{130 - espacios}}{costo}")
        
        # Limpiar los campos de entrada
        codigo_entry.delete(0, tk.END)
        nombre_entry.delete(0, tk.END)
        peso_entry.delete(0, tk.END)
        costo_entry.delete(0, tk.END)
        
        # Actualizar el subtotal
        total = calcular_total(productos)

        total_value.config(text=f"{total}")
    else:
        print("Por favor complete todos los campos")

# # Agregar botón para añadir el producto
# add_button = tk.Button(ventana, text="Añadir Producto")
# add_button.pack()

# agregar panel donde se visualiza el subtotal
subtotal_frame = tk.Frame(ventana)
subtotal_label = tk.Label(subtotal_frame, text="Subtotal", anchor="e")
subtotal_value = tk.Label(subtotal_frame, text="0.00")
subtotal_label.pack(side="left")
subtotal_value.pack(side="right")  # Place the entry widget on the right side of the label
subtotal_frame.pack()

# Agregar el botón de agregar producto
add_button = tk.Button(ventana, text="Añadir Producto", command=agregar_producto)
add_button.pack()

# agregar panel donde se visualiza el subtotal
total_frame = tk.Frame(ventana)
total_label = tk.Label(total_frame, text="Total", anchor="e")
total_value = tk.Label(total_frame, text="0.00")
total_label.pack(side="left")
total_value.pack(side="right")  # Place the entry widget on the right side of the label
total_frame.pack()


# Iniciar el bucle de eventos
ventana.mainloop()
