"""Text-based components for displaying messages."""

from __future__ import annotations

from rich.console import Console

from clicycle.components.base import Component
from clicycle.theme import Theme


class Text(Component):
    """Base text component for messages."""

    def __init__(self, theme: Theme, message: str, text_type: str = "info"):
        super().__init__(theme)
        self.message = message
        self.text_type = text_type
        self.component_type = text_type  # For spacing rules

    def render(self, console: Console) -> None:
        """Render the text message with appropriate icon and style."""
        icon_map = {
            "info": self.theme.icons.info,
            "success": self.theme.icons.success,
            "error": self.theme.icons.error,
            "warning": self.theme.icons.warning,
            "debug": self.theme.icons.debug,
        }

        style_map = {
            "info": self.theme.typography.info_style,
            "success": self.theme.typography.success_style,
            "error": self.theme.typography.error_style,
            "warning": self.theme.typography.warning_style,
            "debug": self.theme.typography.debug_style,
        }

        if self.text_type == "list_item":
            icon = self.theme.icons.bullet
            style = self.theme.typography.info_style
        else:
            icon = icon_map.get(self.text_type, self.theme.icons.info)
            style = style_map.get(self.text_type, self.theme.typography.info_style)

        # Get indentation for this text type
        indent_spaces = getattr(self.theme.indentation, self.text_type, 0)
        indent = " " * indent_spaces

        console.print(f"{indent}{icon} {self.message}", style=style)


class Info(Text):
    """Info message component."""

    component_type = "info"

    def __init__(self, theme: Theme, message: str):
        super().__init__(theme, message, "info")


class Success(Text):
    """Success message component."""

    component_type = "success"

    def __init__(self, theme: Theme, message: str):
        super().__init__(theme, message, "success")


class Error(Text):
    """Error message component."""

    component_type = "error"

    def __init__(self, theme: Theme, message: str):
        super().__init__(theme, message, "error")


class WarningText(Text):
    """Warning message component."""

    component_type = "warning"

    def __init__(self, theme: Theme, message: str):
        super().__init__(theme, message, "warning")


class Debug(Text):
    """Debug message component."""

    component_type = "debug"

    def __init__(self, theme: Theme, message: str):
        super().__init__(theme, message, "debug")

    def render(self, console: Console) -> None:
        """Only render debug messages in verbose mode."""
        # Check if we're in verbose mode using Click context
        try:
            import click
            ctx = click.get_current_context()
            if ctx.obj and isinstance(ctx.obj, dict) and not ctx.obj.get("verbose", False):
                return  # Don't render if not verbose
        except RuntimeError:
            # No click context, don't render
            return

        # Render normally if verbose
        super().render(console)


class ListItem(Text):
    """List item component."""

    component_type = "list_item"

    def __init__(self, theme: Theme, message: str):
        super().__init__(theme, message, "list_item")
