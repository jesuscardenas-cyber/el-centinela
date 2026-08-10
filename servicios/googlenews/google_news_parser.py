from __future__ import annotations


class GoogleNewsParser:
    @staticmethod
    def convertir(feed):

        noticias = []

        for entrada in feed.entries:
            noticias.append(
                {
                    "titulo": entrada.title,
                    "fuente": entrada.source.get("title", "Google News"),
                    "fecha": entrada.published,
                    "url": entrada.link,
                }
            )

        return noticias
