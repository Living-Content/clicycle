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

    def __init__(self, theme: Theme, text: str, **kwargs: Any) -> None:
        super().__init__(theme)
        self.text = text
        self.kwargs = kwargs

    def render(self, console: Console) -> None:
        """Render the prompt and get input."""
        self.result = RichPrompt.ask(self.text, console=console, **self.kwargs)

    def ask(self) -> Any:
        """Return the result from render."""
        return getattr(self, "result", None)


class Confirm(Component):
    """Confirm component for yes/no questions."""

    component_type = "confirm"

    def __init__(self, theme: Theme, text: str, **kwargs: Any) -> None:
        super().__init__(theme)
        self.text = text
        self.kwargs = kwargs

    def render(self, console: Console) -> None:
        """Render the confirm and get input."""
        self.result = RichConfirm.ask(
            self.text,
            console=console,
            **self.kwargs,
        )

    def ask(self) -> bool:
        """Return the result from render."""
        return getattr(self, "result", False)


class SelectList(Component):
    """Select from list component."""

    component_type = "select_list"

    def __init__(
        self,
        theme: Theme,
        item_name: str,
        options: list[str],
        default: str | None = None,
    ):
        self.theme = theme
        self.item_name = item_name
        self.options = options
        self.default = default

    def render(self, console: Console) -> None:
        """Render the options list and get selection."""
        console.print(f"Available {self.item_name}s:")
        for i, option in enumerate(self.options, 1):
            console.print(f"  {i}. {option}")

        prompt_text = f"Select a {self.item_name}"
        if self.default and self.default in self.options:
            default_index = self.options.index(self.default) + 1
            prompt_text += f" (default: {default_index})"
        else:
            default_index = None

        choice = RichPrompt.ask(
            prompt_text,
            console=console,
            default=str(default_index) if default_index else None,
        )

        try:
            choice_num = int(choice) if choice is not None else 0
            if not 1 <= choice_num <= len(self.options):
                raise ValueError()
            self.result = str(self.options[choice_num - 1])
        except (ValueError, TypeError) as exc:
            raise ValueError(
                f"Invalid selection. Please choose a number between 1 and {len(self.options)}."
            ) from exc

    def ask(self) -> str:
        """Return the result from render."""
        return getattr(self, "result", "")
