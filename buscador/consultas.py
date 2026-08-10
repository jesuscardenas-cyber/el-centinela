from itertools import product
from modelos.consulta import Consulta


class GeneradorConsultas:
    """
    Generador de consultas para el motor de inteligencia competitiva.

    Responsabilidades
    -----------------
    - Limpiar listas de entrada.
    - Eliminar duplicados.
    - Generar todas las combinaciones Empresa por Palabra.
    - Devolver una lista de objetos Consulta.
    """

    def __init__(self, empresas, palabras):
        self.empresas = self._limpiar_lista(empresas)
        self.palabras = self._limpiar_lista(palabras)

    @staticmethod
    def _limpiar_lista(lista):

        elementos = []
        vistos = set()

        for item in lista:
            texto = str(item).strip()

            if texto and texto not in vistos:
                elementos.append(texto)
                vistos.add(texto)

        return elementos

    def generar(self):
        """
        Genera todas las combinaciones Empresa + Palabra.
        """

        consultas = []

        for identificador, (empresa, palabra) in enumerate(
            product(self.empresas, self.palabras), start=1
        ):
            consultas.append(
                Consulta(
                    id=identificador,
                    empresa=empresa,
                    palabra=palabra,
                    texto=f'"{empresa}" "{palabra}"',
                )
            )
        return consultas

    def total_consultas(self):
        return len(self.empresas) * len(self.palabras)
