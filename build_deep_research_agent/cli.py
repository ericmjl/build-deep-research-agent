"""Custom CLI for build-deep-research-agent.

This is totally optional;
if you want to use it, though,
follow the skeleton to flesh out the CLI to your liking!
Finally, familiarize yourself with Typer,
which is the package that we use to enable this magic.
Typer's docs can be found at:

    https://typer.tiangolo.com
"""

from __future__ import annotations

from pathlib import Path

import typer

app = typer.Typer()


@app.command()
def hello():
    """Echo the project's name."""
    typer.echo("This project's name is build-deep-research-agent")


@app.command()
def describe():
    """Describe the project."""
    typer.echo("SciPy 2026 Tutorial, Ben Batorsky x Eric Ma")


@app.command()
def bootstrap(
    project_root: Path | None = typer.Option(
        None,
        "--project-root",
        "-p",
        help="Project root directory (defaults to auto-detection via pyprojroot).",
    ),
):
    """Install Ollama, pull models, write .env, and launch notebook 00.

    Pulls gemma2:2b (small, Parts 1-2) always. Auto-detects RAM and pulls
    gemma4:12b (large, Parts 3-5) if the machine has >= 32 GB. Writes .env
    with local Ollama defaults for both models, then opens notebook 00 for
    final verification.
    """
    from build_deep_research_agent.bootstrap import bootstrap as run_bootstrap

    run_bootstrap(project_root=project_root)


if __name__ == "__main__":
    app()
