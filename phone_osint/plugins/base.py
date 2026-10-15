from __future__ import annotations

from abc import ABC, abstractmethod
import httpx

from ..models import PhoneReport, PluginResult


class Plugin(ABC):
    """Базовый класс плагина. Наследники реализуют `run`."""

    name: str = "plugin"
    requires_key: str | None = None   # имя env-переменной, если нужен ключ

    def __init__(self, env: dict[str, str] | None = None):
        self.env = env or {}

    def enabled(self) -> bool:
        if self.requires_key is None:
            return True
        return bool(self.env.get(self.requires_key))

    @abstractmethod
    async def run(
        self,
        report: PhoneReport,
        client: httpx.AsyncClient,
    ) -> PluginResult: ...
