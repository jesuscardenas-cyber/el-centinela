from __future__ import annotations

import requests


class HttpClient:
    def __init__(self, timeout: int = 20):

        self.timeout = timeout

        self.session = requests.Session()

        self.session.headers.update({"User-Agent": "CompetitorSearch/1.0"})

    def get(self, url: str, **kwargs):

        return self.session.get(url, timeout=self.timeout, **kwargs)
