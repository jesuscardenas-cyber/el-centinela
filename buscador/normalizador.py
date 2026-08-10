from __future__ import annotations


class NormalizadorNoticias:
    """
    Convierte cualquier objeto Noticia a un formato estándar.
    """

    @staticmethod
    def normalizar(noticia) -> dict:

        return {
            "titulo": noticia.titulo,
            "fuente": noticia.fuente,
            "fecha": noticia.fecha,
            "enlace": noticia.enlace,
            "servicio": noticia.servicio,
            "empresa": noticia.empresa,
            "palabra": noticia.palabra,
            "id_consulta": noticia.id_consulta,
        }
