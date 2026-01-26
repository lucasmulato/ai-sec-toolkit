import typer
import asyncio
import sys
import yaml
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.logging import RichHandler
import logging

# Setup professional logging
logging.basicConfig(
    level="INFO", format="%(message)s", datefmt="[%X]", handlers=[RichHandler(rich_tracebacks=True)]
)
log = logging.getLogger("ART-T")
console = Console()

app = typer.Typer(
    help="[bold red]ART-T v0.3.0[/bold red]: Enterprise Red Teaming & Policy Validation.",
    rich_markup_mode="rich"
)

# Configuration Management
CONFIG_PATH = Path("config/settings.yaml")

def load_config():
    if not CONFIG_PATH.exists():
        return {"timeout": 30, "retries": 3, "model": "gpt-4o"}
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

@app.command()
def scan(
    input_file: Optional[Path] = typer.Option(None, "--file", "-f", help="Path to a text file to scan."),
    text: Optional[str] = typer.Argument(None, help="Direct text input to scan."),
    output_json: bool = typer.Option(False, "--json", help="Output results in raw JSON format.")
):
    """
    [bold cyan]Multi-Source PII Audit[/bold cyan]: Scans strings or bulk files with error recovery.
    """
    from core.scanner_pii import PIIScanner
    scanner = PIIScanner()
    
    content = text
    if input_file:
        if not input_file.exists():
            log.error(f"File not found: {input_file}")
            raise typer.Exit(code=1)
        content = input_file.read_text()

    if not content:
        log.error("No input provided. Use text argument or --file.")
        return

    async def run_scan():
        try:
            # Added timeout protection for Stage 3 Semantic Reasoning
            return await asyncio.wait_for(scanner.scan(content), timeout=load_config()['timeout'])
        except asyncio.TimeoutError:
            log.error("Scan timed out during Semantic Analysis.")
            return None
        except Exception as e:
            log.exception(f"Unexpected error during scan: {e}")
            return None

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        transient=True,
    ) as progress:
        progress.add_task(description="Deep Scanning Content...", total=None)
        result = asyncio.run(run_scan())

    if result:
        if output_json:
            import json
            console.print(json.dumps(result, indent=2))
        else:
            _display_scan_table(result)

@app.command()
def campaign(
    goal: str,
    parallel: int = typer.Option(1, "--parallel", "-p", help="Number of concurrent attack instances.")
):
    """
    [bold red]Swarm Attack[/bold red]: Launches multiple adaptive agents to converge on a goal faster.
    """
    from core.attack_engine import AdaptiveAttacker
    attacker = AdaptiveAttacker()
    
    async def launch_swarm():
        tasks = [attacker.run_campaign(goal) for _ in range(parallel)]
        return await asyncio.gather(*tasks, return_exceptions=True)

    console.print(Panel(f"🔥 [bold]Swarm Mode Activated[/bold]: Running {parallel} agents for goal: [red]{goal}[/red]"))
    
    results = asyncio.run(launch_swarm())
    
    # Robust result processing
    success_count = sum(1 for r in results if isinstance(r, dict) and r.get("status") == "success")
    console.print(f"\n[bold green]Campaign Results:[/bold green] {success_count}/{parallel} successful.")

def _display_scan_table(result):
    table = Table(title="ART-T Security Audit", border_style="bright_yellow")
    table.add_column("Index", justify="right", style="dim")
    table.add_column("Stage", style="bold")
    table.add_column("PII Type", style="cyan")
    table.add_column("Extracted Data", style="green")

    for i, d in enumerate(result.get("detections", []), 1):
        table.add_row(str(i), d["stage"], d["type"], d["value"])
    
    console.print(table)

if __name__ == "__main__":
    try:
        app()
    except KeyboardInterrupt:
        console.print("\n[bold red]🚨 Interrupted by user. Shutting down agents safely...[/bold red]")
        sys.exit(0)
