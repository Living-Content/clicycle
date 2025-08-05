"""Main Clicycle class - simple orchestrator for CLI components."""

from __future__ import annotations

import click
from rich.console import Console

from clicycle.rendering.stream import RenderStream
from clicycle.theme import Theme


class Clicycle:
    """Simple orchestrator for CLI components."""

    def __init__(
        self, width: int = 100, theme: Theme | None = None, app_name: str | None = None
    ):
        self.width = width
        self.theme = theme or Theme()
        self.console = Console(width=width)
        self.stream = RenderStream(self.console)
        self.app_name = app_name

    def clear(self) -> None:
        """Clear the console and reset history."""
        self.console.clear()
        self.stream.clear_history()

    @property
    def is_verbose(self) -> bool:
        """Check if verbose mode is enabled."""
        try:
            ctx = click.get_current_context()
            if ctx.obj and isinstance(ctx.obj, dict):
                return bool(ctx.obj.get("verbose", False))
            return False
        except RuntimeError:
            return False
