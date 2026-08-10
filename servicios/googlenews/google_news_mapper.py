from __future__ import annotations

from modelos.consulta import Consulta
from modelos.noticias import Noticia


class GoogleNewsMapper:
    """
    Convierte registros del parser en objetos Noticia.
    """

    @staticmethod
    def convertir(
        datos: list[dict],
        consulta: Consulta,
    ) -> list[Noticia]:

        resultado = []

        for item in datos:
            resultado.append(
                Noticia(
                    titulo=item["titulo"],
                    fuente=item["fuente"],
                    fecha=item["fecha"],
                    enlace=item["url"],
                    servicio="Google News",
                    empresa=consulta.empresa,
                    palabra=consulta.palabra,
                    id_consulta=consulta.id,
                )
            )

        return resultado
