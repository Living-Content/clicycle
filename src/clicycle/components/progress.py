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

from clicycle.components.base import Component
from clicycle.theme import Theme


class ProgressBar(Component):
    """Progress bar component - indicates ongoing operation with progress."""

    component_type = "progress"
    deferred_render = True  # Don't render immediately, wait for context manager

    def __init__(self, theme: Theme, description: str, console: Console):
        super().__init__(theme)
        self.description = description
        self.console = console
        self._progress: Progress | None = None
        self._task_id: TaskID | None = None

    def render(self, console: Console) -> None:
        """Render progress bar title/description."""
        # For progress bars, we don't render anything here since the
        # description is shown as part of the Rich Progress bar itself
        pass

    @contextmanager
    def track(self) -> Generator[ProgressBar, None, None]:
        """Context manager for progress tracking."""
        # Apply spacing BEFORE the progress bar starts
        spacing = self.get_spacing_before()
        if spacing > 0:
            self.console.print("\n" * spacing, end="")

        # Print the description on its own line
        self.console.print(f"{self.theme.icons.running} {self.description}")

        # The stream will handle live context when this component is rendered

        # Create progress bar WITHOUT description (since we printed it above)
        self._progress = Progress(
            BarColumn(),
            TaskProgressColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
            transient=False,
        )
        self._task_id = self._progress.add_task("", total=100)

        try:
            with self._progress:
                yield self
        finally:
            # The stream will handle cleanup when the next component is rendered
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
