from __future__ import annotations

from modelos.consulta import Consulta
from modelos.noticias import Noticia
from servicios.base import BaseServicioBusqueda
from servicios.facebook.facebook_api import FacebookAPI
from servicios.facebook.facebook_mapper import FacebookMapper
from servicios.facebook.facebook_parser import FacebookParser


class FacebookSearcher(BaseServicioBusqueda):
    """
    Servicio de búsqueda mediante Facebook.
    """

    @property
    def nombre(self) -> str:
        return "Facebook"

    def __init__(self) -> None:

        self.api = FacebookAPI()
        self.mapper = FacebookMapper()
        self.parser = FacebookParser()

    def buscar(
        self,
        consulta: Consulta,
    ) -> list[Noticia]:

        datos = self.api.buscar(consulta.texto)

        resultados = []

        for dato in datos:
            noticia = self.mapper.mapear(dato)

            noticia.servicio = self.nombre
            noticia.empresa = consulta.empresa
            noticia.palabra = consulta.palabra

            resultados.append(noticia)

        return resultados
