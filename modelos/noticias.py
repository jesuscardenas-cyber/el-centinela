from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Noticia:
    """
    Modelo común para representar una noticia encontrada
    por cualquiera de los servicios de búsqueda.
    """

    titulo: str
    fuente: str
    fecha: str
    enlace: str

    servicio: str = ""
    empresa: str = ""
    palabra: str = ""
    id_consulta: int = 0
