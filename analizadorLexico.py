import tkinter as tk

def analizadorLexico(textAreaInicial, textAreaFinal):
    # Obtener el texto de entrada
    texto = textAreaInicial.get(1.0, tk.END)
    
    # Palabras reservadas y sus traducciones correspondientes
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

    # Lista para almacenar los lexemas y errores
    lexemas = []
    errores = []

    # Dividir el texto en líneas y analizar cada línea
    lineas = texto.split('\n')
    for idx, linea in enumerate(lineas):
        linea = linea.strip()  # Eliminar espacios en blanco al inicio y al final
        if linea:  # Saltar líneas vacías
            partes = linea.split('= nueva')  # Dividir la línea en dos partes por el patrón "= nueva"
            
            # Verificar si se encontró el patrón
            if len(partes) == 2:
                # Analizar la primera parte para determinar el tipo de función y el parámetro
                tipo_funcion, variable_asignacion = partes[0].strip().split(maxsplit=1)
                if tipo_funcion in palabras_reservadas:
                    # Analizar la segunda parte para determinar si hay una coincidencia con el tipo de función
                    parte_funcion = partes[1].strip()
                    if parte_funcion.startswith(tipo_funcion):
                        # Para las funciones de CrearBD y EliminarBD, no hay necesidad de buscar parámetros
                        if tipo_funcion == 'CrearBD':
                            # Buscar el nombre de la base de datos
                            nombre_bd = variable_asignacion.strip().split('=', 1)[-1].strip("“”")
                            # Generar la salida final con parámetros
                            salida_final = f"{palabras_reservadas[tipo_funcion]}('{nombre_bd}');"
                            # Agregar el lexema a la lista
                            lexemas.append(salida_final)
                        elif tipo_funcion == 'EliminarBD':
                            # Generar la salida final sin parámetros
                            salida_final = f"{palabras_reservadas[tipo_funcion]}();"
                            # Agregar el lexema a la lista
                            lexemas.append(salida_final)
                        else:
                            # Buscar el nombre de la colección entre comillas
                            inicio_comillas = parte_funcion.find('“') + 1
                            fin_comillas = parte_funcion.find('”', inicio_comillas)
                            if inicio_comillas != -1 and fin_comillas != -1:
                                nombre_coleccion = parte_funcion[inicio_comillas:fin_comillas]
                                # Generar la salida final
                                salida_final = f"{palabras_reservadas[tipo_funcion]}('{nombre_coleccion}');"
                                # Agregar el lexema a la lista
                                lexemas.append(salida_final)
                            else:
                                errores.append(f"Error léxico: Nombre de la colección no encontrado en línea {idx + 1}")
                    else:
                        # error si la función no coincide con el tipo de función esperado
                        errores.append(f"Error léxico: La función no coincide con el tipo de función en línea {idx + 1}")
                else:
                    # error si la palabra reservada no es reconocida
                    errores.append(f"Error léxico: Palabra clave desconocida en línea {idx + 1}")
            else:
                #  error si no se encontró el patrón esperado
                errores.append(f"Error léxico: Formato incorrecto en línea {idx + 1}")

    # Mostrar los lexemas en el textAreaFinal
    for lexema in lexemas:
        textAreaFinal.insert(tk.END, f"{lexema}\n")
    
    # Mostrar los errores en el textAreaFinal
    for error in errores:
        textAreaFinal.insert(tk.END, f"Error: {error}\n", "error")
    
    return lexemas, errores
