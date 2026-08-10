from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Consulta:
    """
    Representa una consulta de búsqueda.
    """

    id: int
    empresa: str
    palabra: str
    texto: str
