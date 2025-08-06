"""Progress bar component for showing task progress."""

from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager
from types import TracebackType
from typing import Literal

from rich.console import Console
from rich.progress import (
    BarColumn,
    Progress,
    TaskID,
    TaskProgressColumn,
    TextColumn,
)
from rich.table import Column

from clicycle.components.base import Component
from clicycle.theme import Theme


class ProgressBar(Component):
    """Progress bar component - indicates ongoing operation with progress."""

    component_type = "progress"

    def __init__(self, theme: Theme, description: str, console: Console):
        super().__init__(theme)
        self.description = description
        self.console = console
        self._progress: Progress | None = None
        self._task_id: TaskID | None = None

    def render(self, console: Console) -> None:
        """Render progress bar title/description."""
        # The actual progress bar is handled by the context manager
        console.print(
            f"{self.theme.icons.running} {self.description}",
            style=self.theme.typography.info_style,
        )

    @contextmanager
    def track(self) -> Generator[ProgressBar, None, None]:
        """Context manager for progress tracking."""
        self._progress = Progress(
            BarColumn(),
            TaskProgressColumn(),
            TextColumn(
                "[progress.description]{task.description}",
                table_column=Column(width=50),
            ),
            console=self.console,
        )
        self._task_id = self._progress.add_task("", total=100)

        try:
            with self._progress:
                yield self
        finally:
            self._progress = None
            self._task_id = None

    def update(self, percent: float, message: str | None = None) -> None:
        """Update progress bar."""
        if self._progress and self._task_id is not None:
            if message:
                self._progress.update(self._task_id, description=message)
            self._progress.update(self._task_id, completed=percent)

    def __enter__(self) -> ProgressBar:
        """Enter context manager."""
        self._context = self.track()
        return self._context.__enter__()

    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None) -> Literal[False]:
        """Exit context manager."""
        if hasattr(self, '_context'):
            self._context.__exit__(exc_type, exc_val, exc_tb)
        return False
