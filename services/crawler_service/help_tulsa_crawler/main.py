from pathlib import Path
from typing import Optional
import typer

from .parser import parse_excel, parse_url, write_resources
from .scheduler import start_scheduler

app = typer.Typer(help="HelpTulsa resource crawler")

DATA_PATH = Path("/app/data/resources.yaml")

@app.command()
def ingest(source: str):
    """Ingest an Excel file or URL into resources.yaml"""
    if source.startswith("http"):
        records = parse_url(source)
    else:
        records = parse_excel(Path(source))
    write_resources(DATA_PATH, records)
    typer.echo(f"Wrote {len(records)} records to {DATA_PATH}")

@app.command()
def schedule():
    """Start the scheduler for nightly diffs"""
    start_scheduler(DATA_PATH)

if __name__ == "__main__":
    app()
