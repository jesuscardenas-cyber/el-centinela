from __future__ import annotations

from modelos.consulta import Consulta
from modelos.noticias import Noticia


class FacebookMapper:
    """
    Convierte registros estructurados de Facebook en objetos Noticia.
    """

    @staticmethod
    def convertir(datos: list[dict], consulta: Consulta) -> list[Noticia]:
        noticias = []

        for item in datos:
            noticias.append(
                Noticia(
                    titulo=item.get("titulo", ""),
                    fuente=item.get("fuente", "Facebook"),
                    fecha=item.get("fecha", ""),
                    enlace=item.get("url", ""),
                    servicio="Facebook",
                    empresa=consulta.empresa,
                    palabra=consulta.palabra,
                    id_consulta=consulta.id,
                )
            )

        return noticias
