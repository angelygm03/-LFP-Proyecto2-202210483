class Lexema:
    def __init__(self, tipo, lexema, fila, columna):
        self.tipo = tipo
        self.lexema = lexema
        self.fila = fila
        self.columna = columna

class Error:
    def __init__(self, caracter, fila, columna):
        self.caracter = caracter
        self.fila = fila
        self.columna = columna