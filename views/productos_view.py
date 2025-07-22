import tkinter as tk
from tkinter import ttk
from services.my_sql import conectar
from services.manipular_sql import manipular
from tkinter import messagebox
from tkinter import font as tkfont  # Importa tkfont para fuentes


def cargar_productos(ventana, campo_filtro=None, texto_filtro=None):
    color_fondo = "#1e1e1e"
    color_tarjeta = "#ffffff"
    color_borde = "#cccccc"
    color_titulo = "#FFFFFF"
    color_encabezado = "#333333"
    color_texto = "#000000"

    ventana.update_idletasks()

    # Antes de crear un nuevo panel, buscar y destruir el anterior (si existe)
    for widget in ventana.place_slaves():
        # Identifica el panel productos por relx=0.2
        if isinstance(widget, tk.Frame) and widget.place_info().get("relx") == '0.2':
            widget.destroy()

    # Crear el panel productos_panel (derecha 80%)
    productos_panel = tk.Frame(ventana, bg=color_fondo)
    productos_panel.place(relx=0.2, rely=0, relwidth=0.8, relheight=1)

    titulo = tk.Label(productos_panel, text="Lista de Productos",
                      fg=color_titulo, bg=color_fondo, font=("Segoe UI", 18, "bold"), anchor="w")
    titulo.place(relx=0.35, y=10)

    boton_actualizar = tk.Button(productos_panel, text="Actualizar", bg="#007ACC", fg="white",
                                 font=("Segoe UI", 10, "bold"), padx=10, pady=5,
                                 command=lambda: cargar_productos(ventana, campo_filtro, texto_filtro))
    boton_actualizar.place(relx=0.85, y=10)

    canvas = tk.Canvas(productos_panel, bg=color_fondo, bd=0, highlightthickness=0)
    scrollbar = tk.Scrollbar(productos_panel, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.place(relx=0.025, rely=0.1, relwidth=0.94, relheight=0.85)
    scrollbar.place(relx=0.97, rely=0.1, relheight=0.85)

    frame_interno = tk.Frame(canvas, bg=color_fondo)
    canvas_window = canvas.create_window((0, 0), window=frame_interno, anchor="nw", tags="frame_interno")

    def ajustar_ancho(event):
        canvas.itemconfig("frame_interno", width=event.width)
    canvas.bind("<Configure>", ajustar_ancho)

    frame_interno.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    def abrir_editor(producto_id, nombre, precio, cantidad):
        editor = tk.Toplevel(ventana)
        editor.title(f"Editar: {nombre}")
        editor.geometry("300x200")
        editor.config(bg="#f0f0f0")

        tk.Label(editor, text=f"Producto: {nombre}", bg="#f0f0f0").pack(pady=5)
        tk.Label(editor, text="Precio (Q):").pack()
        entry_precio = tk.Entry(editor)
        entry_precio.insert(0, str(precio))
        entry_precio.pack()

        tk.Label(editor, text="Cantidad:").pack()
        entry_cantidad = tk.Entry(editor)
        entry_cantidad.insert(0, str(cantidad))
        entry_cantidad.pack()

        def guardar_cambios():
            try:
                nuevo_precio = float(entry_precio.get())
                nueva_cantidad = int(entry_cantidad.get())
            except ValueError:
                messagebox.showerror("Error", "Precio y cantidad deben ser números válidos.")
                return
            sql = "UPDATE productos SET precio=%s, cantidad=%s WHERE id=%s"
            filas_afectadas = manipular(sql, (nuevo_precio, nueva_cantidad, producto_id))
            if filas_afectadas:
                editor.destroy()
                cargar_productos(ventana, campo_filtro, texto_filtro)

        def eliminar_producto():
            sql = "DELETE FROM productos WHERE id=%s"
            confirmado = messagebox.askyesno("Eliminar", f"¿Estás seguro de eliminar '{nombre}'?")
            if confirmado:
                manipular(sql, (producto_id,))
                editor.destroy()
                cargar_productos(ventana, campo_filtro, texto_filtro)

        tk.Button(editor, text="Guardar", bg="green", fg="white", command=guardar_cambios).pack(pady=5)
        tk.Button(editor, text="Eliminar", bg="red", fg="white", command=eliminar_producto).pack()

    # Títulos de columnas
    encabezados = ["Num. Producto", "Nombre", "Precio", "Cantidad", "Categoría"]

    # Mostrar encabezados
    for col, texto in enumerate(encabezados):
        label = tk.Label(frame_interno, text=texto, bg=color_encabezado, fg=color_tarjeta,
                         font=("Segoe UI", 12, "bold"), borderwidth=1, relief="raised", padx=5, pady=5)
        label.grid(row=0, column=col, sticky="nsew", padx=1, pady=1)

    # SQL base
    consulta_sql = """
        SELECT p.id, p.nombre, p.precio, p.cantidad, c.nombre 
        FROM productos p 
        LEFT JOIN categorias c ON p.categoria_id = c.id
    """

    parametros = ()
    if campo_filtro and texto_filtro and texto_filtro.strip() != "":
        campo_bd_map = {
            "Nombre": "p.nombre",
            "Precio": "p.precio",
            "Cantidad": "p.cantidad",
            "Categoría": "c.nombre"
        }
        columna = campo_bd_map.get(campo_filtro)
        if columna:
            if campo_filtro in ["Precio", "Cantidad"]:
                consulta_sql += f" WHERE {columna} = %s "
                try:
                    if campo_filtro == "Precio":
                        val = float(texto_filtro)
                    else:
                        val = int(texto_filtro)
                    parametros = (val,)
                except ValueError:
                    parametros = ("-1",)
            else:
                consulta_sql += f" WHERE {columna} LIKE %s "
                parametros = (f"%{texto_filtro}%",)
    consulta_sql += " ORDER BY p.id"

    productos_consulta = conectar(consulta_sql, parametros)

    for index, producto in enumerate(productos_consulta, start=1):
        producto_id = producto[0]
        nombre = producto[1]
        precio = producto[2]
        cantidad = producto[3]
        categoria = producto[4] if producto[4] else "Sin categoría"

        datos = [
            str(index),
            nombre,
            f"Q {precio:.2f}",
            str(cantidad),
            categoria
        ]

        for col, texto in enumerate(datos):
            celda = tk.Label(frame_interno, text=texto, bg=color_tarjeta, fg=color_texto,
                             font=("Segoe UI", 11), borderwidth=1, relief="solid", padx=5, pady=5)
            celda.grid(row=index, column=col, sticky="nsew", padx=1, pady=1)

            celda.bind("<Button-1>", lambda e, pid=producto_id, nom=nombre, pre=precio, cant=cantidad: abrir_editor(pid, nom, pre, cant))

    for col in range(5):
        frame_interno.grid_columnconfigure(col, weight=1)

    return productos_panel


def crear_panel_buscador(ventana, actualizar_productos_func):
    """
    Crea un panel en la parte vacía (izquierda arriba) con
    combobox para seleccionar campo, entry para texto, y botón buscar.
    Al hacer búsqueda llama actualizar_productos_func(campo, texto)
    """

    color_fondo = "#D6D6D6"
    color_etiqueta = "#e6f2ff"
    color_boton = "#4CAF50"
    color_boton_texto = "#ffffff"
    fuente_label = tkfont.Font(family="Tahoma", size=12)
    fuente_entrada = tkfont.Font(family="Arial", size=12)
    fuente_boton = tkfont.Font(family="Tahoma", size=14, weight="bold")

    panel_buscador = tk.Frame(ventana, bg=color_fondo)
    panel_buscador.place(relx=0, rely=0.7, relwidth=0.2, relheight=0.3)

    encabezados_busqueda = ["Nombre", "Precio", "Cantidad", "Categoría"]

    etiqueta_campo = tk.Label(panel_buscador, text="Campo a buscar:", font=fuente_label,
                             bg=color_etiqueta, anchor="w")
    etiqueta_campo.pack(padx=10, pady=(10, 2), anchor="w")

    campo_var = tk.StringVar(panel_buscador)
    campo_var.set(encabezados_busqueda[0])

    combo_campo = ttk.Combobox(panel_buscador, textvariable=campo_var, values=encabezados_busqueda,
                              state="readonly", font=fuente_entrada)
    combo_campo.pack(padx=10, pady=(0, 10), anchor="w", fill='x')

    etiqueta_texto = tk.Label(panel_buscador, text="Texto de búsqueda:", font=fuente_label,
                             bg=color_etiqueta, anchor="w")
    etiqueta_texto.pack(padx=10, pady=(0, 2), anchor="w")

    texto_var = tk.StringVar()
    entry_texto = tk.Entry(panel_buscador, textvariable=texto_var, font=fuente_entrada)
    entry_texto.pack(padx=10, pady=(0, 10), anchor="w", fill='x')

    def on_enter(event):
        boton_buscar.invoke()

    combo_campo.bind("<Return>", on_enter)
    combo_campo.bind("<Down>", lambda e: combo_campo.event_generate('<Button-1>'))
    entry_texto.bind("<Return>", on_enter)

    boton_buscar = tk.Button(panel_buscador, text="Buscar", font=fuente_boton,
                             bg=color_boton, fg=color_boton_texto, activebackground="#45a049",
                             bd=0, cursor="hand2",
                             command=lambda: actualizar_productos_func(campo_var.get(), texto_var.get()))
    boton_buscar.pack(padx=10, pady=10, fill='x')

    return panel_buscador
