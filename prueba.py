#Importaciones
import tensorflow as tf
import cv2
import numpy as np
import os
import pantalla

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


p1 = pantalla.Pantalla("p1")

p1.setCodigos(codigo)

p1.iniciar()