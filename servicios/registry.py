from __future__ import annotations

from servicios.facebook.facebook import FacebookSearcher
from servicios.googlenews.google_news import GoogleNewsSearcher


def obtener_servicios():
    """
    Devuelve la lista de servicios de búsqueda habilitados.
    """

    return [
        GoogleNewsSearcher(),
        FacebookSearcher(),
    ]
