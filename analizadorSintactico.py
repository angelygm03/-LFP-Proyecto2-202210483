from lexema import Lexema, Error
from analizadorLexico import analizadorLexico, generar_tabla_errores

def analizadorSintactico(lexemas, errores):
    sentencias_generadas = []

    idx = 0
    while idx < len(lexemas):
        idx += 1
        if lexemas[idx].tipo == 'Palabra Reservada':
            if lexemas[idx].lexema == 'use':
                idx = analizar_crear_bd(lexemas, idx, sentencias_generadas, errores)

            elif lexemas[idx].lexema == 'dropDatabase':
                idx = analizar_eliminar_bd(lexemas, idx, sentencias_generadas, errores)
            elif lexemas[idx].lexema == 'createCollection':
                idx = analizar_crear_coleccion(lexemas, idx, sentencias_generadas, errores)
            elif lexemas[idx].lexema == 'dropCollection':
                idx = analizar_eliminar_coleccion(lexemas, idx, sentencias_generadas, errores)
            elif lexemas[idx].lexema == 'find':
                idx = analizar_buscar_todo(lexemas, idx, sentencias_generadas, errores)
            elif lexemas[idx].lexema == 'findOne':
                idx = analizar_buscar_unico(lexemas, idx, sentencias_generadas, errores)
            else:
                errores.append(Error(lexemas[idx].lexema, lexemas[idx].fila, lexemas[idx].columna))
                idx += 1
        else:
            errores.append(Error(lexemas[idx].lexema, lexemas[idx].fila, lexemas[idx].columna))
            idx += 1

    return sentencias_generadas

def analizar_crear_bd(lexemas, idx, sentencias_generadas, errores):
    idx += 1  # Avanzar al siguiente lexema
    if idx < len(lexemas) and lexemas[idx].tipo == 'Paréntesis abierto':
        idx += 1  # Avanzar al siguiente lexema
        if idx < len(lexemas) and lexemas[idx].tipo == 'Paréntesis cerrado':
            # Generar la sentencia correspondiente
            sentencias_generadas.append("use();")
            idx += 1  # Avanzar al siguiente lexema
            return idx
        else:
            errores.append(Error("Sintáctico", lexemas[idx].fila, lexemas[idx].columna, "Se esperaba ')'"))
            return idx
    else:
        errores.append(Error("Sintáctico", lexemas[idx].fila, lexemas[idx].columna, "Se esperaba '('"))
        return idx

def analizar_eliminar_bd(lexemas, idx, sentencias_generadas, errores):
    idx += 1  # Avanzar al siguiente lexema (debería ser el nombre de la base de datos)
    if idx < len(lexemas) and lexemas[idx].tipo == 'Identificador':
        nombre_bd = lexemas[idx].lexema
        idx += 1  # Avanzar al siguiente lexema
        if idx < len(lexemas) and lexemas[idx].tipo == 'Operador Asignación':
            idx += 1  # Avanzar al siguiente lexema (debería ser 'nueva')
            if idx < len(lexemas) and lexemas[idx].tipo == 'Palabra Reservada' and lexemas[idx].lexema == 'EliminarBD':
                idx += 1  # Avanzar al siguiente lexema (debería ser ';')
                if idx < len(lexemas) and lexemas[idx].tipo == 'Punto y coma':
                    # Generar la sentencia correspondiente
                    sentencias_generadas.append(f"db.dropDatabase('{nombre_bd}');")
                    idx += 1  # Avanzar al siguiente lexema
                    return idx
                else:
                    errores.append(Error("Sintáctico", lexemas[idx].fila, lexemas[idx].columna, "Se esperaba ';'"))
                    return idx
            else:
                errores.append(Error("Sintáctico", lexemas[idx].fila, lexemas[idx].columna, "Se esperaba 'EliminarBD'"))
                return idx
        else:
            errores.append(Error("Sintáctico", lexemas[idx].fila, lexemas[idx].columna, "Se esperaba '='"))
            return idx
    else:
        errores.append(Error("Sintáctico", lexemas[idx].fila, lexemas[idx].columna, "Nombre de la base de datos no encontrado"))
        return idx

def analizar_crear_coleccion(lexemas, idx, sentencias_generadas, errores):
    idx += 1  # Avanzar al siguiente lexema
    if idx < len(lexemas) and lexemas[idx].tipo == 'Identificador':
        nombre_coleccion = lexemas[idx].lexema
        idx += 1  # Avanzar al siguiente lexema
        if idx < len(lexemas) and lexemas[idx].tipo == 'Operador Asignación':
            idx += 1  # Avanzar al siguiente lexema (debería ser 'nueva')
            if idx < len(lexemas) and lexemas[idx].tipo == 'Palabra Reservada' and lexemas[idx].lexema == 'CrearColeccion':
                idx += 1  # Avanzar al siguiente lexema (debería ser '(')
                if idx < len(lexemas) and lexemas[idx].tipo == 'Paréntesis abierto':
                    idx += 1  # Avanzar al siguiente lexema (debería ser un string)
                    if idx < len(lexemas) and lexemas[idx].tipo == 'Cadena de caracteres':
                        nombre_coleccion_string = lexemas[idx].lexema
                        idx += 1  # Avanzar al siguiente lexema
                        if idx < len(lexemas) and lexemas[idx].tipo == 'Paréntesis cerrado':
                            idx += 1  # Avanzar al siguiente lexema
                            if idx < len(lexemas) and lexemas[idx].tipo == 'Punto y coma':
                                # Generar la sentencia correspondiente
                                sentencias_generadas.append(f"{nombre_coleccion} = nueva CrearColeccion('{nombre_coleccion_string}');")
                                idx += 1  # Avanzar al siguiente lexema
                                return idx
                            else:
                                errores.append(Error("Sintáctico", lexemas[idx].fila, lexemas[idx].columna, "Se esperaba ';'"))
                                return idx
                        else:
                            errores.append(Error("Sintáctico", lexemas[idx].fila, lexemas[idx].columna, "Se esperaba ')'"))
                            return idx
                    else:
                        errores.append(Error("Sintáctico", lexemas[idx].fila, lexemas[idx].columna, "Se esperaba un string para el nombre de la colección"))
                        return idx
                else:
                    errores.append(Error("Sintáctico", lexemas[idx].fila, lexemas[idx].columna, "Se esperaba '('"))
                    return idx
            else:
                errores.append(Error("Sintáctico", lexemas[idx].fila, lexemas[idx].columna, "Se esperaba 'CrearColeccion'"))
                return idx
        else:
            errores.append(Error("Sintáctico", lexemas[idx].fila, lexemas[idx].columna, "Se esperaba '='"))
            return idx
    else:
        errores.append(Error("Sintáctico", lexemas[idx].fila, lexemas[idx].columna, "Nombre de la colección no encontrado"))
        return idx

def analizar_eliminar_coleccion(lexemas, idx, sentencias_generadas, errores):
    idx += 1  # Avanzar al siguiente lexema
    if idx < len(lexemas) and lexemas[idx].tipo == 'Identificador':
        nombre_coleccion = lexemas[idx].lexema
        idx += 1  # Avanzar al siguiente lexema
        if idx < len(lexemas) and lexemas[idx].tipo == 'Operador Asignación':
            idx += 1  # Avanzar al siguiente lexema (debería ser 'nueva')
            if idx < len(lexemas) and lexemas[idx].tipo == 'Palabra Reservada' and lexemas[idx].lexema == 'EliminarColeccion':
                idx += 1  # Avanzar al siguiente lexema (debería ser '(')
                if idx < len(lexemas) and lexemas[idx].tipo == 'Paréntesis abierto':
                    idx += 1  # Avanzar al siguiente lexema (debería ser un string)
                    if idx < len(lexemas) and lexemas[idx].tipo == 'Cadena de caracteres':
                        nombre_coleccion_string = lexemas[idx].lexema
                        idx += 1  # Avanzar al siguiente lexema
                        if idx < len(lexemas) and lexemas[idx].tipo == 'Paréntesis cerrado':
                            idx += 1  # Avanzar al siguiente lexema
                            if idx < len(lexemas) and lexemas[idx].tipo == 'Punto y coma':
                                # Generar la sentencia correspondiente
                                sentencias_generadas.append(f"{nombre_coleccion} = nueva EliminarColeccion('{nombre_coleccion_string}');")
                                idx += 1  # Avanzar al siguiente lexema
                                return idx
                            else:
                                errores.append(Error("Sintáctico", lexemas[idx].fila, lexemas[idx].columna, "Se esperaba ';'"))
                                return idx
                        else:
                            errores.append(Error("Sintáctico", lexemas[idx].fila, lexemas[idx].columna, "Se esperaba ')'"))
                            return idx
                    else:
                        errores.append(Error("Sintáctico", lexemas[idx].fila, lexemas[idx].columna, "Se esperaba un string para el nombre de la colección"))
                        return idx
                else:
                    errores.append(Error("Sintáctico", lexemas[idx].fila, lexemas[idx].columna, "Se esperaba '('"))
                    return idx
            else:
                errores.append(Error("Sintáctico", lexemas[idx].fila, lexemas[idx].columna, "Se esperaba 'EliminarColeccion'"))
                return idx
        else:
            errores.append(Error("Sintáctico", lexemas[idx].fila, lexemas[idx].columna, "Se esperaba '='"))
            return idx
    else:
        errores.append(Error("Sintáctico", lexemas[idx].fila, lexemas[idx].columna, "Nombre de la colección no encontrado"))
        return idx

def analizar_buscar_todo(lexemas, idx, sentencias_generadas, errores):
    idx += 1  # Avanzar al siguiente lexema
    if idx < len(lexemas) and lexemas[idx].tipo == 'Identificador':
        nombre_variable = lexemas[idx].lexema
        idx += 1  # Avanzar al siguiente lexema
        if idx < len(lexemas) and lexemas[idx].tipo == 'Operador Asignación':
            idx += 1  # Avanzar al siguiente lexema (debería ser 'nueva')
            if idx < len(lexemas) and lexemas[idx].tipo == 'Palabra Reservada' and lexemas[idx].lexema == 'BuscarTodo':
                idx += 1  # Avanzar al siguiente lexema (debería ser '(')
                if idx < len(lexemas) and lexemas[idx].tipo == 'Paréntesis abierto':
                    idx += 1  # Avanzar al siguiente lexema (debería ser un string)
                    if idx < len(lexemas) and lexemas[idx].tipo == 'Cadena de caracteres':
                        nombre_coleccion = lexemas[idx].lexema
                        idx += 1  # Avanzar al siguiente lexema
                        if idx < len(lexemas) and lexemas[idx].tipo == 'Paréntesis cerrado':
                            idx += 1  # Avanzar al siguiente lexema
                            if idx < len(lexemas) and lexemas[idx].tipo == 'Punto y coma':
                                # Generar la sentencia correspondiente
                                sentencias_generadas.append(f"{nombre_variable} = nueva BuscarTodo('{nombre_coleccion}');")
                                idx += 1  # Avanzar al siguiente lexema
                                return idx
                            else:
                                errores.append(Error("Sintáctico", lexemas[idx].fila, lexemas[idx].columna, "Se esperaba ';'"))
                                return idx
                        else:
                            errores.append(Error("Sintáctico", lexemas[idx].fila, lexemas[idx].columna, "Se esperaba ')'"))
                            return idx
                    else:
                        errores.append(Error("Sintáctico", lexemas[idx].fila, lexemas[idx].columna, "Se esperaba un string para el nombre de la colección"))
                        return idx
                else:
                    errores.append(Error("Sintáctico", lexemas[idx].fila, lexemas[idx].columna, "Se esperaba '('"))
                    return idx
            else:
                errores.append(Error("Sintáctico", lexemas[idx].fila, lexemas[idx].columna, "Se esperaba 'BuscarTodo'"))
                return idx
        else:
            errores.append(Error("Sintáctico", lexemas[idx].fila, lexemas[idx].columna, "Se esperaba '='"))
            return idx
    else:
        errores.append(Error("Sintáctico", lexemas[idx].fila, lexemas[idx].columna, "Nombre de la variable no encontrado"))
        return idx

def analizar_buscar_unico(lexemas, idx, sentencias_generadas, errores):
    idx += 1  # Avanzar al siguiente lexema
    if idx < len(lexemas) and lexemas[idx].tipo == 'Identificador':
        nombre_variable = lexemas[idx].lexema
        idx += 1  # Avanzar al siguiente lexema
        if idx < len(lexemas) and lexemas[idx].tipo == 'Operador Asignación':
            idx += 1  # Avanzar al siguiente lexema (debería ser 'nueva')
            if idx < len(lexemas) and lexemas[idx].tipo == 'Palabra Reservada' and lexemas[idx].lexema == 'BuscarUnico':
                idx += 1  # Avanzar al siguiente lexema (debería ser '(')
                if idx < len(lexemas) and lexemas[idx].tipo == 'Paréntesis abierto':
                    idx += 1  # Avanzar al siguiente lexema (debería ser un string)
                    if idx < len(lexemas) and lexemas[idx].tipo == 'Cadena de caracteres':
                        nombre_coleccion = lexemas[idx].lexema
                        idx += 1  # Avanzar al siguiente lexema
                        if idx < len(lexemas) and lexemas[idx].tipo == 'Paréntesis cerrado':
                            idx += 1  # Avanzar al siguiente lexema
                            if idx < len(lexemas) and lexemas[idx].tipo == 'Punto y coma':
                                # Generar la sentencia correspondiente
                                sentencias_generadas.append(f"{nombre_variable} = nueva BuscarUnico('{nombre_coleccion}');")
                                idx += 1  # Avanzar al siguiente lexema
                                return idx
                            else:
                                errores.append(Error("Sintáctico", lexemas[idx].fila, lexemas[idx].columna, "Se esperaba ';'"))
                                return idx
                        else:
                            errores.append(Error("Sintáctico", lexemas[idx].fila, lexemas[idx].columna, "Se esperaba ')'"))
                            return idx
                    else:
                        errores.append(Error("Sintáctico", lexemas[idx].fila, lexemas[idx].columna, "Se esperaba un string para el nombre de la colección"))
                        return idx
                else:
                    errores.append(Error("Sintáctico", lexemas[idx].fila, lexemas[idx].columna, "Se esperaba '('"))
                    return idx
            else:
                errores.append(Error("Sintáctico", lexemas[idx].fila, lexemas[idx].columna, "Se esperaba 'BuscarUnico'"))
                return idx
        else:
            errores.append(Error("Sintáctico", lexemas[idx].fila, lexemas[idx].columna, "Se esperaba '='"))
            return idx
    else:
        errores.append(Error("Sintáctico", lexemas[idx].fila, lexemas[idx].columna, "Nombre de la variable no encontrado"))
        return idx
