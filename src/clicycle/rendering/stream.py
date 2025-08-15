"""RenderStream orchestrator - just tells components to render themselves."""

from __future__ import annotations

from typing import TYPE_CHECKING

from rich.console import Console

if TYPE_CHECKING:
    from clicycle.components.base import Component


class RenderStream:
    """Orchestrator that tells components to render themselves with context."""

    def __init__(self, console: Console, max_history: int = 100):
        self.console = console
        self.history: list[Component] = []
        self.max_history = max_history
        self.in_live_context = False  # Track if we're in a progress/spinner context
        self.deferred_component: Component | None = (
            None  # Track the current deferred component
        )

    def render(self, component: Component) -> None:
        """Tell component to render itself with proper context."""
        # For deferred components, set context first then add to history
        # For regular components, they get added after any deferred component
        if hasattr(component, "deferred_render") and component.deferred_render:
            # Deferred components get context from last component in history
            last_comp = self.last_component
            component.set_context(last_comp)

            # Add to history immediately so it's available for spacing calculations
            self.history.append(component)
            if len(self.history) > self.max_history:
                self.history = self.history[-self.max_history :]
            self.deferred_component = component
            self.in_live_context = True
        else:
            # Regular components can always render
            # If there was a deferred component, use it as context
            last_comp = self.last_component
            component.set_context(last_comp)

            # Add regular component to history with size limit
            self.history.append(component)
            if len(self.history) > self.max_history:
                # Keep only the most recent components
                self.history = self.history[-self.max_history :]

            # Clear deferred tracking if it was set
            if self.deferred_component:
                self.deferred_component = None
                self.in_live_context = False

        # Component renders itself with spacing
        component.render_with_spacing(self.console)

    @property
    def last_component(self) -> Component | None:
        """Get the last rendered component."""
        return self.history[-1] if self.history else None

    def clear_history(self) -> None:
        """Clear render history."""
        self.history.clear()
