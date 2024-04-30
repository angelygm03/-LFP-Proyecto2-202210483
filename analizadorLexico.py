import tkinter as tk
from lexema import Lexema, Error
import webbrowser
import os, json

def analizadorLexico(textAreaInicial, textAreaFinal):
    texto = textAreaInicial.get(1.0, tk.END)
    
    palabras_reservadas = {
        'CrearBD': 'use',
        'EliminarBD': 'db.dropDatabase',
        'CrearColeccion': 'db.createCollection',
        'EliminarColeccion': 'db.',
        'InsertarUnico': 'insertOne',
        'ActualizarUnico': 'updateOne',
        'EliminarUnico': 'deleteOne',
        'BuscarTodo': 'find',
        'BuscarUnico': 'findOne'
    }

    sentencias_generadas = []
    lexemas = []
    errores = []
    sentencias = []
    palabra = ""
    dentro_cadena = False  
    columna = 0  
    fila = 1  
    
    for char in texto:
        columna += 1
        if char == '"':
            dentro_cadena = not dentro_cadena
            palabra += char
            continue
        
        if dentro_cadena:
            palabra += char
            continue
        
        if char.isalnum(): 
            palabra += char
        else:
            if palabra:
                if palabra in palabras_reservadas:
                    lexemas.append(Lexema("Palabra Reservada", palabra, fila, columna - len(palabra)))
                elif palabra.isdigit():
                    lexemas.append(Lexema("Número", palabra, fila, columna - len(palabra)))
                else:
                    lexemas.append(Lexema("Cadena", palabra, fila, columna - len(palabra)))
                palabra = ""
            
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
            elif char in ['“']:
                lexemas.append(Lexema("Comillas dobles apertura", char, fila, columna)) 
            elif char in ['”']:
                lexemas.append(Lexema("Comillas dobles cierre", char, fila, columna)) 
            elif char in ['/']:
                lexemas.append(Lexema("Diagonal", char, fila, columna))  
            elif char in ['*']:
                lexemas.append(Lexema("Asterisco", char, fila, columna))  
            elif char in ['-']:
                lexemas.append(Lexema("Guión", char, fila, columna))                            
            elif char in [' ']:
                continue
            elif char == '\n':
                fila += 1
                columna = 0
                continue                                        
            # Errores para caracteres específicos
            elif char in ['+', '?', '¡', '¿', '!', '|', '%', '_', '@']:
                errores.append(Error("Error léxico", fila, columna, token_esperado=char, descripcion=f"No se esperaba el carácter '{char}'"))
            else:
                pass

    if palabra:
        if palabra in palabras_reservadas:
            lexemas.append(Lexema("Palabra Reservada", palabra, fila, columna - len(palabra)))
        elif palabra.isdigit():
            lexemas.append(Lexema("Número", palabra, fila, columna - len(palabra)))
        else:
            lexemas.append(Lexema("Cadena", palabra, fila, columna - len(palabra)))
    
    lineas = texto.split('\n')
    for idx, linea in enumerate(lineas):
        linea = linea.strip()  
        if linea: 
            partes = linea.split('= nueva')  
            
            if len(partes) == 2:
                tipo_funcion, variable_asignacion = partes[0].strip().split(maxsplit=1)
                if tipo_funcion in palabras_reservadas:
                    parte_funcion = partes[1].strip()
                    if parte_funcion.startswith(tipo_funcion):
                        if tipo_funcion == 'CrearBD':
                            nombre_bd = variable_asignacion.strip().split('=', 1)[-1].strip("“”")
                            salida_final = f"{palabras_reservadas[tipo_funcion]} ('{nombre_bd}');"
                            sentencias_generadas.append(salida_final)
                        elif tipo_funcion == 'EliminarBD':
                            salida_final = f"{palabras_reservadas[tipo_funcion]}();"
                            sentencias_generadas.append(salida_final)
                        elif tipo_funcion == 'EliminarColeccion':
                            inicio_comillas = parte_funcion.find('(') + 1
                            fin_comillas = parte_funcion.find(')', inicio_comillas)
                            if inicio_comillas != -1 and fin_comillas != -1:
                                nombre_coleccion = parte_funcion[inicio_comillas:fin_comillas].strip('\"')
                                salida_final = f"db.{nombre_coleccion}.drop();"
                                sentencias_generadas.append(salida_final)
                            else:
                                errores.append(Error("Error léxico", fila, columna, descripcion=f"Nombre de la colección no encontrado en línea {idx + 1}"))

                        elif tipo_funcion == 'CrearColeccion':
                            inicio_comillas = parte_funcion.find('(') + 1
                            fin_comillas = parte_funcion.find(')', inicio_comillas)
                            if inicio_comillas != -1 and fin_comillas != -1:
                                nombre_coleccion = parte_funcion[inicio_comillas:fin_comillas].strip('\"')
                                salida_final = f"db.createCollection('{nombre_coleccion}');"
                                sentencias_generadas.append(salida_final)
                            else:
                                errores.append(Error("Error léxico", fila, columna, descripcion=f"Nombre de la colección no encontrado en línea {idx + 1}"))
                        elif tipo_funcion == 'InsertarUnico':
                            inicio_parentesis = parte_funcion.find("(")
                            fin_parentesis = parte_funcion.find(")")
                            if inicio_parentesis != -1 and fin_parentesis != -1:
                                inicio_comillas = parte_funcion.find('"', inicio_parentesis + 1)
                                fin_comillas = parte_funcion.find('"', inicio_comillas + 1)
                                if inicio_comillas != -1 and fin_comillas != -1:
                                    nombre_coleccion = parte_funcion[inicio_parentesis + 1:fin_parentesis].strip()
                                    json_text = parte_funcion[fin_parentesis + 1:fin_comillas].strip()
                                    salida_final = f"db.{nombre_coleccion}.insertOne({json_text});"
                                    sentencias_generadas.append(salida_final)
                                else:
                                    errores.append(Error("Error léxico", fila, columna, descripcion=f"Formato incorrecto en línea {idx + 1}"))
                            else:
                                errores.append(Error("Error léxico", fila, columna, descripcion=f"Datos de inserción no encontrados en línea {idx + 1}"))

                        elif tipo_funcion == 'BuscarTodo':
                            inicio_comillas = parte_funcion.find('(') + 1
                            fin_comillas = parte_funcion.find(')', inicio_comillas)
                            if inicio_comillas != -1 and fin_comillas != -1:
                                nombre_coleccion = parte_funcion[inicio_comillas:fin_comillas].strip('\"')
                                salida_final = f"db.{nombre_coleccion}.find();"
                                sentencias_generadas.append(salida_final)
                            else:
                                errores.append(Error("Error léxico", fila, columna, descripcion=f"Nombre de la colección no encontrado en línea {idx + 1}"))

                        elif tipo_funcion == 'BuscarUnico':
                            inicio_comillas = parte_funcion.find('(') + 1
                            fin_comillas = parte_funcion.find(')', inicio_comillas)
                            if inicio_comillas != -1 and fin_comillas != -1:
                                nombre_coleccion = parte_funcion[inicio_comillas:fin_comillas].strip('\"')
                                salida_final = f"db.{nombre_coleccion}.findOne();"
                                sentencias_generadas.append(salida_final)
                            else:
                                errores.append(Error("Error léxico", fila, columna, descripcion=f"Nombre de la colección no encontrado en línea {idx + 1}"))

                        else:
                            errores.append(Error("Error léxico", fila, columna, descripcion=f"La función no coincide con el tipo de función en línea {idx + 1}"))
                    else:
                        errores.append(Error("Error léxico", fila, columna, descripcion=f"Palabra clave desconocida en línea {idx + 1}"))
                else:
                    errores.append(Error("Error léxico", fila, columna, descripcion=f"Formato incorrecto en línea {idx + 1}"))

    print("Número de sentencias generadas:", len(sentencias_generadas))
    print("Sentencias generadas:", sentencias_generadas)
    print("Lexemas:", lexemas)
    print("Errores:", errores)

    return sentencias_generadas, lexemas, errores

def imprimirLexemas(lexemas, errores):
    with open("lexemas.html", "w", encoding='utf-8') as f:
        f.write("<html>\n<head>\n<title>Listado de Tokens y Lexemas</title>\n</head>\n<body>\n")
        f.write("<h1>Listado de Tokens y Lexemas</h1>\n")
        f.write("<table border='1'>\n")
        f.write("<tr><th>Correlativo</th><th>Token</th><th>No. de Token</th><th>Lexema</th></tr>\n")
        
        for idx, lexema in enumerate(lexemas, start=1):
            f.write(f"<tr><td>{idx}</td><td>{lexema.tipo}</td><td>{idx}</td><td>{lexema.lexema}</td></tr>\n")
        
        f.write("</table>\n")
        f.write("</body>\n</html>")

    webbrowser.open('file://' + os.path.realpath("lexemas.html"))

def generar_tabla_errores(errores):
    print("Generando tabla de errores...")
    with open("errores.html", "w", encoding='utf-8') as f:
        f.write("<html>\n<head>\n<title>Errores</title>\n</head>\n<body>\n")
        f.write("<h1>Errores Lexicos y Sintacticos</h1>\n")
        f.write("<table border='1'>\n")
        f.write("<tr><th>Tipo de Error</th><th>Línea</th><th>Columna</th><th>Token</th></tr>\n")
        
        for error in errores:
            token_esperado = error.token_esperado if error.token_esperado is not None else ""
            f.write(f"<tr><td>{error.tipo}</td><td>{error.fila}</td><td>{error.columna}</td><td>{token_esperado}</td></tr>\n")
        
        f.write("</table>\n")
        f.write("</body>\n</html>")
    webbrowser.open('file://' + os.path.realpath("errores.html"))

