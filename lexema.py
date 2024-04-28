class Lexema:
    def __init__(self, tipo, lexema, fila, columna):
        self.tipo = tipo
        self.lexema = lexema
        self.fila = fila
        self.columna = columna

class Error:
    def __init__(self, tipo, fila, columna, token_esperado=None, descripcion=None):
        self.tipo = tipo
        self.fila = fila
        self.columna = columna
        self.token_esperado = token_esperado
        self.descripcion = descripcion
