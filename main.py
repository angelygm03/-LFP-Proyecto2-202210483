import tkinter as tk
from tkinter import ttk

def abrir_archivo():
    pass

def analizar_texto_y_mostrar_mongoDB():
    pass

def salir():
    ventana.quit()

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Traductor Mongo DB")
ventana.configure(bg="#9195F6") 
ventana.geometry("1000x600")

# Menú de opciones
menu_opciones = tk.Menu(ventana)
ventana.config(menu=menu_opciones)

# Opción Archivo
submenu_archivo = tk.Menu(menu_opciones, tearoff=0)
menu_opciones.add_cascade(label="Archivo", menu=submenu_archivo)
submenu_archivo.add_command(label="Abrir archivo", command=abrir_archivo)
submenu_archivo.add_separator()
submenu_archivo.add_command(label="Salir", command=salir)

# Opción Análisis
submenu_analisis = tk.Menu(menu_opciones, tearoff=0)
menu_opciones.add_cascade(label="Análisis", menu=submenu_analisis)
submenu_analisis.add_command(label="Traducir a HTML", command=analizar_texto_y_mostrar_mongoDB)

# Opción Tokens
submenu_tokens = tk.Menu(menu_opciones, tearoff=0)
menu_opciones.add_cascade(label="Tokens", menu=submenu_tokens)

# Opción Errores
submenu_errores = tk.Menu(menu_opciones, tearoff=0)
menu_opciones.add_cascade(label="Errores", menu=submenu_errores)

# Contenedor para los TextAreas
frame_textareas = tk.Frame(ventana, bg="#9195F6")
frame_textareas.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

# Primer textarea
textAreaInicial = tk.Text(frame_textareas, height=20, width=40)
textAreaInicial.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.BOTH)

# Segundo textarea
textAreaFinal = tk.Text(frame_textareas, height=20, width=40, state="normal")
textAreaFinal.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.BOTH)

ventana.mainloop()
