from __future__ import annotations


class FacebookParser:
    """
    Limpieza y estructuración de la respuesta JSON devuelta por Meta Graph API.
    """

    @staticmethod
    def limpiar(respuesta: dict) -> list[dict]:
        datos = respuesta.get("data", [])
        resultado = []

        for item in datos:
            cuerpos = item.get("ad_creative_bodies", [])
            texto_anuncio = cuerpos[0] if cuerpos else "Anuncio de Facebook / Meta"

            resultado.append(
                {
                    "titulo": texto_anuncio[:150]
                    + ("..." if len(texto_anuncio) > 150 else ""),
                    "fuente": item.get("page_name", "Facebook Ad"),
                    "fecha": item.get("ad_delivery_start_time", ""),
                    "url": item.get(
                        "ad_snapshot_url", "https://www.facebook.com/ads/library/"
                    ),
                }
            )

        return resultado
