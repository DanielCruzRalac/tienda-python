import tkinter as tk
from views.productos_view import cargar_productos
from views.agregar_prod import agregar_productos

def ventana_usuario(datos):
    venta_usuario = tk.Tk()
    venta_usuario.title("Ventana Usuario")
    venta_usuario.state('zoomed')  # Maximiza ventana (Windows)

    # Panel superior con botón de actualización general
    panel_superior = tk.Frame(venta_usuario, bg="#e0e0e0")
    panel_superior.place(relx=0, rely=0, relwidth=1, relheight=0.05)

    def actualizar_ventana():
        for widget in venta_usuario.winfo_children():
            if isinstance(widget, tk.Frame) and widget != panel_superior:
                widget.destroy()
        cargar_productos(venta_usuario)
        agregar_productos(venta_usuario)

    boton_actualizar = tk.Button(
        panel_superior,
        text="Actualizar ventana",
        command=actualizar_ventana,
        bg="#2196F3",
        fg="white",
        font=("Segoe UI", 10, "bold")
    )
    boton_actualizar.pack(padx=10, pady=5, side="left")

    # Cargar paneles principales
    cargar_productos(venta_usuario)
    agregar_productos(venta_usuario)

    venta_usuario.mainloop()
