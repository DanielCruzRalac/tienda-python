import tkinter as tk
from tkinter import font as tkfont
from services.manipular_sql import manipular
from views.productos_view import cargar_productos  # Importa la función para actualizar lista

def agregar_productos(ventana):
    color_fondo = "#D6D6D6"
    color_etiqueta = "#e6f2ff"
    color_boton = "#4CAF50"
    color_boton_texto = "#ffffff"

    fuente_titulo = tkfont.Font(family="Segoe UI", size=20, weight="bold")
    fuente_label = tkfont.Font(family="Tahoma", size=12)
    fuente_entrada = tkfont.Font(family="Arial", size=12)
    fuente_boton = tkfont.Font(family="Tahoma", size=14, weight="bold")

    panel_izquierdo = tk.Frame(ventana, bg=color_fondo)
    panel_izquierdo.place(relx=0, rely=0, relwidth=0.2, relheight=0.8)

    titulo_izquierdo = tk.Label(panel_izquierdo, text="Agrega tus\nproductos", bg=color_fondo,
                                font=fuente_titulo, anchor="w", justify="left")
    titulo_izquierdo.pack(padx=10, pady=(10, 20), anchor="w")

    # Consulta categorías para llenar el OptionMenu
    categorias = manipular("SELECT id, nombre FROM categorias")
    if not categorias:
        categorias = []
    # Diccionario para mapear nombre a id
    categorias_dict = {nombre: id for id, nombre in categorias}

    campos = [
        ("Nombre del Producto:", "producto"),
        ("Asignar Precio:", "precio"),
        ("Cantidad de Productos:", "cantidad"),
        # La categoría la manejaremos aparte abajo
    ]

    entradas = {}
    for texto, clave in campos:
        etiqueta = tk.Label(panel_izquierdo, text=texto, font=fuente_label,
                            bg=color_etiqueta, anchor="w")
        etiqueta.pack(padx=10, anchor="w")
        entrada = tk.Entry(panel_izquierdo, font=fuente_entrada)
        entrada.pack(padx=10, pady=(0, 10), anchor="w", fill='x')
        entradas[clave] = entrada

    # Agregar etiqueta para categoría
    etiqueta_categoria = tk.Label(panel_izquierdo, text="Selecciona Categoría:", font=fuente_label,
                                  bg=color_etiqueta, anchor="w")
    etiqueta_categoria.pack(padx=10, anchor="w")

    # Variable para guardar selección categoría
    categoria_var = tk.StringVar(panel_izquierdo)
    # Si hay categorías, establecer primera como default, sino vacío
    if categorias:
        categoria_var.set(categorias[0][1])
    else:
        categoria_var.set("")

    optionmenu_categoria = tk.OptionMenu(panel_izquierdo, categoria_var, *[nombre for _, nombre in categorias])
    optionmenu_categoria.config(font=fuente_entrada)
    optionmenu_categoria.pack(padx=10, pady=(0, 10), anchor="w", fill='x')

    # Función para pasar el foco al siguiente Entry o ejecutar el botón
    def avanzar(event, clave_actual):
        claves = list(entradas.keys()) + ["categoria"]
        idx = claves.index(clave_actual)
        if idx < len(claves) - 1:
            siguiente = claves[idx + 1]
            if siguiente == "categoria":
                optionmenu_categoria.focus_set()
            else:
                entradas[siguiente].focus_set()
        else:
            boton_continuar.invoke()  # Ejecuta el comando del botón

    # Asignar evento Enter a cada Entry
    for clave in entradas:
        entradas[clave].bind("<Return>", lambda e, c=clave: avanzar(e, c))

    # Para el OptionMenu, detectamos Enter en su widget subyacente (no tan directo)
    # Mejor agregar botón para continuar, o bind en tecla Return a la ventana si está en OptionMenu
    # Aquí una forma sencilla: bind Return al OptionMenu widget para invocar botón
    optionmenu_categoria.bind("<Return>", lambda e: boton_continuar.invoke())

    def insertar_producto():
        try:
            nombre = entradas["producto"].get()
            precio = float(entradas["precio"].get())
            cantidad = int(entradas["cantidad"].get())
            categoria_nombre = categoria_var.get()
            categoria_id = categorias_dict.get(categoria_nombre)
            if categoria_id is None:
                print("❌ Selecciona una categoría válida.")
                return
        except ValueError:
            print("❌ Precio y cantidad deben ser números válidos.")
            return
        
        sql = """INSERT INTO productos (nombre, precio, cantidad, categoria_id)
                 VALUES (%s, %s, %s, %s)"""
        parametros = (nombre, precio, cantidad, categoria_id)
        filas = manipular(sql, parametros)

        if filas == 1:
            print("✅ Producto insertado correctamente.")
            for entrada in entradas.values():
                entrada.delete(0, tk.END)
            # Reiniciar opción categoría a la primera
            if categorias:
                categoria_var.set(categorias[0][1])
            cargar_productos(ventana)  # Actualiza panel productos
        else:
            print("❌ Error al insertar producto.")

    boton_continuar = tk.Button(panel_izquierdo, text="Continuar", font=fuente_boton,
                                bg=color_boton, fg=color_boton_texto, activebackground="#45a049",
                                bd=0, cursor="hand2", command=insertar_producto)
    boton_continuar.pack(pady=10, fill='x', padx=10)
