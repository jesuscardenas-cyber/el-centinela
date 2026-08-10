from __future__ import annotations

from pathlib import Path

import pandas as pd

from exportadores.base import BaseExportador


class ExcelExportador(BaseExportador):
    @property
    def nombre(self) -> str:
        return "Excel"

    def exportar(self, df: pd.DataFrame, destino: Path) -> Path:

        destino.parent.mkdir(parents=True, exist_ok=True)

        with pd.ExcelWriter(destino, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="Resultados", index=False)

        return destino
