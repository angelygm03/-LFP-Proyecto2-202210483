import tkinter as tk
from lexema import Lexema, Error

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
    palabra = ""
    dentro_cadena = False  
    columna = 0  # Inicializar la variable columna
    fila = 1  # Inicializar la variable fila
    
    # Iterar sobre cada caracter del texto
    for char in texto:
        columna += 1
        # Se verifica si está dentro de una cadena de texto
        if char == '"':
            dentro_cadena = not dentro_cadena
            palabra += char
            continue
        
        # Si está dentro de una cadena de texto, se añade el caracter a la palabra
        if dentro_cadena:
            palabra += char
            continue
        
        # Se verifica que el caracter sea una letra, un dígito o un carácter especial
        if char.isalnum(): 
            palabra += char
        else:
            if palabra:
                # Verificar si la palabra es una palabra reservada
                if palabra in ['CrearBD', 'EliminarBD', 'CrearColeccion', 'EliminarColeccion', 'InsertarUnico', 'ActualizarUnico', 'EliminarUnico', 'BuscarTodo', 'BuscarUnico', 'elimina', 'colec', 'eliminacolec', 'insertadoc', 'actualizadoc', 'eliminadoc', 'todo', 'nueva']:
                    lexemas.append(Lexema("Palabra Reservada", palabra, fila, columna - len(palabra)))
                elif palabra.isdigit():
                    lexemas.append(Lexema("Número", palabra, fila, columna - len(palabra)))
                else:
                    lexemas.append(Lexema("Cadena", palabra, fila, columna - len(palabra)))
                palabra = ""
            
            # Otros caracteres especiales
            if char in [',']:
                lexemas.append(Lexema("Coma", char, fila, columna))
            elif char in ['.']:
                lexemas.append(Lexema("Punto", char, fila, columna))
            elif char in ['(']:
                lexemas.append(Lexema("Paréntesis abierto", char, fila, columna))
            elif char in [')']:
                lexemas.append(Lexema("Paréntesis cerrado", char, fila, columna))
            elif char in ['{']:
                lexemas.append(Lexema("Llave de apertura", char, fila, columna))
            elif char in ['}']:
                lexemas.append(Lexema("Llave de cierre", char, fila, columna))
            elif char in [':']:
                lexemas.append(Lexema("Dos puntos", char, fila, columna))
            elif char in ['[']:
                lexemas.append(Lexema("Corchete de apertura", char, fila, columna))
            elif char in [']']:
                lexemas.append(Lexema("Corchete de cierre", char, fila, columna))  
            elif char in ['=']:
                lexemas.append(Lexema("Igual", char, fila, columna))                     
            elif char in [';']:
                lexemas.append(Lexema("Punto y coma", char, fila, columna)) 
            elif char in ['"']:
                lexemas.append(Lexema("Comillas dobles", char, fila, columna))                           
            elif char in [' ']:
                continue
            elif char == '\n':
                fila += 1
                columna = 0  # Reiniciar la columna cuando se encuentra un salto de línea
                continue                                        
            else:
                errores.append(Error(f"{char}", fila, columna))
    
    # Verificar si hay una palabra aún por agregar
    if palabra:
        if palabra in ['CrearBD', 'EliminarBD', 'CrearColeccion', 'EliminarColeccion', 'InsertarUnico', 'ActualizarUnico', 'EliminarUnico', 'BuscarTodo', 'BuscarUnico', 'elimina', 'colec', 'eliminacolec', 'insertadoc', 'actualizadoc', 'eliminadoc', 'todo', 'nueva']:
            lexemas.append(Lexema("Palabra Reservada", palabra, fila, columna - len(palabra)))
        elif palabra.isdigit():
            lexemas.append(Lexema("Número", palabra, fila, columna - len(palabra)))
        else:
            lexemas.append(Lexema("Cadena", palabra, fila, columna - len(palabra)))
    
    imprimirLexemas(lexemas)

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
    
    return lexemas, errores

def imprimirLexemas(lexemas):
    with open("lexemas.html", "w", encoding='utf-8') as f:
        f.write("<html>\n<head>\n<title>Listado de Tokens y Lexemas</title>\n</head>\n<body>\n")
        f.write("<h1>Listado de Tokens y Lexemas</h1>\n")
        f.write("<table border='1'>\n")
        f.write("<tr><th>Correlativo</th><th>Token</th><th>No. de Token</th><th>Lexema</th></tr>\n")
        
        for idx, lexema in enumerate(lexemas, start=1):
            f.write(f"<tr><td>{idx}</td><td>{lexema.tipo}</td><td>{idx}</td><td>{lexema.lexema}</td></tr>\n")
        
        f.write("</table>\n")
        f.write("</body>\n</html>")