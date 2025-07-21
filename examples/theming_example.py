#!/usr/bin/env python3
"""Theming example for Clicycle CLI framework."""

from rich import box as rich_box

from clicycle import Clicycle, Icons, Layout, Theme, Typography


def demo_default_theme():
    """Demonstrate the default theme."""
    cli = Clicycle(app_name="Default")

    cli.header("Default Theme", "Built-in styling")
    cli.info("This uses the default Clicycle theme")
    cli.success("Clean and professional appearance")
    cli.warning("Consistent spacing and colors")

    data = [
        {"Feature": "Icons", "Status": "✔ Enabled"},
        {"Feature": "Colors", "Status": "✔ Enabled"},
    ]
    cli.table(data, title="Theme Features")


def demo_custom_theme():
    """Demonstrate a custom theme with emoji icons."""
    # Create custom theme with emoji icons
    emoji_theme = Theme(
        icons=Icons(
            success="✅",
            error="❌",
            info="💡",
            warning="⚠️",
            debug="🐛",
            running="🔄",
            bullet="🔸",
            event="📅",
            url="🔗",
            cached="⚡",
            fresh="✨",
        ),
        typography=Typography(
            header_style="bold magenta",
            success_style="bold green",
            error_style="bold red",
            warning_style="bold yellow",
            info_style="bold cyan",
            section_style="bold blue",
        ),
    )

    cli = Clicycle(theme=emoji_theme, app_name="Custom")

    cli.header("Custom Theme", "Emoji icons and custom colors")
    cli.info("This theme uses emoji icons")
    cli.success("Much more colorful and fun!")
    cli.warning("Custom typography styles")
    cli.error("Different visual personality")

    data = [
        {"Feature": "Emoji Icons", "Status": "✅ Active"},
        {"Feature": "Custom Colors", "Status": "✅ Active"},
        {"Feature": "Personality", "Status": "🎉 Fun"},
    ]
    cli.table(data, title="Custom Theme Features")


def demo_minimal_theme():
    """Demonstrate a minimal, text-only theme."""
    minimal_theme = Theme(
        icons=Icons(
            success="[OK]",
            error="[ERROR]",
            info="[INFO]",
            warning="[WARN]",
            debug="[DEBUG]",
            running="[...]",
            bullet="-",
            event="*",
        ),
        typography=Typography(
            header_style="bold",
            success_style="green",
            error_style="red",
            warning_style="yellow",
            info_style="default",
            section_style="bold",
        ),
        layout=Layout(
            table_box=rich_box.SIMPLE,
            table_border_style="dim",
        ),
    )

    cli = Clicycle(theme=minimal_theme, app_name="Minimal")

    cli.header("Minimal Theme", "Text-only, no fancy symbols")
    cli.info("Perfect for environments with limited Unicode support")
    cli.success("Clean and simple appearance")
    cli.warning("Focuses on readability")

    data = [
        {"Feature": "Text Icons", "Status": "[OK] Enabled"},
        {"Feature": "Simple Borders", "Status": "[OK] Enabled"},
        {"Feature": "High Compatibility", "Status": "[OK] Enabled"},
    ]
    cli.table(data, title="Minimal Theme Features")


def demo_corporate_theme():
    """Demonstrate a professional corporate theme."""
    corporate_theme = Theme(
        icons=Icons(
            success="✓",
            error="✗",
            info="i",
            warning="!",
            debug=">",
            running="→",
            bullet="•",
        ),
        typography=Typography(
            header_style="bold blue",
            subheader_style="dim blue",
            success_style="bold green",
            error_style="bold red",
            warning_style="bold bright_yellow",
            info_style="bright_blue",
            section_style="bold bright_blue",
            header_transform="title",  # Title case headers
            section_transform="none",  # No transformation for sections
        ),
        layout=Layout(
            table_box=rich_box.ROUNDED,
            table_border_style="blue",
        ),
    )

    cli = Clicycle(theme=corporate_theme, app_name="Corp Suite")

    cli.header(
        "corporate theme demonstration",
        "Professional appearance for business applications",
    )
    cli.info("Designed for corporate environments")
    cli.success("Professional color scheme")
    cli.warning("Clear visual hierarchy")

    data = [
        {"Metric": "Uptime", "Value": "99.9%", "Status": "✓"},
        {"Metric": "Performance", "Value": "Excellent", "Status": "✓"},
        {"Metric": "Security", "Value": "Compliant", "Status": "✓"},
    ]
    cli.table(data, title="System Metrics")


def main():
    """Run all theme demonstrations."""
    print("\n" + "=" * 80)
    print("CLICYCLE THEMING DEMONSTRATION")
    print("=" * 80)

    print("\n[1/4] Default Theme:")
    demo_default_theme()

    print("\n[2/4] Custom Emoji Theme:")
    demo_custom_theme()

    print("\n[3/4] Minimal Text Theme:")
    demo_minimal_theme()

    print("\n[4/4] Corporate Theme:")
    demo_corporate_theme()

    # Final summary using clicycle
    cli = Clicycle()
    cli.section("Summary")
    cli.success("Theme demonstration complete!")
    cli.info(
        "Create your own themes by customizing Icons, Typography, and Layout classes."
    )
    cli.suggestions(
        [
            "Experiment with different icon sets",
            "Try custom color schemes",
            "Mix and match theme components",
            "Create themes for different environments",
        ]
    )


if __name__ == "__main__":
    main()
