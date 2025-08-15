"""Group modifier for rendering components without spacing."""

from __future__ import annotations

from rich.console import Console

from clicycle.components.base import Component
from clicycle.theme import Theme


class Group(Component):
    """Group modifier - renders components together ignoring their spacing rules."""

    component_type = "group"

    def __init__(self, theme: Theme, components: list[Component]):
        super().__init__(theme)
        self.components = components

    def render(self, console: Console) -> None:
        """Render components without spacing between them."""
        # Render all components directly without spacing
        for component in self.components:
            component.render(console)
