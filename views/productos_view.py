import tkinter as tk 
from services.my_sql import conectar
def cargar_productos(ventana):
    color_fondo = "Black"
    productos_panel = tk.Frame(
        ventana,
        bg=color_fondo, 
        padx=0, 
        pady=0,
        width=400,
        height=600)
    
    titulo = tk.Label(productos_panel,text="Productos",fg="white",bg=color_fondo,font=("Castelar",14,"bold"))
    titulo.place(x=160,y=0)

    productos_consulta=conectar("SELECT nombre FROM productos")
    productos = ""
    for cada_uno in productos_consulta:
        productos += f"{cada_uno}\n"

    titulo = tk.Label(productos_panel,text=productos,fg="Black",bg="white",font=("Arial",12),justify="left")
    titulo.place(x=10,y=30)



    productos_panel.place(x=0,y=0)
    print("panel productos cargado")