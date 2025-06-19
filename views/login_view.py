import tkinter as tk 
from services.my_sql import conectar
from views.dashboard import ventana_usuario
tamano_wi = 500
tamano_he = 300
def cargar_login(ventana):
    # Panel principal
    login_panel = tk.Frame(
        ventana,
        bg="#e6f2ff",     # Azul claro
        padx=40,
        pady=40,
        width=tamano_wi,
        height=tamano_he


    )
    login_panel.pack(expand=True)

    # Título
    titulo = tk.Label(
        login_panel,
        text="Inicio de Sesión",
        font=("Arial", 24, "bold"),
        bg="#e6f2ff",
        fg="#003366"
    )
    titulo.pack(pady=(0, 20))

    # Etiqueta correo
    txt_correo = tk.Label(
        login_panel,
        text="Correo electrónico",
        font=("Arial", 12),
        bg="#e6f2ff"
    )
    txt_correo.pack(anchor="w")

    entrada_correo = tk.Entry(login_panel, font=("Arial", 12), width=30)
    entrada_correo.pack(pady=(0, 10))

    # Etiqueta contraseña

    entrada_correo.bind("<Return>", lambda event: entrada_contrasenha.focus_set())

    txt_contrasena = tk.Label(
        login_panel,
        text="Contraseña",
        font=("Arial", 12),
        bg="#e6f2ff"
    )
    txt_contrasena.pack(anchor="w")

    entrada_contrasenha = tk.Entry(login_panel, font=("Arial", 12), width=30, show="*")
    entrada_contrasenha.pack(pady=(0, 20))

    # Función del botón
    def funcion_boton():
        
        usuario_login = entrada_correo.get()
        contrasenha_login = entrada_contrasenha.get()
        consultar_usuario = conectar(
            f"SELECT * FROM usuarios WHERE correo = '{usuario_login}' AND contrasenna = '{contrasenha_login}'"
        )
        if len(consultar_usuario) != 0:
            print("Usuario Activo")
            ventana.destroy()
            print(consultar_usuario[0][3])
            ventana_usuario(consultar_usuario)
        else:
            print("Datos incorrectos")

    # Botón continuar
    boton = tk.Button(
        login_panel,
        text="Iniciar Sesión",
        command=funcion_boton,
        font=("Arial", 12),
        bg="#007acc",
        fg="white",
        padx=10,
        pady=5,
        relief="flat",
        activebackground="#005f99"
    )
    boton.pack()
    entrada_contrasenha.bind("<Return>", lambda event: funcion_boton())
    print("Panel login cargado")
