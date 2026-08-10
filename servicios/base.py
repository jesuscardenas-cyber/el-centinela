from __future__ import annotations

from abc import ABC, abstractmethod

from modelos.consulta import Consulta
from modelos.noticias import Noticia


class BaseServicioBusqueda(ABC):
    """
    Contrato base para todos los servicios de búsqueda.
    """

    @property
    @abstractmethod
    def nombre(self) -> str:
        """
        Nombre identificador del servicio.
        """

    @abstractmethod
    def buscar(self, consulta: Consulta) -> list[Noticia]:
        """
        Ejecuta una búsqueda y devuelve una lista
        normalizada de objetos Noticia.
        """