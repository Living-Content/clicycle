"""Code display component."""

from __future__ import annotations

import json
from typing import Any

from rich.console import Console
from rich.syntax import Syntax

from clicycle.components.base import Component
from clicycle.theme import Theme


class Code(Component):
    """Code component for syntax-highlighted code display."""

    component_type = "code"

    def __init__(
        self,
        theme: Theme,
        code: str,
        language: str = "python",
        title: str | None = None,
        line_numbers: bool = True,
    ):
        super().__init__(theme)
        self.code = code
        self.language = language
        self.title = title
        self.line_numbers = line_numbers

    def render(self, console: Console) -> None:
        """Render syntax-highlighted code."""
        if self.title:
            console.print(f"[bold]{self.title}[/]")

        syntax = Syntax(
            self.code.strip(),
            self.language,
            theme="monokai",
            line_numbers=self.line_numbers,
            word_wrap=True,
        )
        console.print(syntax)


def json_code(theme: Theme, data: dict[str, Any], title: str | None = None) -> Code:
    """Create a Code component for JSON data."""
    return Code(
        theme,
        json.dumps(data, indent=2),
        language="json",
        title=title,
    )
