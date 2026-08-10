from __future__ import annotations

from modelos.consulta import Consulta
from modelos.noticias import Noticia
from servicios.base import BaseServicioBusqueda
from servicios.googlenews.google_news_api import GoogleNewsAPI
from servicios.googlenews.google_news_mapper import GoogleNewsMapper
from servicios.googlenews.google_news_parser import GoogleNewsParser


class GoogleNewsSearcher(BaseServicioBusqueda):
    """
    Servicio de búsqueda mediante Google News.
    """

    @property
    def nombre(self) -> str:
        return "Google News"

    def __init__(self) -> None:
        self.api = GoogleNewsAPI()

    def buscar(
        self,
        consulta: Consulta,
    ) -> list[Noticia]:

        feed = self.api.buscar(consulta.texto)

        datos = GoogleNewsParser.convertir(feed)

        return GoogleNewsMapper.convertir(
            datos,
            consulta,
        )
