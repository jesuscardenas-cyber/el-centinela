from __future__ import annotations

from modelos.consulta import Consulta
from modelos.noticias import Noticia
from servicios.base import BaseServicioBusqueda
from servicios.facebook.facebook_api import FacebookAPI
from servicios.facebook.facebook_mapper import FacebookMapper
from servicios.facebook.facebook_parser import FacebookParser


class FacebookSearcher(BaseServicioBusqueda):
    """
    Servicio de búsqueda mediante la API de Meta Ads / Facebook.
    """

    @property
    def nombre(self) -> str:
        return "Facebook"

    def __init__(self) -> None:
        self.api = FacebookAPI()

    def buscar(self, consulta: Consulta, token_override: str = "") -> list[Noticia]:
        respuesta_raw = self.api.buscar(consulta, token_override=token_override)
        datos_limpios = FacebookParser.limpiar(respuesta_raw)
        return FacebookMapper.convertir(datos_limpios, consulta)
