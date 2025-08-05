"""Unified CLI theme configuration for Clicycle."""

from __future__ import annotations

from dataclasses import dataclass, field

from rich import box as rich_box


@dataclass
class Icons:
    """Icon set for CLI - clean text symbols instead of emojis."""

    # Core status icons
    success: str = "✔"
    error: str = "✖"
    warning: str = "⚠"
    info: str = "ℹ"

    # Progress and activity
    running: str = "→"
    waiting: str = "…"

    # Operations
    sync: str = "⟳"

    # Objects
    event: str = "◆"
    artist: str = "♪"
    image: str = "▣"
    url: str = "⎘"
    time: str = "◷"
    location: str = "◉"

    # Status indicators
    cached: str = "⚡"
    fresh: str = "✧"
    failed: str = "✖"
    debug: str = "›"

    # General
    bullet: str = "•"
    arrow_right: str = "→"
    arrow_left: str = "←"
    arrow_down: str = "↓"
    arrow_up: str = "↑"


@dataclass
class Typography:
    """Typography styles for different text elements."""

    # Headers
    header_style: str = "bold white"
    header_transform: str = "upper"  # upper, lower, title, none

    subheader_style: str = "dim white"
    subheader_transform: str = "none"

    # Sections
    section_style: str = "bold bright_blue"
    section_transform: str = "upper"
    section_underline: str = "─"  # Character to repeat for underline

    # Labels and values
    label_style: str = "bold"
    value_style: str = "default"

    # Status messages
    success_style: str = "bold green"
    error_style: str = "bold red"
    warning_style: str = "bold yellow"
    info_style: str = "cyan"
    debug_style: str = "dim cyan"

    # Other text
    muted_style: str = "bright_black"
    dim_style: str = "dim"


@dataclass
class Layout:
    """Layout configuration."""

    # Table
    table_box: rich_box.Box = field(default_factory=lambda: rich_box.HEAVY_HEAD)
    table_border_style: str = "bright_black"

    # URL display
    url_style: str = "full"  # "full", "domain", "compact"


@dataclass
class ComponentSpacing:
    """Spacing rules for components - defaults to 1, only specify exceptions."""

    info: dict[str, int] = field(default_factory=lambda: {"info": 0})
    debug: dict[str, int] = field(default_factory=lambda: {"debug": 0})
    code: dict[str, int] = field(
        default_factory=lambda: {
            "info": 0,
            "code": 0,
        }
    )
    list_item: dict[str, int] = field(
        default_factory=lambda: {
            "info": 0,
            "debug": 0,
            "list_item": 0,
        }
    )


@dataclass
class ComponentIndentation:
    """Indentation rules for components - number of spaces per text type."""

    info: int = 0
    success: int = 0
    error: int = 0
    warning: int = 0
    debug: int = 0
    list_item: int = 2  # list_item defaults to two spaces


@dataclass
class Theme:
    """Complete theme configuration."""

    icons: Icons = field(default_factory=Icons)
    typography: Typography = field(default_factory=Typography)
    layout: Layout = field(default_factory=Layout)
    spacing: ComponentSpacing = field(default_factory=ComponentSpacing)
    indentation: ComponentIndentation = field(default_factory=ComponentIndentation)

    # Layout basics
    width: int = 100
    indent: str = "  "

    # Spinner behavior
    disappearing_spinners: bool = False
    spinner_type: str = (
        "dots"  # Rich spinner types: dots, dots2, dots3, line, bouncingBar, etc.
    )

    # Performance optimization: cached formatted styles
    _style_cache: dict[str, str] = field(default_factory=dict, init=False, repr=False)

    def __post_init__(self) -> None:
        """Pre-compute and cache frequently used style combinations."""
        self._style_cache.update(
            {
                "info_icon": f"{self.icons.info} ",
                "success_icon": f"{self.icons.success} ",
                "warning_icon": f"{self.icons.warning} ",
                "error_icon": f"{self.icons.error} ",
                "debug_icon": f"{self.icons.debug} ",
                "bullet_icon": f"{self.icons.bullet} ",
            }
        )

    def transform_text(self, text: str, transform: str) -> str:
        """Apply text transformation."""
        if transform == "upper":
            return text.upper()
        if transform == "lower":
            return text.lower()
        if transform == "title":
            return text.title()
        return text
