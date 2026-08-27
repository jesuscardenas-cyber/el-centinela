from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd


class BaseExportador(ABC):
    """
    Clase base para todos los exportadores.
    """

    @property
    @abstractmethod
    def nombre(self) -> str:
        """Nombre del exportador."""

    @abstractmethod
    def exportar(self, df: pd.DataFrame, destino: Path) -> Path:
        """
        Exporta un DataFrame y devuelve la ruta del archivo generado.
        """
