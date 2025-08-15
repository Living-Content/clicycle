"""Interactive multi-select component with vertical navigation and checkboxes."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Any

from clicycle.interactive.base import _BaseRenderer

if TYPE_CHECKING:
    from clicycle import Clicycle


class _MultiSelectRenderer(_BaseRenderer):
    """Renders the interactive multi-select prompt."""

    def __init__(
        self,
        title: str,
        options: list[str | dict[str, Any]],
        default_selected: list[int] | None,
        min_selection: int,
        max_selection: int | None,
        cli: Clicycle,
    ) -> None:
        super().__init__(title, options, cli)
        self.selected_indices = set(default_selected or [])
        self.min_selection = min_selection
        self.max_selection = max_selection
        self.option_lines: list[int] = []
        self.selected_values: list[Any] | None = None
        self.total_lines = len(self.options) + 1

    def _draw_line(self, index: int, is_current: bool) -> None:
        """Draw a single line (option or submit button)."""
        sys.stdout.write("\r\033[2K")
        if index < len(self.options):
            label = self.options[index].get("label", str(self.options[index]))
            checkbox = (
                f"[{self.cli.theme.icons.success}]"
                if index in self.selected_indices
                else "[ ]"
            )
            line = f"{checkbox} {label}"
        else:
            line = "[Submit]"

        if is_current:
            sys.stdout.write(f"\033[32;1m→ {line}\033[0m")
        else:
            sys.stdout.write(f"  {line}")

    def _update_display(self, old_index: int) -> None:
        """Update the display after a change."""
        self._move_cursor_to_line(old_index)
        self._draw_line(old_index, False)
        self._move_cursor_to_line(self.current_index)
        self._draw_line(self.current_index, True)
        sys.stdout.flush()

    def _toggle_selection(self) -> None:
        """Toggle selection for the current item."""
        if self.current_index in self.selected_indices:
            self.selected_indices.remove(self.current_index)
        elif (
            self.max_selection is None
            or len(self.selected_indices) < self.max_selection
        ):
            self.selected_indices.add(self.current_index)
        self._draw_line(self.current_index, True)
        sys.stdout.flush()

    def _setup_terminal(self) -> None:
        """Draw the initial menu and configure terminal."""
        if self.title:
            self.cli.console.print(f"\n{self.title}")
        self.cli.console.show_cursor(False)

        self.option_lines = list(range(len(self.options) + 1))
        for i in self.option_lines:
            self._draw_line(i, i == self.current_index)
            sys.stdout.write("\n")
        sys.stdout.flush()
        self.cursor_line = len(self.options) + 1

    def _move_cursor_to_line(self, target_index: int) -> None:
        target_line = self.option_lines[target_index]
        move = self.cursor_line - target_line
        if move > 0:
            sys.stdout.write(f"\033[{move}A")
        elif move < 0:
            sys.stdout.write(f"\033[{-move}B")
        self.cursor_line = target_line

    def _main_loop(self) -> None:
        """Handle user input and update display."""
        while True:
            key = self._get_key()
            old_current = self.current_index

            if key == "up" and self.current_index > 0:
                self.current_index -= 1
                self._update_display(old_current)
            elif key == "down" and self.current_index < len(self.options):
                self.current_index += 1
                self._update_display(old_current)
            elif key == "space" and self.current_index < len(self.options):
                self._toggle_selection()
            elif key == "enter" and self.current_index == len(self.options):
                if len(self.selected_indices) >= self.min_selection:
                    self.selected_values = [
                        self.options[i].get("value", self.options[i].get("label"))
                        for i in sorted(self.selected_indices)
                    ]
                    break
            elif key == "quit":
                self.selected_values = None
                break
        self.selected_value = self.selected_values


def interactive_multi_select(
    title: str,
    options: list[str | dict[str, Any]],
    default_selected: list[int] | None = None,
    min_selection: int = 0,
    max_selection: int | None = None,
) -> list[Any] | None:
    """Show an interactive multi-select menu with checkboxes."""
    clicycle_module = sys.modules.get("clicycle")
    if clicycle_module is None:
        raise RuntimeError("clicycle module not imported")
    cli = getattr(clicycle_module, "_cli", None)
    if cli is None:
        raise RuntimeError("clicycle._cli not initialized")
    renderer = _MultiSelectRenderer(
        title,
        options,
        default_selected,
        min_selection,
        max_selection,
        cli,
    )
    result = renderer.render()
    return result if isinstance(result, list) else None
