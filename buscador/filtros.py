from __future__ import annotations

import re

import pandas as pd


class FiltrosNoticias:
    """
    Conjunto de filtros reutilizables para limpiar
    y filtrar resultados de noticias.

    Los métodos trabajan exclusivamente con los
    nombres internos del modelo de datos.
    """

    @staticmethod
    def eliminar_duplicados(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Elimina noticias duplicadas utilizando el enlace
        como identificador principal.

        Si no existe la columna 'enlace', utiliza todas
        las columnas disponibles.
        """

        if df.empty:
            return df

        if "enlace" in df.columns:
            return df.drop_duplicates(
                subset=["enlace"]
            ).copy()

        return df.drop_duplicates().copy()

    @staticmethod
    def ordenar_por_fecha(
        df: pd.DataFrame,
        columna: str = "fecha",
        ascendente: bool = False,
    ) -> pd.DataFrame:
        """
        Ordena las noticias por fecha.

        Por defecto, muestra primero las noticias
        más recientes.
        """

        if df.empty:
            return df

        if columna not in df.columns:
            return df

        return (
            df.sort_values(
                columna,
                ascending=ascendente,
            )
            .reset_index(drop=True)
        )

    @staticmethod
    def filtrar_fecha_desde(
        df: pd.DataFrame,
        fecha_minima,
    ) -> pd.DataFrame:
        """
        Conserva únicamente noticias posteriores
        o iguales a la fecha indicada.
        """

        if df.empty:
            return df

        if "fecha" not in df.columns:
            return df

        fechas = pd.to_datetime(
            df["fecha"],
            errors="coerce",
        )

        return (
            df[fechas >= fecha_minima]
            .reset_index(drop=True)
        )

    @staticmethod
    def excluir_palabras(
        df: pd.DataFrame,
        palabras: list[str],
    ) -> pd.DataFrame:
        """
        Excluye noticias cuyo título contenga alguna
        de las palabras indicadas.
        """

        if df.empty or not palabras:
            return df

        if "titulo" not in df.columns:
            return df

        patron = "|".join(
            re.escape(p)
            for p in palabras
        )

        mascara = df["titulo"].str.contains(
            patron,
            case=False,
            na=False,
        )

        return (
            df[~mascara]
            .reset_index(drop=True)
        )

    @staticmethod
    def incluir_palabras(
        df: pd.DataFrame,
        palabras: list[str],
    ) -> pd.DataFrame:
        """
        Conserva únicamente noticias cuyo título
        contenga alguna de las palabras indicadas.
        """

        if df.empty or not palabras:
            return df

        if "titulo" not in df.columns:
            return df

        patron = "|".join(
            re.escape(p)
            for p in palabras
        )

        mascara = df["titulo"].str.contains(
            patron,
            case=False,
            na=False,
        )

        return (
            df[mascara]
            .reset_index(drop=True)
        )

    @staticmethod
    def excluir_fuentes(
        df: pd.DataFrame,
        fuentes: list[str],
    ) -> pd.DataFrame:
        """
        Excluye noticias provenientes de las fuentes
        indicadas.
        """

        if df.empty or not fuentes:
            return df

        if "fuente" not in df.columns:
            return df

        patron = "|".join(
            re.escape(f)
            for f in fuentes
        )

        mascara = df["fuente"].str.contains(
            patron,
            case=False,
            na=False,
        )

        return (
            df[~mascara]
            .reset_index(drop=True)
        )

    @staticmethod
    def limitar(
        df: pd.DataFrame,
        cantidad: int,
    ) -> pd.DataFrame:
        """
        Limita la cantidad de resultados.
        """

        if cantidad < 1:
            return df.iloc[0:0].copy()

        return df.head(cantidad).copy()