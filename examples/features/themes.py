#!/usr/bin/env python3
"""Example showing theme customization in clicycle."""

import clicycle as cc
from clicycle import Icons, Theme, Typography

# Create a custom theme with emojis
emoji_theme = Theme(
    icons=Icons(
        success="✅",
        error="❌",
        warning="⚠️",
        info="📌",
        bullet="👉",
        running="🔄",
        debug="🐛",
    ),
    typography=Typography(
        header_style="bold magenta",
        section_style="bold yellow",
        success_style="bold green",
        error_style="bold red on dark_red",
        warning_style="bold yellow",
        info_style="bright_blue",
    ),
    spinner_type="star",
)

# Apply the custom theme
cc.configure(theme=emoji_theme)

# Demo the custom theme
cc.header("Custom Theme Demo", "With Emojis! 🎨")

cc.section("Custom Icons")
cc.info("Notice the custom info icon")
cc.success("Success with emoji!")
cc.warning("Warning looks different")
cc.error("Error with background color")

cc.list_item("Custom bullet point")
cc.list_item("Another item with emoji bullet")

# Create a minimal theme
minimal_theme = Theme(
    icons=Icons(
        success=">",
        error="!",
        warning="?",
        info="-",
        bullet="*",
    ),
    typography=Typography(
        header_style="bold",
        section_style="underline",
        success_style="green",
        error_style="red",
        warning_style="yellow",
        info_style="white",
    ),
)

# Switch to minimal theme
cc.configure(theme=minimal_theme)

cc.section("Minimal Theme")
cc.info("Clean and simple")
cc.success("No emojis, just text")
cc.warning("Minimal styling")
cc.error("Basic colors only")

# Create a matrix-style theme
matrix_theme = Theme(
    icons=Icons(
        success="[OK]",
        error="[ERR]",
        warning="[WRN]",
        info="[INF]",
        bullet=">",
        running="...",
    ),
    typography=Typography(
        header_style="bold green",
        section_style="green",
        success_style="bright_green",
        error_style="bright_red",
        warning_style="bright_yellow",
        info_style="green",
        muted_style="dark_green",
    ),
    spinner_type="line",
)

cc.configure(theme=matrix_theme)

cc.section("Matrix Theme")
cc.info("System status: operational")
cc.success("Connection established")
cc.warning("Anomaly detected")
cc.error("Access denied")

# Show theme data in a table
cc.table(
    [
        {
            "Theme": "Emoji",
            "Style": "Fun and colorful",
            "Use Case": "User-friendly CLIs",
        },
        {
            "Theme": "Minimal",
            "Style": "Clean and simple",
            "Use Case": "Professional tools",
        },
        {"Theme": "Matrix", "Style": "Technical", "Use Case": "System utilities"},
    ],
    title="Theme Comparison",
)

cc.success("Theme demonstration complete!")
