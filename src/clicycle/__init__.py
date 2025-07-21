"""Clicycle: HTML-like CLI framework with self-spacing components and Rich theming.

A modern CLI framework that provides React/HTML-like components for building
beautiful command-line interfaces with automatic spacing and Rich theming.

Basic Usage:
    from clicycle import Clicycle, Theme

    cli = Clicycle()
    cli.header("My App", "Version 1.0")
    cli.info("This is an info message")
    cli.success("Operation completed!")

Components:
    - Header: Main page titles with branding
    - Section: Section dividers with rules
    - Text: Info, success, error, warning, debug messages
    - Table: Data tables with smart column sizing
    - Code: Syntax-highlighted code blocks
    - Summary: Key-value data display
    - Progress: Progress bars and spinners
    - Prompts: Interactive input with proper spacing

Theming:
    Customize icons, typography, layout, and spacing rules through the Theme class.
"""

from .core import Clicycle
from .prompts import select_from_list
from .theme import ComponentSpacing, Icons, Layout, Theme, Typography

__version__ = "0.1.0"
__all__ = [
    "Clicycle",
    "Theme",
    "Icons",
    "Typography",
    "Layout",
    "ComponentSpacing",
    "select_from_list",
]
