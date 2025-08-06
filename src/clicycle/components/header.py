"""Header component for displaying titles."""

from __future__ import annotations

from rich.console import Console
from rich.text import Text as RichText

from clicycle.components.base import Component
from clicycle.theme import Theme


class Header(Component):
    """Header component for displaying prominent titles.

    Creates a visually prominent header with optional subtitle and app branding.
    Typically used at the start of an application or major section.
    Text transforms (uppercase, title case) are applied based on theme settings.

    Args:
        theme: Theme configuration for styling and spacing
        title: Main header text to display prominently
        subtitle: Optional secondary text shown below the title
        app_name: Optional application name shown as branding prefix

    Example:
        >>> import clicycle as cc
        >>> cc.header("User Management", "Configure system users")
        >>> cc.header("Welcome", app_name="MyApp")  # Shows: MyApp / Welcome
        >>> cc.header("Data Processing", "Analyzing 10,000 records")
    """

    component_type = "header"

    def __init__(
        self,
        theme: Theme,
        title: str,
        subtitle: str | None = None,
        app_name: str | None = None,
    ):
        super().__init__(theme)
        self.title = title
        self.subtitle = subtitle
        self.app_name = app_name

    def render(self, console: Console) -> None:
        """Render header with optional app branding.

        Args:
            console: Rich console instance for rendering
        """
        title_text = self.theme.transform_text(
            self.title,
            self.theme.typography.header_transform,
        )

        if self.app_name:
            app_branding = f"[bold cyan]{self.app_name}[/][bold white] / [/]"
            console.print(
                f"{app_branding}{RichText(title_text, style=self.theme.typography.header_style)}",
            )
        else:
            console.print(
                RichText(title_text, style=self.theme.typography.header_style),
            )

        if self.subtitle:
            subtitle_text = self.theme.transform_text(
                self.subtitle,
                self.theme.typography.subheader_transform,
            )
            console.print(
                RichText(subtitle_text, style=self.theme.typography.subheader_style),
            )
