"""Table component for displaying structured data."""

from __future__ import annotations

from rich.console import Console
from rich.table import Table as RichTable

from clicycle.components.base import Component
from clicycle.theme import Theme


class Table(Component):
    """Table component - displays data in tabular format."""

    component_type = "table"

    def __init__(
        self,
        theme: Theme,
        data: list[dict[str, str | int | float | bool | None]],
        title: str | None = None,
    ):
        super().__init__(theme)
        self.data = data
        self.title = title

    def render(self, console: Console) -> None:
        """Render data as a table."""
        if not self.data:
            return

        table = RichTable(
            title=self.title,
            box=self.theme.layout.table_box,
            border_style=self.theme.layout.table_border_style,
            title_style=self.theme.typography.header_style,
            header_style=self.theme.typography.label_style,
        )

        # Add columns
        for key in self.data[0]:
            table.add_column(str(key))

        # Add rows
        for row in self.data:
            table.add_row(*[str(row.get(key, "")) for key in self.data[0]])

        console.print(table)
