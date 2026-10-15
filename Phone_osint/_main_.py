from __future__ import annotations

import asyncio
from pathlib import Path

import typer

from .core import investigate
from .report import print_rich, save_html, to_json

app = typer.Typer(
    add_completion=False,
    help="OSINT-анализ номера телефона (только легальные источники).",
)


@app.command()
def main(
    number: str = typer.Argument(..., help="Номер, например +79991234567"),
    json_out: bool = typer.Option(False, "--json", help="Вывести JSON"),
    html_path: Path | None = typer.Option(
        None, "--html", help="Сохранить HTML-отчёт по указанному пути"
    ),
) -> None:
    report = asyncio.run(investigate(number))

    if json_out:
        typer.echo(to_json(report))
    else:
        print_rich(report)

    if html_path:
        saved = save_html(report, html_path)
        typer.secho(f"HTML: {saved}", fg=typer.colors.GREEN)


if __name__ == "__main__":
    app()
