"""Base component class with standard interface."""

from __future__ import annotations

from abc import ABC, abstractmethod

from rich.console import Console

from clicycle.theme import Theme


class Component(ABC):
    """Base component with standard values and interface."""

    component_type: str = "base"

    def __init__(self, theme: Theme):
        self.theme = theme
        self._previous_component: Component | None = None
        self.was_transient = False  # Track if this component disappeared

    def set_context(self, previous: Component | None) -> None:
        """Set rendering context - what came before this component."""
        self._previous_component = previous

    def get_spacing_before(self) -> int:
        """Get spacing before this component based on theme and context."""
        if self._previous_component is None:
            return 0

        # Get spacing rules from theme for this component type
        spacing_rules = getattr(self.theme.spacing, self.component_type, {})

        # Check if we have a rule for the previous component type
        if self._previous_component.component_type in spacing_rules:
            spacing = int(spacing_rules[self._previous_component.component_type])
        else:
            # Default spacing
            spacing = 1

        # If previous component was transient (disappeared), reduce spacing by 1
        if (
            hasattr(self._previous_component, "was_transient")
            and self._previous_component.was_transient
        ):
            spacing = max(0, spacing - 1)

        return spacing

    def render_with_spacing(self, console: Console) -> None:
        """Render this component with appropriate spacing."""
        # For deferred components (progress/spinner), don't do anything here
        # They handle their own spacing and rendering when their context manager starts
        if hasattr(self, "deferred_render") and self.deferred_render:
            return

        # Apply spacing
        spacing = self.get_spacing_before()
        if spacing > 0:
            console.print("\n" * spacing, end="")

        # Render the component
        self.render(console)

    @abstractmethod
    def render(self, console: Console) -> None:
        """Render the component content."""
        pass
