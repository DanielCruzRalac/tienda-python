import tkinter as tk 

def cargar_usuario(ventana):
    login_panel = tk.Frame(
        ventana,
        bg="green",
        padx=0,
        pady=0,
        width=1000,
        height=600
        )
    
    titulo = tk.Label(login_panel, text="Usuario")
    titulo.pack()

    entrada_correo = tk.Entry(login_panel)
    entrada_correo.pack()
 
    titulo = tk.Label(login_panel, text="Contraseña")
    titulo.pack()

    entrada_correo = tk.Entry(login_panel)
    entrada_correo.pack()

    boton = tk.Button(login_panel, text = "Continuar")
    boton.pack()

    login_panel.pack()
    print("Panel login cargado")
