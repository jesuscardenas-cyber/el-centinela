class FacebookParser:
    """
    Limpieza y normalización
    de respuestas de Facebook.
    """

    @staticmethod
    def limpiar(datos: list[dict]) -> list[dict]:

        resultado = []

        for item in datos:
            if item:
                resultado.append(item)

        return resultado
