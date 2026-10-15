from __future__ import annotations

import httpx

from ..models import PhoneReport, PluginResult
from .base import Plugin

NUMVERIFY_URL = "http://apilayer.net/api/validate"


class NumverifyPlugin(Plugin):
    """Оператор и тип линии через Numverify (требует API key)."""

    name = "numverify"
    requires_key = "NUMVERIFY_API_KEY"

    async def run(self, report: PhoneReport, client: httpx.AsyncClient) -> PluginResult:
        params = {
            "access_key": self.env["NUMVERIFY_API_KEY"],
            "number": report.e164 or report.raw,
            "format": 1,
        }
        try:
            r = await client.get(NUMVERIFY_URL, params=params, timeout=15)
            data = r.json()
            if not data.get("valid"):
                return PluginResult(
                    name=self.name, status="ok",
                    data={"valid": False, "raw": data},
                )
            return PluginResult(
                name=self.name, status="ok",
                data={
                    "valid": True,
                    "country": data.get("country_name"),
                    "location": data.get("location"),
                    "carrier": data.get("carrier"),
                    "line_type": data.get("line_type"),
                },
            )
        except Exception as e:
            return PluginResult(name=self.name, status="error", error=str(e))
