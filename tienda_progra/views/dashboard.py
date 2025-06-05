import tkinter as tk
from views.productos_view import cargar_productos
def ventana_usuario(datos):
    venta_usuario = tk.Tk()
    venta_usuario.title("Ventana Usuario")
    venta_usuario.geometry("400x500")


    cargar_productos(venta_usuario)

    venta_usuario.mainloop()