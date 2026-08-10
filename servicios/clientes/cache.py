class CacheTemporal:
    def __init__(self):

        self._datos = {}

    def obtener(self, clave):

        return self._datos.get(clave)

    def guardar(self, clave, valor):

        self._datos[clave] = valor
