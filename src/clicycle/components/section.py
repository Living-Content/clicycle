"""Section component for dividing content."""

from __future__ import annotations

from rich.console import Console

from clicycle.components.base import Component
from clicycle.theme import Theme


class Section(Component):
    """Section component - like <section> tag."""

    component_type = "section"

    def __init__(self, theme: Theme, title: str):
        super().__init__(theme)
        self.title = title

    def render(self, console: Console) -> None:
        """Render section with rule."""
        transformed_title = self.theme.transform_text(
            self.title,
            self.theme.typography.section_transform,
        )
        console.rule(
            f"[cyan]{transformed_title}[/]",
            style="dim bright_black",
            align="right",
        )
