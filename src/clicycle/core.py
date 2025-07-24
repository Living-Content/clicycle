"""HTML-like CLI with self-spacing components."""

from __future__ import annotations

import json
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

import click
from rich.console import Console
from rich.progress import (
    BarColumn,
    Progress,
    TaskID,
    TaskProgressColumn,
    TextColumn,
)
from rich.table import Column

from .render import (
    Block,
    Code,
    Confirm,
    Header,
    ProgressBar,
    Prompt,
    RenderStream,
    Section,
    Spinner,
    Summary,
    Table,
    Text,
)
from .theme import Theme


class Clicycle:
    """HTML-like CLI with self-spacing components."""

    def __init__(
        self, width: int = 100, theme: Theme | None = None, app_name: str | None = None
    ):
        self.width = width
        self.theme = theme or Theme()
        self.console = Console(width=width)
        self.stream = RenderStream(self.console)
        self.app_name = app_name

        # Progress tracking
        self._progress: Progress | None = None
        self._task_id: TaskID | None = None

    def header(
        self, title: str, subtitle: str | None = None, app_name: str | None = None
    ) -> None:
        """Render header component."""
        # Use passed app_name, fall back to instance app_name, or None
        header_app_name = app_name or self.app_name
        self.stream.render(Header(self.theme, title, subtitle, header_app_name))

    def section(self, title: str) -> None:
        """Render section component."""
        self.stream.render(Section(self.theme, title))

    def info(self, message: str) -> None:
        """Render info message."""
        # Fast path: calculate spacing but render directly
        component = Text(self.theme, message, "info")
        spacing = component.spacing_before(self.stream.last_component)
        if spacing > 0:
            self.console.print("\n" * spacing, end="")

        # Direct console output with cached styles
        icon = self.theme._style_cache.get("info_icon", f"{self.theme.icons.info} ")
        self.console.print(f"{icon}{message}", style=self.theme.typography.info_style)

        # Update render history
        self.stream.history.append(component)

    def success(self, message: str) -> None:
        """Render success message."""
        # Fast path: calculate spacing but render directly
        component = Text(self.theme, message, "success")
        spacing = component.spacing_before(self.stream.last_component)
        if spacing > 0:
            self.console.print("\n" * spacing, end="")

        # Direct console output with cached styles
        icon = self.theme._style_cache.get(
            "success_icon", f"{self.theme.icons.success} "
        )
        self.console.print(
            f"{icon}{message}", style=self.theme.typography.success_style
        )

        # Update render history
        self.stream.history.append(component)

    def error(self, message: str) -> None:
        """Render error message."""
        # Fast path: calculate spacing but render directly
        component = Text(self.theme, message, "error")
        spacing = component.spacing_before(self.stream.last_component)
        if spacing > 0:
            self.console.print("\n" * spacing, end="")

        # Direct console output with cached styles
        icon = self.theme._style_cache.get("error_icon", f"{self.theme.icons.error} ")
        self.console.print(f"{icon}{message}", style=self.theme.typography.error_style)

        # Update render history
        self.stream.history.append(component)

    def warning(self, message: str) -> None:
        """Render warning message."""
        # Fast path: calculate spacing but render directly
        component = Text(self.theme, message, "warning")
        spacing = component.spacing_before(self.stream.last_component)
        if spacing > 0:
            self.console.print("\n" * spacing, end="")

        # Direct console output with cached styles
        icon = self.theme._style_cache.get(
            "warning_icon", f"{self.theme.icons.warning} "
        )
        self.console.print(
            f"{icon}{message}", style=self.theme.typography.warning_style
        )

        # Update render history
        self.stream.history.append(component)

    def debug(self, message: str) -> None:
        """Render debug message only in verbose mode."""
        if self.is_verbose:
            # Fast path: calculate spacing but render directly
            component = Text(self.theme, message, "debug")
            spacing = component.spacing_before(self.stream.last_component)
            if spacing > 0:
                self.console.print("\n" * spacing, end="")

            # Direct console output with cached styles
            icon = self.theme._style_cache.get(
                "debug_icon", f"{self.theme.icons.debug} "
            )
            self.console.print(
                f"{icon}{message}", style=self.theme.typography.debug_style
            )

            # Update render history
            self.stream.history.append(component)

    def prompt(self, text: str, **kwargs):
        """Render a prompt with proper spacing."""
        # Render the Prompt component for spacing
        self.stream.render(Prompt(self.theme, text, **kwargs))
        # Then call click.prompt() which will appear with proper spacing
        return click.prompt(text, **kwargs)

    def confirm(self, text: str, **kwargs):
        """Render a confirm with proper spacing."""
        # Render the Confirm component for spacing
        self.stream.render(Confirm(self.theme, text, **kwargs))
        # Then call click.confirm() which will appear with proper spacing
        return click.confirm(text, **kwargs)

    def summary(self, data: list[dict[str, str | int | float | bool | None]]) -> None:
        """Render summary component."""
        self.stream.render(Summary(self.theme, data))

    def list_item(self, item: str) -> None:
        """Render list text with bullet point."""
        # Fast path: calculate spacing but render directly
        component = Text(self.theme, item, "list")
        spacing = component.spacing_before(self.stream.last_component)
        if spacing > 0:
            self.console.print("\n" * spacing, end="")

        # Direct console output with cached styles
        icon = self.theme._style_cache.get("bullet_icon", f"{self.theme.icons.bullet} ")
        self.console.print(f"{icon}{item}", style=self.theme.typography.info_style)

        # Update render history
        self.stream.history.append(component)

    @contextmanager
    def spinner(self, message: str):
        """Context manager for spinner."""
        if self.is_verbose:
            self.info(message)
            yield
        elif self._progress is not None:
            # We're inside a progress context, just squelch the spinner
            yield
        else:
            # Render spinner component for spacing, then show actual spinner
            self.stream.render(Spinner(self.theme, message))
            with self.console.status(
                "",
                spinner="dots",
                spinner_style=self.theme.typography.info_style,
            ):
                yield

    def table(
        self,
        data: list[dict[str, str | int | float | bool | None]],
        title: str | None = None,
    ) -> None:
        """Render table component."""
        self.stream.render(Table(self.theme, data, title))

    def code(
        self,
        code: str,
        language: str = "python",
        title: str | None = None,
        line_numbers: bool = True,
    ) -> None:
        """Render code component."""
        self.stream.render(Code(self.theme, code, language, title, line_numbers))

    def json(self, data: dict, title: str | None = None) -> None:
        """Render JSON as code."""
        json_str = json.dumps(data, indent=2, default=str)
        self.stream.render(Code(self.theme, json_str, "json", title))

    @contextmanager
    def progress(self, description: str = "Processing") -> Iterator[Clicycle]:
        """Context manager for progress tracking."""
        if self._progress is not None:
            # We're already in a progress context, just squelch the nested one
            yield self
        else:
            # Render progress component for spacing
            self.stream.render(ProgressBar(self.theme, description))

            progress = Progress(
                BarColumn(),
                TaskProgressColumn(),
                TextColumn(
                    "[progress.description]{task.description}",
                    table_column=Column(width=50),
                ),
                console=self.console,
            )

            self._progress = progress
            self._task_id = progress.add_task("", total=100)

            with progress:
                yield self

            self._progress = None
            self._task_id = None

    @contextmanager
    def multi_progress(self, description: str = "Processing") -> Iterator[Progress]:
        """Context manager for multi-task progress tracking, yielding the Progress object."""
        # Render progress component for spacing
        self.stream.render(ProgressBar(self.theme, description))

        progress = Progress(
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

        with progress as p:
            yield p

    def update_progress(self, percent: float, message: str | None = None) -> None:
        """Update progress bar."""
        if self._progress and self._task_id is not None:
            if message:
                self._progress.update(self._task_id, description=message)
            self._progress.update(self._task_id, completed=percent)

    def suggestions(self, suggestions: list[str]) -> None:
        """Render suggestions list."""
        self.section("Suggestions")
        with self.block():
            for suggestion in suggestions:
                self.list_item(suggestion)

    @contextmanager
    def block(self):
        """Context manager for grouped content with automatic nested block spacing."""
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
                # The 'with' statement handles closing the file.

                # Get all the components that were rendered to the temp stream
                components = temp_stream.history

                # Restore original stream and console
                self.stream = original_stream
                self.console = original_console

                # Render as block
                if components:
                    self.stream.render(Block(self.theme, components))

    def clear(self) -> None:
        """Clear terminal and reset context."""
        self.console.clear()
        self.stream.clear_history()

    @property
    def is_verbose(self) -> bool:
        """Check if verbose mode is enabled."""
        try:
            ctx = click.get_current_context()
            return ctx.obj.get("verbose", False) if ctx.obj else False
        except RuntimeError:
            return False
