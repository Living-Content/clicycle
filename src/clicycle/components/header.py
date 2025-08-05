"""Header component for displaying titles."""

from __future__ import annotations

from rich.console import Console
from rich.text import Text as RichText

from clicycle.components.base import Component
from clicycle.theme import Theme


class Header(Component):
    """Header component - like <h1> tag."""

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
        """Render header with optional app branding."""
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
