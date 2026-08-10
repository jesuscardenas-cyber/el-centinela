from __future__ import annotations

from datetime import datetime, timezone

from modelos.consulta import Consulta
from modelos.noticias import Noticia


class FacebookMapper:
    @staticmethod
    def convertir(datos: list[dict], consulta: Consulta) -> list[Noticia]:

        noticias = []

        for item in datos:
            noticias.append(
                Noticia(
                    id_consulta=consulta.id,
                    empresa=consulta.empresa,
                    palabra=consulta.palabra,
                    plataforma="Facebook",
                    titulo=item.get("titulo", ""),
                    fuente=item.get("fuente", "Facebook"),
                    fecha_publicacion=item.get("fecha"),
                    enlace=item.get("url", ""),
                    fecha_consulta=datetime.now(tz=timezone.utc),
                )
            )

        return noticias
