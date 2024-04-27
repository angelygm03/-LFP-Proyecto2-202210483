class Error():
    def __init__(self, error, tipo, fila, columna):
        self.error=error
        self.tipo=tipo
        self.fila=fila
        self.columna=columna

    def __str__(self):
        return f"'{self.error}'"