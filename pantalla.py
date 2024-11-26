#Importaciones
import tkinter as tk
from tkinter import ttk


class Pantalla():
    #Lista de los productos que estarán en pantalla
    mostrarProdPant = []
    #Matriz de productos finales de compra
    productos = []
    #Matriz de códigos de los productos
    codigo = []

    # Crear la ventana principal
    ventana = tk.Tk()
    #Le añadimos un título
    ventana.title("Productos a comprar")
    #Añadimos un tamaño
    espacio_frame = tk.Frame(ventana, height=15)
    espacio_frame.pack()

    

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
            Pantalla.calcular_subtotal(int(input))  # Calcular el subtotal al ingresar un peso válido
            return True
        elif input == "":
            Pantalla.calcular_subtotal(0)  # Calcular el subtotal al dejar el campo de peso vacío
            return True
        else:
            return False

    # Configurar la validación de la entrada del peso
    validar_peso = ventana.register(validar_peso)
    peso_entry.config(validate="key", validatecommand=(validar_peso, "%P"))
    peso_label.pack(side="left")
    peso_entry.pack(side="left")  # Place the entry widget on the right side of the label

    # Agregar espacio entre el peso y el costo
    espacio_frame = tk.Frame(ventana, height=15)
    espacio_frame.pack()

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

    def agregar_producto():
        codigo = Pantalla.codigo_entry.get()
        producto = Pantalla.nombre_entry.get()
        peso = Pantalla.peso_entry.get()
        costo = Pantalla.costo_entry.get()

        # Validar que todos los campos estén completos
        if codigo and producto and peso and costo:
            # Agregar el producto a la lista de datos
            Pantalla.productos.append([codigo, producto, peso, costo])
            print(f'Esto son producto {Pantalla.productos}')

            # # Actualizar la lista seleccionable con el nuevo producto
            # espacios = (len(producto)-6)*2
            # lista.insert(tk.END, f"   {codigo:<130}{producto}{peso:>{130 - espacios}}{costo}")
            
            # Limpiar los campos de entrada
            Pantalla.codigo_entry.delete(0, tk.END)
            Pantalla.nombre_entry.delete(0, tk.END)
            Pantalla.peso_entry.delete(0, tk.END)
            Pantalla.costo_entry.delete(0, tk.END)
            
            # Actualizar el subtotal
            total = Pantalla.calcular_total(Pantalla.productos)

            Pantalla.total_value.config(text=f"{total}")
        else:
            print("Por favor complete todos los campos")

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


    def setCodigos(self, codigos):
        Pantalla.codigo = codigos


    # Función para obtener el dato seleccionado
    def obtener_dato_seleccionado(event):
        #El valor de la selección en la lista
        seleccion = Pantalla.lista.curselection()

        if seleccion:
            indice = seleccion[0]
            dato_seleccionado = Pantalla.lista.get(indice)
            print("Dato seleccionado:", dato_seleccionado.split())
            codigo_producto = dato_seleccionado.split()[0]  # Obtener el código del producto
            Pantalla.codigo_entry.delete(0, tk.END)  # Borrar el contenido actual del Entry widget
            Pantalla.codigo_entry.insert(0, codigo_producto)  # Insertar el código del producto en el Entry widget

            nombre_producto = dato_seleccionado.split()[1]  # Obtener el código del producto
            if len(dato_seleccionado.split()) > 3:
                nombre_producto = nombre_producto + " " + dato_seleccionado.split()[2]
            Pantalla.nombre_entry.delete(0, tk.END)  # Borrar el contenido actual del Entry widget
            Pantalla.nombre_entry.insert(0, nombre_producto)  # Insertar el código del producto en el Entry widget

            costo_producto = dato_seleccionado.split()[2]  # Obtener el código del producto
            if len(dato_seleccionado.split()) > 3:
                costo_producto = dato_seleccionado.split()[3]
            Pantalla.costo_entry.delete(0, tk.END)  # Borrar el contenido actual del Entry widget
            Pantalla.costo_entry.insert(0, costo_producto)  # Insertar el código del producto en el Entry widget

    # Asociar el evento <<ListboxSelect>> a la función obtener_dato_seleccionado
    lista.bind("<<ListboxSelect>>", obtener_dato_seleccionado)

    # Función para validar la entrada del peso
    def validar_peso(input):
        if input.isdigit():
            Pantalla.calcular_subtotal(int(input))  # Calcular el subtotal al ingresar un peso válido
            return True
        elif input == "":
            Pantalla.calcular_subtotal(0)  # Calcular el subtotal al dejar el campo de peso vacío
            return True
        else:
            return False

    #Función para calcular el subtotal
    def calcular_subtotal(peso):
        costo = float(Pantalla.costo_entry.get())
        subtotal = peso * costo
        Pantalla.subtotal_value.config(text=f"{subtotal:.2f}")

    # Función para obtener el dato seleccionado
    def obtener_dato_seleccionado(event):
        seleccion = Pantalla.lista.curselection()
        if seleccion:
            indice = seleccion[0]
            dato_seleccionado = Pantalla.lista.get(indice)
            print("Dato seleccionado:", dato_seleccionado.split())
            codigo_producto = dato_seleccionado.split()[0]  # Obtener el código del producto
            Pantalla.codigo_entry.delete(0, tk.END)  # Borrar el contenido actual del Entry widget
            Pantalla.codigo_entry.insert(0, codigo_producto)  # Insertar el código del producto en el Entry widget

            nombre_producto = dato_seleccionado.split()[1]  # Obtener el código del producto
            if len(dato_seleccionado.split()) > 3:
                nombre_producto = nombre_producto + " " + dato_seleccionado.split()[2]
            Pantalla.nombre_entry.delete(0, tk.END)  # Borrar el contenido actual del Entry widget
            Pantalla.nombre_entry.insert(0, nombre_producto)  # Insertar el código del producto en el Entry widget

            costo_producto = dato_seleccionado.split()[2]  # Obtener el código del producto
            if len(dato_seleccionado.split()) > 3:
                costo_producto = dato_seleccionado.split()[3]
            Pantalla.costo_entry.delete(0, tk.END)  # Borrar el contenido actual del Entry widget
            Pantalla.costo_entry.insert(0, costo_producto)  # Insertar el código del producto en el Entry widget
            Pantalla.calcular_subtotal(int(Pantalla.peso_entry.get()))  # Calcular el subtotal al seleccionar un dato

    # Asociar el evento <<ListboxSelect>> a la función obtener_dato_seleccionado
    lista.bind("<<ListboxSelect>>", obtener_dato_seleccionado)

    #Función para calcular el total
    def calcular_total(productos):
        total = 0
        if len(productos) != 0:
            for i in productos:
                valor = int(i[2])*int(i[3])
                total += valor         
        return total

    def iniciar(self):
        # Iniciar el bucle de eventos
        Pantalla.ventana.mainloop()

    def __init__(self, name):
        self.name = name
