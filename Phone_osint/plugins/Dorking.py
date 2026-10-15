from __future__ import annotations

import httpx

from ..models import PhoneReport, PluginResult
from .base import Plugin

GOOGLE_CSE_URL = "https://www.googleapis.com/customsearch/v1"


class DorkingPlugin(Plugin):
    """
    Поиск публичных упоминаний номера через Google Custom Search API.
    Требует GOOGLE_API_KEY + GOOGLE_CSE_ID.
    """

    name = "google_dorking"
    requires_key = "GOOGLE_API_KEY"

    async def run(self, report: PhoneReport, client: httpx.AsyncClient) -> PluginResult:
        if not self.env.get("GOOGLE_CSE_ID"):
            return PluginResult(
                name=self.name, status="skipped",
                error="GOOGLE_CSE_ID not set",
            )

        # Пробуем разные форматы — как номер реально пишут на сайтах
        queries = [
            f'"{report.raw}"',
            f'"{report.e164}"',
            f'site:vk.com "{report.raw}"',
            f'site:ok.ru "{report.raw}"',
            f'site:avito.ru "{report.raw}"',
        ]

        hits: list[dict] = []
        for q in queries:
            try:
                r = await client.get(
                    GOOGLE_CSE_URL,
                    params={
                        "key": self.env["GOOGLE_API_KEY"],
                        "cx": self.env["GOOGLE_CSE_ID"],
                        "q": q,
                        "num": 5,
                    },
                    timeout=15,
                )
                if r.status_code != 200:
                    continue
                for item in r.json().get("items", []):
                    hits.append({
                        "query": q,
                        "title": item.get("title"),
                        "link": item.get("link"),
                        "snippet": item.get("snippet"),
                    })
            except Exception:
                continue

        return PluginResult(
            name=self.name, status="ok",
            data={"hits": hits, "count": len(hits)},
        )
