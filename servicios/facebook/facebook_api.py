from __future__ import annotations

import json
import urllib.parse
import urllib.request

from config import FB_ACCESS_TOKEN
from modelos.consulta import Consulta
from servicios.clientes.retry import Retry


class FacebookAPI:
    """
    Cliente oficial para consumir la Meta Ad Library API (Graph API).
    """

    BASE_URL = "https://graph.facebook.com/v22.0/ads_archive"

    def buscar(self, consulta: Consulta, token_override: str = "") -> dict:
        token = token_override or FB_ACCESS_TOKEN

        if not token:
            return {"data": []}

        params = {
            "access_token": token,
            "search_terms": consulta.texto,
            "ad_reached_countries": "['MX']",  # Ajustable según el mercado
            "ad_active_status": "ALL",
            "fields": "id,page_name,ad_creative_bodies,ad_delivery_start_time,ad_snapshot_url",
            "limit": "25",
        }

        url = f"{self.BASE_URL}?{urllib.parse.urlencode(params)}"

        def _peticion():
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode("utf-8"))

        try:
            return Retry.ejecutar(_peticion)
        except (json.JSONDecodeError, OSError):
            return {"data": []}
