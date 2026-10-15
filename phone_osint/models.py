from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class PluginResult:
    """Результат одного плагина."""
    name: str
    status: str = "ok"          # ok | skipped | error
    data: dict[str, Any] = field(default_factory=dict)
    error: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class PhoneReport:
    raw: str
    e164: str = ""
    valid: bool = False
    country: str = ""
    region: str = ""
    carrier: str = ""
    timezones: list[str] = field(default_factory=list)
    number_type: str = "unknown"
    results: list[PluginResult] = field(default_factory=list)

    def add(self, result: PluginResult) -> None:
        self.results.append(result)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["results"] = [r.to_dict() for r in self.results]
        return d
