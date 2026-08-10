from __future__ import annotations

import urllib.parse

import feedparser

from servicios.clientes.retry import Retry


class GoogleNewsAPI:
    """
    Cliente para consumir el RSS de Google News.
    """

    BASE_URL = (
        "https://news.google.com/rss/search?q={query}&hl=es-419&gl=MX&ceid=MX:es-419"
    )

    def buscar(
        self,
        texto: str,
    ):
        """
        Ejecuta una búsqueda en Google News.

        Parameters
        ----------
        texto : str
            Texto completo de la consulta.

        Returns
        -------
        feedparser.FeedParserDict
            Respuesta procesada del RSS.
        """

        query = urllib.parse.quote_plus(texto)

        url = self.BASE_URL.format(query=query)

        return Retry.ejecutar(lambda: feedparser.parse(url))
