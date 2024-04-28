import tkinter as tk
from tkinter import filedialog, messagebox
from analizadorLexico import analizadorLexico, imprimirLexemas
from lexema import Lexema
import webbrowser
import json
import os

# Variable global para almacenar las sentencias generadas
sentencias_generadas = []
lexemas = []

def nuevo():
    if textAreaInicial.get(1.0, tk.END).strip() != "":
        respuesta = messagebox.askyesnocancel("Guardar Cambios", "¿Desea guardar los cambios antes de limpiar el editor?")
        if respuesta is True:
            guardar()
            limpiar_editor()
        elif respuesta is False:
            limpiar_editor()

def abrir_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")])
    if archivo:
        with open(archivo, "r", encoding="utf-8") as f:
            contenido = f.read()
        textAreaInicial.delete(1.0, tk.END)
        textAreaInicial.insert(1.0, contenido)

def guardar():
    try:
        archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")])
        contenido = textAreaInicial.get(1.0, tk.END)
        with open(archivo, "w") as f:
            f.write(contenido)
        messagebox.showinfo("Guardado", "El archivo ha sido guardado exitosamente.")
    except Exception as e:
        messagebox.showerror("Error al guardar", f"Se produjo un error al guardar el archivo: {str(e)}")

def guardar_como():
    try:
        archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")])
        contenido = textAreaInicial.get(1.0, tk.END)
        with open(archivo, "w") as f:
            f.write(contenido)
        messagebox.showinfo("Guardado", "El archivo ha sido guardado exitosamente.")
    except Exception as e:
        messagebox.showerror("Error al guardar", f"Se produjo un error al guardar el archivo: {str(e)}")

def analizar_texto_wrapper(textAreaInicial, textAreaFinal):
    global sentencias_generadas
    sentencias_generadas, lexemas = analizadorLexico(textAreaInicial, textAreaFinal)
    imprimirLexemas(lexemas)  
    print("Sentencias generadas en analizar_texto_wrapper:", sentencias_generadas)  
    for sentencia in sentencias_generadas:
        textAreaFinal.insert(tk.END, f"{sentencia}\n")

def generar_tabla_tokens(lexemas):
    print("Generando tabla de tokens...")
    imprimirLexemas(lexemas)


def salir():
    ventana.quit()

def limpiar_editor():
    textAreaInicial.delete(1.0, tk.END)
    textAreaFinal.delete(1.0, tk.END)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Traductor Mongo DB")
ventana.configure(bg="#9195F6") 
ventana.geometry("900x600")

# Menú de opciones
menu_opciones = tk.Menu(ventana)
ventana.config(menu=menu_opciones)

# Opción Archivo
submenu_archivo = tk.Menu(menu_opciones, tearoff=0)
menu_opciones.add_cascade(label="Archivo", menu=submenu_archivo)
submenu_archivo.add_command(label="Nuevo", command=nuevo)
submenu_archivo.add_separator()
submenu_archivo.add_command(label="Abrir ", command=abrir_archivo)
submenu_archivo.add_separator()
submenu_archivo.add_command(label="Guardar", command=guardar)
submenu_archivo.add_separator()
submenu_archivo.add_command(label="Guardar como", command=guardar_como)
submenu_archivo.add_separator()
submenu_archivo.add_command(label="Salir", command=salir)

# Opción Análisis
submenu_analisis = tk.Menu(menu_opciones, tearoff=0)
menu_opciones.add_cascade(label="Análisis", menu=submenu_analisis)
submenu_analisis.add_command(label="Traducir a Mongo DB", command=lambda: analizar_texto_wrapper(textAreaInicial, textAreaFinal))

# Opción Tokens
submenu_tokens = tk.Menu(menu_opciones, tearoff=0)
menu_opciones.add_cascade(label="Tokens", menu=submenu_tokens)
submenu_tokens.add_command(label="Generar tabla", command=lambda: generar_tabla_tokens(lexemas))

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