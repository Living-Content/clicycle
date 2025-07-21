"""HTML-like CLI rendering system with self-spacing components."""

from __future__ import annotations

from abc import ABC, abstractmethod

from rich import table
from rich.console import Console
from rich.syntax import Syntax
from rich.text import Text as RichText

from .theme import Theme


class Component(ABC):
    """Base component class - like HTML elements with display behavior."""

    # Component type name for spacing lookups
    component_type: str = ""

    def __init__(self, theme: Theme):
        self.theme = theme

    def spacing_before(self, previous: Component | None) -> int:
        """How much space this component needs before itself."""
        if previous is None:
            return 0

        # Get spacing rules for this component type from theme
        spacing_rules = getattr(self.theme.spacing, self.component_type, {})

        if previous.component_type in spacing_rules:
            return spacing_rules[previous.component_type]
        return 1  # Default spacing

    @abstractmethod
    def render(self, console: Console) -> None:
        """Render the component content."""


class Header(Component):
    """Header component - like <h1> tag."""

    component_type = "header"

    def __init__(
        self,
        theme: Theme,
        title: str,
        subtitle: str | None = None,
        app_name: str | None = None,
    ):
        super().__init__(theme)
        self.title = title
        self.subtitle = subtitle
        self.app_name = app_name

    def render(self, console: Console) -> None:
        """Render header with optional app branding."""
        title_text = self.theme.transform_text(
            self.title,
            self.theme.typography.header_transform,
        )

        if self.app_name:
            app_branding = f"[bold cyan]{self.app_name}[/][bold white] / [/]"
            console.print(
                f"{app_branding}{RichText(title_text, style=self.theme.typography.header_style)}",
            )
        else:
            console.print(
                RichText(title_text, style=self.theme.typography.header_style),
            )

        if self.subtitle:
            subtitle_text = self.theme.transform_text(
                self.subtitle,
                self.theme.typography.subheader_transform,
            )
            console.print(
                RichText(subtitle_text, style=self.theme.typography.subheader_style),
            )


class Section(Component):
    """Section component - like <section> tag."""

    component_type = "section"

    def __init__(self, theme: Theme, title: str):
        super().__init__(theme)
        self.title = title

    def render(self, console: Console) -> None:
        """Render section with rule."""
        transformed_title = self.theme.transform_text(
            self.title,
            self.theme.typography.section_transform,
        )
        console.rule(
            f"[cyan]{transformed_title}[/]",
            style="dim bright_black",
            align="right",
        )


class Text(Component):
    """Text component - like <p> tag."""

    def __init__(self, theme: Theme, text: str, text_type: str = "info"):
        super().__init__(theme)
        self.text = text
        self.text_type = text_type
        # Dynamically set component_type for spacing rules
        self.component_type = text_type

    def render(self, console: Console) -> None:
        """Render message with appropriate icon and style."""
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

        if self.text_type == "list":
            icon = self.theme.icons.bullet
            style = self.theme.typography.info_style
        else:
            icon = icon_map.get(self.text_type, self.theme.icons.info)
            style = style_map.get(self.text_type, self.theme.typography.info_style)

        console.print(f"{icon} {self.text}", style=style)


class Table(Component):
    """Table component - like <table> tag."""

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

    def _create_base_table(self) -> table.Table:
        """Create the base table with theme styling."""
        rich_table = table.Table(
            box=self.theme.layout.table_box,
            border_style=self.theme.layout.table_border_style,
            show_header=True,
            header_style=f"bold {self.theme.typography.section_style}",
            expand=True,
        )

        if self.title:
            rich_table.title = f"[{self.theme.typography.label_style}]{self.title}[/]"

        return rich_table

    def _add_columns(self, rich_table: table.Table, headers: list[str]) -> None:
        """Add columns with smart styling based on header names."""
        for header in headers:
            if header in ["ID", "Port", "Replicas", "Projects", "Tenants"]:
                rich_table.add_column(
                    header,
                    justify="right",
                    no_wrap=True,
                    style="cyan",
                    width=8,
                )
            elif "Status" in header or "Health" in header:
                rich_table.add_column(header, justify="left", no_wrap=True, width=12)
            elif header == "Name":
                rich_table.add_column(header, style="bold", ratio=2)
            elif header == "Check":
                rich_table.add_column(header, ratio=2)
            elif header == "Message" or header == "Description":
                rich_table.add_column(header, ratio=4)
            elif header == "Frontend URL":
                rich_table.add_column(header, style="blue", ratio=3)
            elif header == "Environment":
                rich_table.add_column(header, width=12, no_wrap=True)
            elif header == "Cluster":
                rich_table.add_column(header, ratio=2)
            else:
                rich_table.add_column(header, ratio=1)

    def _add_rows(self, rich_table: table.Table) -> None:
        """Add data rows to the table."""
        for row in self.data:
            rich_table.add_row(*[str(v) for v in row.values()])

    def render(self, console: Console) -> None:
        """Render table with theme styling."""
        if not self.data:
            console.print(
                f"[{self.theme.typography.muted_style}]No data to display.[/]",
            )
            return

        rich_table = self._create_base_table()
        headers = list(self.data[0].keys())

        self._add_columns(rich_table, headers)
        self._add_rows(rich_table)

        console.print(rich_table)


class Code(Component):
    """Code component - like <pre> tag."""

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
        """Render code with syntax highlighting."""
        if self.title:
            console.print(RichText(self.title, style=self.theme.typography.label_style))

        padding = 0
        show_line_numbers = self.line_numbers

        # If line numbers are off, calculate padding to align code as if they were on
        if not self.line_numbers:
            # Count lines and calculate the width needed for the line number gutter.
            # Gutter width = number of digits in the last line number + padding for " │ "
            num_lines = self.code.count("\\n") + 1
            if num_lines > 0:
                gutter_width = len(str(num_lines)) + 4
                padding = (0, 0, 0, gutter_width)  # top, right, bottom, left

        syntax = Syntax(
            self.code,
            self.language,
            theme="monokai",
            line_numbers=show_line_numbers,
            background_color="default",
            word_wrap=True,
            padding=padding,
        )
        console.print(syntax, end="")


class Summary(Component):
    """Summary component - like <dl> tag."""

    component_type = "summary"

    def __init__(
        self, theme: Theme, data: list[dict[str, str | int | float | bool | None]]
    ):
        super().__init__(theme)
        self.data = data

    def render(self, console: Console) -> None:
        """Render key-value summary."""
        for item in self.data:
            label = item.get("label", "")
            value = item.get("value", "")
            console.print(
                f"[{self.theme.typography.label_style}]{label}:[/] "
                f"[{self.theme.typography.value_style}]{value}[/]",
            )


class Block(Component):
    """Block component - like <div> tag. Groups components with internal spacing control."""

    component_type = "block"

    def __init__(self, theme: Theme, components: list[Component]):
        super().__init__(theme)
        self.components = components

    def render(self, console: Console) -> None:
        """Render components with automatic nested block spacing."""
        # If we have nested blocks, use a temporary stream for proper spacing
        has_nested_blocks = any(isinstance(comp, Block) for comp in self.components)

        if has_nested_blocks:
            # Create a temporary stream for internal spacing between nested blocks
            temp_stream = RenderStream(console)
            for component in self.components:
                temp_stream.render(component)
        else:
            # Render without spacing between components
            for component in self.components:
                component.render(console)


class Spinner(Component):
    """Spinner component - indicates ongoing operation."""

    component_type = "spinner"

    def __init__(self, theme: Theme, message: str):
        super().__init__(theme)
        self.message = message

    def render(self, console: Console) -> None:
        """Render spinner message (actual spinner handled by context manager)."""
        # Just render the message - the actual spinner will be handled separately
        console.print(
            f"{self.theme.icons.running} {self.message}",
            style=self.theme.typography.info_style,
        )


class ProgressBar(Component):
    """Progress bar component - indicates ongoing operation with progress."""

    component_type = "progress"

    def __init__(self, theme: Theme, description: str):
        super().__init__(theme)
        self.description = description

    def render(self, console: Console) -> None:
        """Render progress description (actual progress bar handled by context manager)."""
        # Just render a placeholder - the actual progress bar will be handled separately
        console.print(
            f"{self.theme.icons.running} {self.description}",
            style=self.theme.typography.info_style,
        )


class Prompt(Component):
    """Prompt component - themed wrapper around click.prompt()."""

    component_type = "prompt"

    def __init__(self, theme: Theme, text: str, **kwargs):
        super().__init__(theme)
        self.text = text
        self.kwargs = kwargs

    def render(self, console: Console) -> None:
        """Render prompt - this will be called for spacing, then click.prompt() called separately."""
        # This component exists only for spacing - the actual prompt is handled by Clicycle.prompt()


class Confirm(Component):
    """Confirm component - themed wrapper around cli.confirm()."""

    component_type = "confirm"

    def __init__(self, theme: Theme, text: str, **kwargs):
        super().__init__(theme)
        self.text = text
        self.kwargs = kwargs

    def render(self, console: Console) -> None:
        """Render confirm - this will be called for spacing, then cli.confirm() called separately."""
        # This component exists only for spacing - the actual confirm is handled by Clicycle.confirm()


class List(Component):
    """List component for bullet-pointed items."""

    component_type = "list"

    def __init__(self, theme: Theme, items: list[str]):
        super().__init__(theme)
        self.items = items

    def render(self, console: Console) -> None:
        """Render bulleted list."""
        for item in self.items:
            bullet = self.theme.icons.bullet
            console.print(f"{bullet} {item}", style=self.theme.typography.info_style)


class RenderStream:
    """Manages component rendering with automatic spacing."""

    def __init__(self, console: Console):
        self.console = console
        self.history: list[Component] = []

    def render(self, component: Component) -> None:
        """Render component with automatic spacing."""
        # Component decides its own spacing
        spacing = component.spacing_before(self.last_component)
        if spacing > 0:
            self.console.print("\n" * spacing, end="")

        # Render the component
        component.render(self.console)

        # Update history
        self.history.append(component)

    @property
    def last_component(self) -> Component | None:
        """Get the last rendered component."""
        return self.history[-1] if self.history else None

    def clear_history(self) -> None:
        """Clear render history (for new logical sections)."""
        self.history.clear()
