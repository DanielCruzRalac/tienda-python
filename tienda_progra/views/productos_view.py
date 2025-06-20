import tkinter as tk
from services.my_sql import conectar
from services.manipular_sql import manipular
from tkinter import messagebox


def cargar_productos(ventana):
    color_fondo = "#1e1e1e"
    color_tarjeta = "#ffffff"
    color_borde = "#cccccc"
    color_titulo = "#FFFFFF"
    color_encabezado = "#333333"
    color_texto = "#000000"

    ventana.update_idletasks()

    productos_panel = tk.Frame(ventana, bg=color_fondo)
    productos_panel.place(relx=0.2, rely=0, relwidth=0.8, relheight=1)

    titulo = tk.Label(productos_panel, text="Lista de Productos",
                      fg=color_titulo, bg=color_fondo, font=("Segoe UI", 18, "bold"), anchor="w")
    titulo.place(relx=0.35, y=10)

    boton_actualizar = tk.Button(productos_panel, text="Actualizar", bg="#007ACC", fg="white",
                                 font=("Segoe UI", 10, "bold"), padx=10, pady=5, command=lambda: actualizar_productos())
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
            nuevo_precio = float(entry_precio.get())
            nueva_cantidad = int(entry_cantidad.get())
            sql = "UPDATE productos SET precio=%s, cantidad=%s WHERE id=%s"
            filas_afectadas = manipular(sql, (nuevo_precio, nueva_cantidad, producto_id))
            if filas_afectadas:
                editor.destroy()
                actualizar_productos()

        def eliminar_producto():
            sql = "DELETE FROM productos WHERE id=%s"
            confirmado = messagebox.askyesno("Eliminar", f"¿Estás seguro de eliminar '{nombre}'?")
            if confirmado:
                manipular(sql, (producto_id,))
                editor.destroy()
                actualizar_productos()

        tk.Button(editor, text="Guardar", bg="green", fg="white", command=guardar_cambios).pack(pady=5)
        tk.Button(editor, text="Eliminar", bg="red", fg="white", command=eliminar_producto).pack()

    def actualizar_productos():
        for widget in frame_interno.winfo_children():
            widget.destroy()

        encabezados = ["Num. Producto", "Nombre", "Precio", "Cantidad", "Categoría"]
        for col, texto in enumerate(encabezados):
            label = tk.Label(frame_interno, text=texto, bg=color_encabezado, fg=color_tarjeta,
                            font=("Segoe UI", 12, "bold"), borderwidth=1, relief="raised", padx=5, pady=5)
            label.grid(row=0, column=col, sticky="nsew", padx=1, pady=1)

        consulta_sql = """
            SELECT p.id, p.nombre, p.precio, p.cantidad, c.nombre 
            FROM productos p 
            LEFT JOIN categorias c ON p.categoria_id = c.id
            ORDER BY p.id
        """
        productos_consulta = conectar(consulta_sql)

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

                # Clic en cualquier celda de la fila → editar producto
                celda.bind("<Button-1>", lambda e, pid=producto_id, nom=nombre, pre=precio, cant=cantidad: abrir_editor(pid, nom, pre, cant))

        for col in range(5):
            frame_interno.grid_columnconfigure(col, weight=1)

    actualizar_productos()
    print("Panel de productos cargado")
