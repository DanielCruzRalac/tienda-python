import tkinter as tk 
from views.header_view import cargar_header
from views.productos_view import cargar_productos
from views.login_view import *
from views.login_view import cargar_login
from views.dashboard import cargar_productos

ventana = tk.Tk()
ventana.title("Mi tienda")
ventana.geometry("500x300")

cargar_login(ventana)

ventana. mainloop()
#USUARIO para puruebas : juan.perez@email.com ,contraseña: 123456   


