"""Manages the default Clicycle instance."""

from __future__ import annotations

from .core import Clicycle
from .theme import Theme

_default_cli: Clicycle | None = None


def get_default_cli() -> Clicycle:
    """Get the default Clicycle instance, creating it if necessary."""
    global _default_cli
    if _default_cli is None:
        _default_cli = Clicycle()
    return _default_cli


def configure(
    width: int = 100, theme: Theme | None = None, app_name: str | None = None
) -> None:
    """Configure the default Clicycle instance.

    This should be called at the beginning of your application.
    """
    global _default_cli
    _default_cli = Clicycle(width=width, theme=theme, app_name=app_name)
