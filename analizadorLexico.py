import tkinter as tk

def analizadorLexico(textAreaInicial, textAreaFinal):
    # Se obtiene el texto de entrada
    texto = textAreaInicial.get(1.0, tk.END)
    
    # Palabras reservadas
    palabras_reservadas = {
        'CrearBD': 'use',
        'EliminarBD': 'dropDataBase',
        'CrearColeccion': 'createCollection',
        'EliminarColeccion': 'dropCollection',
        'InsertarUnico': 'insertOne',
        'ActualizarUnico': 'updateOne',
        'EliminarUnico': 'deleteOne',
        'BuscarTodo': 'find',
        'BuscarUnico': 'findOne'
    }

    # lista para almacenar los lexemas y errores
    lexemas = []
    errores = []

    # Dividir el texto en líneas y analizar cada línea
    lineas = texto.split('\n')
    for idx, linea in enumerate(lineas):
        linea = linea.strip()  # Eliminar espacios en blanco al inicio y al final
        if linea:  # Saltar líneas vacías
            partes = linea.split('= nueva') 
            
            # Verificar si se encontró el patrón
            if len(partes) == 2:
                # Analizar la primera parte para determinar el tipo de función y el parámetro
                tipo_funcion, parametro = partes[0].strip().split(maxsplit=1)
                if tipo_funcion in palabras_reservadas:
                    # Generar la salida final
                    salida_final = f"{palabras_reservadas[tipo_funcion]}('{parametro}');"
                    # Agregar el lexema a la lista
                    lexemas.append(salida_final)
                else:
                    # Enviar error si la palabra clave no es reconocida
                    errores.append(f"Error léxico: Palabra clave desconocida en línea {idx + 1}")
            else:
                # Enviar error si no se encontró el patrón esperado
                errores.append(f"Error léxico: Formato incorrecto en línea {idx + 1}")

    # Mostrar los lexemas en el textAreaFinal
    for lexema in lexemas:
        textAreaFinal.insert(tk.END, f"{lexema}\n")
    
    # Mostrar los errores en el textAreaFinal
    for error in errores:
        textAreaFinal.insert(tk.END, f"Error: {error}\n", "error")
    
    return lexemas, errores
