from __future__ import annotations

import time


class Retry:
    @staticmethod
    def ejecutar(
        funcion,
        intentos: int = 3,
        espera: int = 2,
        excepciones: tuple[type[BaseException], ...] = (Exception,),
    ):

        ultimo_error = None

        for _ in range(intentos):
            try:
                return funcion()

            except excepciones as ex:
                ultimo_error = ex

                time.sleep(espera)

        raise ultimo_error
