"""Interactive select component with vertical arrow key navigation."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Any

from clicycle.interactive.base import _BaseRenderer

if TYPE_CHECKING:
    from clicycle import Clicycle


class _SelectRenderer(_BaseRenderer):
    """Renders the interactive select prompt."""

    def __init__(
        self,
        title: str,
        options: list[str | dict[str, Any]],
        default_index: int,
        cli: Clicycle,
    ) -> None:
        super().__init__(title, options, cli)
        self.current_index = default_index
        self.option_lines: list[int] = []
        self.total_lines = len(self.options)

    def _format_label(self, opt: dict[str, Any]) -> str:
        """Format label with special handling for 'Back' and 'Exit'."""
        label = opt.get("label", str(opt))
        if "← Back" in label:
            return "Back ←"
        if label == "Exit":
            return f"Exit {self.cli.theme.icons.error}"
        return str(label)

    def _setup_terminal(self) -> None:
        """Draw the initial menu and configure terminal."""
        if self.title:
            self.cli.console.print(f"\n{self.title}")
        self.cli.console.show_cursor(False)

        for i, option in enumerate(self.options):
            label = self._format_label(option)
            if i == self.current_index:
                sys.stdout.write(f"\033[32;1m→ {label}\033[0m\n")
            else:
                sys.stdout.write(f"  {label}\n")
        sys.stdout.flush()

        self.cursor_line = len(self.options)
        self.option_lines = list(range(len(self.options)))

    def _update_display(self, old_index: int) -> None:
        """Update the display after a selection change."""
        old_line_pos = self.option_lines[old_index]
        move = self.cursor_line - old_line_pos
        if move > 0:
            sys.stdout.write(f"\033[{move}A")

        sys.stdout.write("\r\033[2K")
        label = self._format_label(self.options[old_index])
        sys.stdout.write(f"  {label}")
        self.cursor_line = old_line_pos

        new_line_pos = self.option_lines[self.current_index]
        move = new_line_pos - self.cursor_line
        if move > 0:
            sys.stdout.write(f"\033[{move}B")
        elif move < 0:
            sys.stdout.write(f"\033[{-move}A")

        sys.stdout.write("\r\033[2K")
        label = self._format_label(self.options[self.current_index])
        sys.stdout.write(f"\033[32;1m→ {label}\033[0m")
        self.cursor_line = new_line_pos

        sys.stdout.flush()

    def _main_loop(self) -> None:
        """Handle user input and update display."""
        while True:
            key = self._get_key()
            old_current = self.current_index

            if key == "up" and self.current_index > 0:
                self.current_index -= 1
            elif key == "down" and self.current_index < len(self.options) - 1:
                self.current_index += 1
            elif key == "enter":
                self.selected_value = self.options[self.current_index].get(
                    "value", self.options[self.current_index].get("label")
                )
                break
            elif key == "quit":
                break
            else:
                continue

            self._update_display(old_current)


def interactive_select(
    title: str,
    options: list[str | dict[str, Any]],
    default_index: int = 0,
) -> Any:
    """Show an interactive select menu with arrow key navigation."""
    clicycle_module = sys.modules.get("clicycle")
    if clicycle_module is None:
        raise RuntimeError("clicycle module not imported")
    cli = getattr(clicycle_module, "_cli", None)
    if cli is None:
        raise RuntimeError("clicycle._cli not initialized")
    renderer = _SelectRenderer(title, options, default_index, cli)
    return renderer.render()
