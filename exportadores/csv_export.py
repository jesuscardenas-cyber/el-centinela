from __future__ import annotations

from pathlib import Path

import pandas as pd

from exportadores.base import BaseExportador


class CSVExportador(BaseExportador):
    @property
    def nombre(self) -> str:
        return "CSV"

    def exportar(self, df: pd.DataFrame, destino: Path) -> Path:

        destino.parent.mkdir(parents=True, exist_ok=True)

        df.to_csv(destino, index=False, encoding="utf-8-sig")

        return destino
