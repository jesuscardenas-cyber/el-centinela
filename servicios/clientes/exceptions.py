class ServicioBusquedaError(Exception):
    """Excepción base para los servicios."""


class ConexionError(ServicioBusquedaError):
    """Error de conexión."""


class RateLimitError(ServicioBusquedaError):
    """Límite de consultas alcanzado."""


class RespuestaInvalidaError(ServicioBusquedaError):
    """Respuesta inválida del servicio."""
