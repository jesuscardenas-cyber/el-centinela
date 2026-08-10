from __future__ import annotations

from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from time import perf_counter
from typing import Any


@dataclass(slots=True)
class ResultadoTarea:
    """
    Representa el resultado de una tarea ejecutada.
    """

    servicio: str = ""
    resultado: Any = None
    exitoso: bool = False
    error: str | None = None
    intentos: int = 0
    tiempo_segundos: float = 0.0


class TaskManager:
    """
    Administrador de tareas concurrentes.

    Se encarga de ejecutar tareas utilizando ThreadPoolExecutor,
    procesarlas por lotes y controlar los errores.
    """

    def __init__(
        self,
        max_workers: int = 5,
        batch_size: int = 10,
        max_retries: int = 2,
    ) -> None:

        if max_workers < 1:
            raise ValueError("max_workers debe ser mayor que 0.")

        if batch_size < 1:
            raise ValueError("batch_size debe ser mayor que 0.")

        if max_retries < 0:
            raise ValueError("max_retries no puede ser negativo.")

        self.max_workers = max_workers
        self.batch_size = batch_size
        self.max_retries = max_retries

    def ejecutar_tarea(
        self,
        funcion: Callable,
        argumentos: tuple = (),
        servicio: str = "",
    ) -> ResultadoTarea:
        """
        Ejecuta una tarea individual con reintentos.
        """

        inicio = perf_counter()

        ultimo_error = None

        for intento in range(
            1,
            self.max_retries + 2,
        ):
            try:
                resultado = funcion(*argumentos)

                fin = perf_counter()

                return ResultadoTarea(
                    servicio=servicio,
                    resultado=resultado,
                    exitoso=True,
                    intentos=intento,
                    tiempo_segundos=round(
                        fin - inicio,
                        2,
                    ),
                )

            except Exception as ex:  # noqa: BLE001
                ultimo_error = str(ex)

                print(f"[INTENTO {intento}] Error ejecutando tarea: {ex}")

        fin = perf_counter()

        return ResultadoTarea(
            servicio=servicio,
            resultado=None,
            exitoso=False,
            error=ultimo_error,
            intentos=self.max_retries + 1,
            tiempo_segundos=round(
                fin - inicio,
                2,
            ),
        )

    def ejecutar_batch(
        self,
        tareas: list[tuple[Callable, tuple] | tuple[Callable, tuple, str]],
    ) -> list[ResultadoTarea]:
        """
        Ejecuta un batch de tareas concurrentemente.

        Cada entrada puede ser:
        - (funcion, argumentos)
        - (funcion, argumentos, servicio)
        """

        resultados = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futuros = []

            for tarea in tareas:
                if len(tarea) == 2:
                    funcion, argumentos = tarea
                    servicio = ""
                elif len(tarea) == 3:
                    funcion, argumentos, servicio = tarea
                else:
                    raise ValueError(
                        "Cada tarea debe tener 2 o 3 elementos: "
                        "(funcion, argumentos) o (funcion, argumentos, servicio)"
                    )

                futuros.append(
                    executor.submit(
                        self.ejecutar_tarea,
                        funcion,
                        argumentos,
                        servicio,
                    )
                )

            for futuro in as_completed(futuros):
                resultado = futuro.result()

                resultados.append(resultado)

        return resultados

    def ejecutar(
        self,
        tareas: list[tuple[Callable, tuple] | tuple[Callable, tuple, str]],
    ) -> list[ResultadoTarea]:
        """
        Ejecuta todas las tareas utilizando batches.
        """

        if not tareas:
            return []

        resultados_totales = []

        total_tareas = len(tareas)

        total_batches = (total_tareas + self.batch_size - 1) // self.batch_size

        print(f"Total de tareas: {total_tareas}")

        print(f"Total de batches: {total_batches}")

        for numero_batch in range(total_batches):
            inicio = numero_batch * self.batch_size

            fin = min(
                inicio + self.batch_size,
                total_tareas,
            )

            batch = tareas[inicio:fin]

            print(
                f"\nProcesando batch "
                f"{numero_batch + 1}/"
                f"{total_batches} "
                f"({len(batch)} tareas)"
            )

            resultados_batch = self.ejecutar_batch(batch)

            resultados_totales.extend(resultados_batch)

        return resultados_totales

    def obtener_estadisticas_por_servicio(
        self,
        resultados: list[ResultadoTarea],
    ) -> dict:
        """
        Genera estadísticas agrupadas por servicio.
        """

        estadisticas = {}

        for resultado in resultados:
            servicio = resultado.servicio

            if servicio not in estadisticas:
                estadisticas[servicio] = {
                    "tareas": 0,
                    "exitosas": 0,
                    "fallidas": 0,
                    "noticias": 0,
                    "reintentos": 0,
                    "tiempo_total": 0.0,
                }

            datos = estadisticas[servicio]

            datos["tareas"] += 1

            if resultado.exitoso:
                datos["exitosas"] += 1
            else:
                datos["fallidas"] += 1

            if resultado.resultado:
                datos["noticias"] += len(resultado.resultado)

            datos["reintentos"] += max(
                resultado.intentos - 1,
                0,
            )

            datos["tiempo_total"] += resultado.tiempo_segundos

        for datos in estadisticas.values():
            if datos["tareas"] > 0:
                datos["tiempo_promedio"] = round(
                    datos["tiempo_total"] / datos["tareas"],
                    2,
                )
            else:
                datos["tiempo_promedio"] = 0.0

            del datos["tiempo_total"]

        return estadisticas
