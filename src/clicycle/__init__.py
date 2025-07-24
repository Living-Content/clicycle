from contextlib import contextmanager

from .core import Clicycle
from .instance import configure, get_default_cli
from .prompts import select_from_list
from .theme import ComponentSpacing, Icons, Layout, Theme, Typography

__version__ = "1.0.3"


def header(
    title: str, subtitle: str | None = None, app_name: str | None = None
) -> None:
    """Render header component."""
    get_default_cli().header(title, subtitle, app_name)


def section(title: str) -> None:
    """Render section component."""
    get_default_cli().section(title)


def info(message: str) -> None:
    """Render info message."""
    get_default_cli().info(message)


def success(message: str) -> None:
    """Render success message."""
    get_default_cli().success(message)


def error(message: str) -> None:
    """Render error message."""
    get_default_cli().error(message)


def warning(message: str) -> None:
    """Render warning message."""
    get_default_cli().warning(message)


def debug(message: str) -> None:
    """Render debug message."""
    get_default_cli().debug(message)


def prompt(text: str, **kwargs):
    """Render a prompt with proper spacing."""
    return get_default_cli().prompt(text, **kwargs)


def confirm(text: str, **kwargs):
    """Render a confirm with proper spacing."""
    return get_default_cli().confirm(text, **kwargs)


def summary(data: list[dict[str, str | int | float | bool | None]]) -> None:
    """Render summary component."""
    get_default_cli().summary(data)


def list_item(item: str) -> None:
    """Render list text with bullet point."""
    get_default_cli().list_item(item)


@contextmanager
def spinner(message: str):
    """Context manager for spinner."""
    with get_default_cli().spinner(message) as s:
        yield s


def table(
    data: list[dict[str, str | int | float | bool | None]],
    title: str | None = None,
) -> None:
    """Render table component."""
    get_default_cli().table(data, title)


def code(
    code_str: str,
    language: str = "python",
    title: str | None = None,
    line_numbers: bool = True,
) -> None:
    """Render code component."""
    get_default_cli().code(code_str, language, title, line_numbers)


def json(data: dict, title: str | None = None) -> None:
    """Render JSON as code."""
    get_default_cli().json(data, title)


@contextmanager
def progress(description: str = "Processing"):
    """Context manager for progress tracking."""
    with get_default_cli().progress(description) as p:
        yield p


@contextmanager
def multi_progress(description: str = "Processing"):
    """Context manager for multi-task progress tracking."""
    with get_default_cli().multi_progress(description) as p:
        yield p


def update_progress(percent: float, message: str | None = None) -> None:
    """Update progress bar."""
    get_default_cli().update_progress(percent, message)


def suggestions(suggestions: list[str]) -> None:
    """Render suggestions list."""
    get_default_cli().suggestions(suggestions)


@contextmanager
def block():
    """Context manager for grouped content."""
    with get_default_cli().block() as b:
        yield b


def clear() -> None:
    """Clear terminal and reset context."""
    get_default_cli().clear()


__all__ = [
    "Clicycle",
    "Theme",
    "Icons",
    "Typography",
    "Layout",
    "ComponentSpacing",
    "select_from_list",
    "configure",
    "header",
    "section",
    "info",
    "success",
    "error",
    "warning",
    "debug",
    "prompt",
    "confirm",
    "summary",
    "list_item",
    "spinner",
    "table",
    "code",
    "json",
    "progress",
    "multi_progress",
    "update_progress",
    "suggestions",
    "block",
    "clear",
]
