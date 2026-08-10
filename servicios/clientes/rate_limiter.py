from __future__ import annotations

import time


class RateLimiter:
    def __init__(self, intervalo: float = 1.0):

        self.intervalo = intervalo

        self.ultimo = 0

    def esperar(self):

        ahora = time.time()

        diferencia = ahora - self.ultimo

        if diferencia < self.intervalo:
            time.sleep(self.intervalo - diferencia)

        self.ultimo = time.time()
