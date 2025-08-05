"""RenderStream orchestrator - just tells components to render themselves."""

from __future__ import annotations

from typing import TYPE_CHECKING

from rich.console import Console

if TYPE_CHECKING:
    from clicycle.components.base import Component


class RenderStream:
    """Orchestrator that tells components to render themselves with context."""

    def __init__(self, console: Console):
        self.console = console
        self.history: list[Component] = []

    def render(self, component: Component) -> None:
        """Tell component to render itself with proper context."""
        # Set context - what came before
        component.set_context(self.last_component)

        # Component renders itself with spacing
        component.render_with_spacing(self.console)

        # Track in history
        self.history.append(component)

    @property
    def last_component(self) -> Component | None:
        """Get the last rendered component."""
        return self.history[-1] if self.history else None

    def clear_history(self) -> None:
        """Clear render history."""
        self.history.clear()
