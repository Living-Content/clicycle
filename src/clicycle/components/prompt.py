"""Prompt components for user input."""

from __future__ import annotations

from typing import Any

from rich.console import Console
from rich.prompt import Confirm as RichConfirm
from rich.prompt import Prompt as RichPrompt

from clicycle.components.base import Component
from clicycle.theme import Theme


class Prompt(Component):
    """Prompt component for user input."""

    component_type = "prompt"

    def __init__(self, theme: Theme, text: str, console: Console, **kwargs: Any) -> None:
        super().__init__(theme)
        self.text = text
        self.console = console
        self.kwargs = kwargs

    def render(self, console: Console) -> None:
        """Prompts don't render - they return values."""
        pass

    def ask(self) -> Any:
        """Ask the user for input."""
        return RichPrompt.ask(
            f"{self.theme.icons.info} {self.text}", console=self.console, **self.kwargs
        )


class Confirm(Component):
    """Confirm component for yes/no questions."""

    component_type = "confirm"

    def __init__(self, theme: Theme, text: str, console: Console, **kwargs: Any) -> None:
        super().__init__(theme)
        self.text = text
        self.console = console
        self.kwargs = kwargs

    def render(self, console: Console) -> None:
        """Confirms don't render - they return values."""
        pass

    def ask(self) -> bool:
        """Ask the user for confirmation."""
        return RichConfirm.ask(
            f"{self.theme.icons.warning} {self.text}",
            console=self.console,
            **self.kwargs,
        )


class SelectList(Component):
    """Select from list component."""

    component_type = "select_list"

    def __init__(
        self,
        theme: Theme,
        item_name: str,
        options: list[str],
        console: Console,
        default: str | None = None,
    ):
        self.theme = theme
        self.item_name = item_name
        self.options = options
        self.console = console
        self.default = default

    def render(self, console: Console) -> None:
        """Render the options list."""
        console.print(f"{self.theme.icons.info} Available {self.item_name}s:")
        for i, option in enumerate(self.options, 1):
            console.print(f"  {i}. {option}")

    def ask(self) -> str:
        """Ask the user to select an option."""
        prompt_text = f"Select a {self.item_name}"
        if self.default and self.default in self.options:
            default_index = self.options.index(self.default) + 1
            prompt_text += f" (default: {default_index})"
        else:
            default_index = None

        choice = RichPrompt.ask(
            f"{self.theme.icons.info} {prompt_text}",
            console=self.console,
            default=str(default_index) if default_index else None,
        )

        try:
            choice_num = int(choice) if choice is not None else 0
            if not 1 <= choice_num <= len(self.options):
                raise ValueError()
            return str(self.options[choice_num - 1])
        except (ValueError, TypeError) as exc:
            raise ValueError(
                f"Invalid selection. Please choose a number between 1 and {len(self.options)}."
            ) from exc
