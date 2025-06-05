import tkinter as tk
from services.my_sql import conectar

def cargar_productos(ventana):
    color_fondo = "#1e1e1e"
    color_tarjeta = "#f8f8f8"
    color_borde = "#d1d1d1"
    color_titulo = "#00FFCC"

    productos_panel = tk.Frame(
        ventana,
        bg=color_fondo,
        padx=0,
        pady=0,
        width=400,
        height=600
    )

    # Título con ícono decorativo
    titulo = tk.Label(
        productos_panel,
        text="Lista de Productos",
        fg=color_titulo,
        bg=color_fondo,
        font=("Segoe UI", 16, "bold"),
        anchor="w"
    )
    titulo.place(x=10, y=0)

    # Canvas con scrollbar para scroll
    canvas = tk.Canvas(productos_panel, bg=color_fondo, bd=0, highlightthickness=0, width=380, height=540)
    scrollbar = tk.Scrollbar(productos_panel, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Frame interior para productos
    frame_interno = tk.Frame(canvas, bg=color_fondo)

    # Consulta a la base de datos
    productos_consulta = conectar("SELECT nombre FROM productos")

    for i, producto in enumerate(productos_consulta, start=1):
        texto = f"{i}. {producto[0]}"
        
        # Tarjeta decorativa para cada producto
        tarjeta = tk.Frame(frame_interno, bg=color_tarjeta, bd=1, relief="solid")
        label = tk.Label(
            tarjeta,
            text=texto,
            bg=color_tarjeta,
            fg="#333333",
            font=("Calibri", 12),
            anchor="w",
            padx=10,
            pady=5
        )
        label.pack(fill="x")

        tarjeta.pack(padx=8, pady=4, fill="x")

    # Scroll config
    frame_interno.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=frame_interno, anchor="nw")

    canvas.place(x=10, y=40)
    scrollbar.place(x=380, y=40, height=540)

    productos_panel.place(x=0, y=0)
    print("panel productos cargado")
