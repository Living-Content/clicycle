"""Summary component for key-value displays."""

from __future__ import annotations

from rich.console import Console
from rich.table import Table

from clicycle.components.base import Component
from clicycle.theme import Theme


class Summary(Component):
    """Summary component for displaying key-value pairs."""

    component_type = "summary"

    def __init__(
        self,
        theme: Theme,
        data: list[dict[str, str | int | float | bool | None]],
    ):
        super().__init__(theme)
        self.data = data

    def render(self, console: Console) -> None:
        """Render summary as a key-value table."""
        if not self.data:
            return

        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column(style=self.theme.typography.label_style)
        table.add_column(style=self.theme.typography.value_style)

        for item in self.data:
            label = str(item.get("label", ""))
            value = str(item.get("value", ""))
            table.add_row(label, value)

        console.print(table)
