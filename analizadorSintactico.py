from lexema import Lexema, Error
from analizadorLexico import analizadorLexico

def analizadorSintactico(lexemas, errores):
    sentencias_generadas = []
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

    idx = 0
    while idx < len(lexemas):
        if lexemas[idx].tipo == 'Palabra Reservada':
            tipo_funcion = lexemas[idx].lexema
            if tipo_funcion in palabras_reservadas:
                idx += 1
                if idx < len(lexemas) and lexemas[idx].tipo == 'Cadena':
                    if lexemas[idx + 1].tipo == 'Punto y coma':
                        nombre = lexemas[idx].lexema.strip('“”')
                        sentencia = f"{palabras_reservadas[tipo_funcion]}('{nombre}');"
                        sentencias_generadas.append(sentencia)
                        idx += 2
                    elif lexemas[idx + 1].tipo == 'Paréntesis abierto':
                        parametros = []
                        idx += 2
                        while idx < len(lexemas) and lexemas[idx].tipo != 'Paréntesis cerrado':
                            if lexemas[idx].tipo == 'Comillas dobles':
                                cadena = ""
                                idx += 1
                                while idx < len(lexemas) and lexemas[idx].tipo != 'Comillas dobles':
                                    cadena += lexemas[idx].lexema
                                    idx += 1
                                parametros.append(cadena.strip())
                                idx += 1
                            else:
                                parametros.append(lexemas[idx].lexema)
                                idx += 1
                        if idx < len(lexemas) and lexemas[idx].tipo == 'Paréntesis cerrado':
                            sentencia = f"{palabras_reservadas[tipo_funcion]}({','.join(parametros)});"
                            sentencias_generadas.append(sentencia)
                            idx += 1
                        else:
                            errores.append(Error(')', lexemas[idx].fila, lexemas[idx].columna))
                    else:
                        errores.append(Error(lexemas[idx].lexema, lexemas[idx].fila, lexemas[idx].columna))
                else:
                    errores.append(Error('Cadena', lexemas[idx].fila, lexemas[idx].columna))
            else:
                errores.append(Error(tipo_funcion, lexemas[idx].fila, lexemas[idx].columna))
        else:
            errores.append(Error(lexemas[idx].lexema, lexemas[idx].fila, lexemas[idx].columna))
            idx += 1

    return sentencias_generadas