"""Main Clicycle class - simple orchestrator for CLI components."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

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

    @contextmanager
    def group(self) -> Iterator[Clicycle]:
        """Context manager for grouped content without spacing between components."""
        from clicycle.modifiers.group import Group

        # Store the current stream and console
        original_stream = self.stream
        original_console = self.console

        with Path("/dev/null").open("w") as dev_null_file:
            # Create temporary console and stream that won't actually display anything
            temp_console = Console(width=self.width, file=dev_null_file)
            temp_stream = RenderStream(temp_console)

            # Temporarily replace both the stream and console
            self.stream = temp_stream
            self.console = temp_console

            try:
                yield self
            finally:
                # Get all the components that were rendered to the temp stream
                components = temp_stream.history

                # Restore original stream and console
                self.stream = original_stream
                self.console = original_console

                # Render as group
                if components:
                    self.stream.render(Group(self.theme, components))
