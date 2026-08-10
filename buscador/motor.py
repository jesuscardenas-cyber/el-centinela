from __future__ import annotations

from time import perf_counter

import pandas as pd

from buscador.consultas import GeneradorConsultas
from buscador.filtros import FiltrosNoticias
from buscador.normalizador import NormalizadorNoticias
from buscador.task_manager import TaskManager
from config import BATCH_SIZE, MAX_RETRIES, MAX_WORKERS
from modelos.consulta import Consulta
from modelos.noticias import Noticia
from servicios.base import BaseServicioBusqueda
from servicios.registry import obtener_servicios


class MotorBusqueda:
    """
    Motor principal del sistema.

    Orquesta las consultas, delega la ejecución concurrente
    al TaskManager y consolida los resultados.
    """

    def __init__(self) -> None:
        """
        Inicializa los servicios de búsqueda y el administrador
        de tareas.
        """

        self.servicios = obtener_servicios()

        if not self.servicios:
            raise RuntimeError("No existen servicios registrados.")

        self.task_manager = TaskManager(
            max_workers=MAX_WORKERS, batch_size=BATCH_SIZE, max_retries=MAX_RETRIES
        )

    def _crear_tareas(self, consultas):
        """
        Crea las tareas de búsqueda.

        Cada tarea representa una combinación:

        Consulta + Servicio

        Returns
        -------
        list[tuple]
            Lista de funciones y argumentos para TaskManager.
        """

        tareas = []

        for consulta in consultas:
            for servicio in self.servicios:
                tareas.append(
                    (
                        self._buscar_servicio,
                        (
                            servicio,
                            consulta,
                        ),
                        servicio.nombre,
                    )
                )

        return tareas

    @staticmethod
    def _buscar_servicio(
        servicio: BaseServicioBusqueda,
        consulta: Consulta,
    ) -> list[Noticia]:
        """
        Ejecuta una búsqueda sobre un servicio.

        Si el servicio genera un error, se captura para evitar
        que una fuente afecte las demás búsquedas.
        """

        try:
            return servicio.buscar(consulta)

        except Exception as ex:  # noqa: BLE001 - servicios externos pueden lanzar errores heterogéneos
            print(f"[ERROR] {servicio.nombre}: {ex}")

            return []

    def ejecutar(
        self,
        empresas: list[str],
        palabras: list[str],
    ) -> tuple[pd.DataFrame, dict]:
        """
        Ejecuta todas las búsquedas.

        Parameters
        ----------
        empresas : list[str]
            Empresas a investigar.

        palabras : list[str]
            Palabras clave.

        Returns
        -------
        tuple[pd.DataFrame, dict]
            DataFrame consolidado y estadísticas.
        """

        inicio = perf_counter()

        consultas = GeneradorConsultas(
            empresas,
            palabras,
        ).generar()

        tareas = self._crear_tareas(consultas)

        resultados = self.task_manager.ejecutar(tareas)

        estadisticas_servicios = self.task_manager.obtener_estadisticas_por_servicio(
            resultados
        )

        total_bruto = sum(
            len(resultado.resultado)
            for resultado in resultados
            if resultado.exitoso and resultado.resultado
        )

        registros = []

        for resultado in resultados:
            if not resultado.exitoso:
                continue

            if not resultado.resultado:
                continue

            for noticia in resultado.resultado:
                registro = NormalizadorNoticias.normalizar(noticia)

                registros.append(registro)

        df = pd.DataFrame(registros)

        if not df.empty:
            df = FiltrosNoticias.eliminar_duplicados(df)

            df = FiltrosNoticias.ordenar_por_fecha(df)

            df.reset_index(drop=True, inplace=True)

        fin = perf_counter()

        total_batches = (len(tareas) + BATCH_SIZE - 1) // BATCH_SIZE

        estadisticas = {
            "servicios": len(self.servicios),
            "nombres_servicios": [servicio.nombre for servicio in self.servicios],
            "workers": MAX_WORKERS,
            "batch_size": BATCH_SIZE,
            "total_batches": total_batches,
            "consultas": len(consultas),
            "tareas": len(tareas),
            "noticias_brutas": total_bruto,
            "noticias_finales": len(df),
            "duplicados": total_bruto - len(df),
            "tiempo_segundos": round(
                fin - inicio,
                2,
            ),
            "por_servicio": estadisticas_servicios,
        }
        return df, estadisticas
