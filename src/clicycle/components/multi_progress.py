"""Multi-task progress component for showing multiple concurrent tasks."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from types import TracebackType
from typing import Literal

from rich.console import Console
from rich.progress import (
    BarColumn,
    Progress,
    TaskProgressColumn,
    TextColumn,
)
from rich.table import Column

from clicycle.components.base import Component
from clicycle.theme import Theme


class MultiProgress(Component):
    """Multi-task progress component - tracks multiple concurrent tasks."""

    component_type = "multi_progress"

    def __init__(self, theme: Theme, description: str, console: Console):
        super().__init__(theme)
        self.description = description
        self.console = console
        self._progress: Progress | None = None

    def render(self, console: Console) -> None:
        """Render multi-progress title/description."""
        console.print(
            f"{self.theme.icons.running} {self.description}",
            style=self.theme.typography.info_style,
        )

    @contextmanager
    def track(self) -> Iterator[Progress]:
        """Context manager that yields the Progress object for multi-task tracking."""
        self._progress = Progress(
            TextColumn("[bold blue]{task.fields[short_id]}", justify="right"),
            TextColumn(
                "[progress.description]{task.description}",
                table_column=Column(width=12),
            ),
            BarColumn(),
            "[",
            TaskProgressColumn(),
            "]",
            console=self.console,
        )

        try:
            with self._progress as p:
                yield p
        finally:
            self._progress = None

    def __enter__(self) -> Progress:
        """Enter context manager, returning Progress object."""
        self._context = self.track()
        return self._context.__enter__()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> Literal[False]:
        """Exit context manager."""
        if hasattr(self, "_context"):
            self._context.__exit__(exc_type, exc_val, exc_tb)
        return False
