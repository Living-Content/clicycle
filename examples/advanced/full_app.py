#!/usr/bin/env python3
"""Complete showcase of all Clicycle components and features."""

import time

from clicycle import Clicycle, Theme
from clicycle.components.code import Code, json_code
from clicycle.components.header import Header
from clicycle.components.progress import ProgressBar
from clicycle.components.section import Section
from clicycle.components.spinner import Spinner
from clicycle.components.summary import Summary
from clicycle.components.table import Table
from clicycle.components.text import Debug, Error, Info, ListItem, Success, WarningText


def showcase_text_components(cli):
    """Demonstrate all text component types."""
    cli.stream.render(Section(cli.theme, "Text Components"))

    cli.stream.render(Info(cli.theme, "This is an info message"))
    cli.stream.render(Success(cli.theme, "This is a success message"))
    cli.stream.render(WarningText(cli.theme, "This is a warning message"))
    cli.stream.render(Error(cli.theme, "This is an error message"))
    cli.stream.render(
        Debug(cli.theme, "This is a debug message (only shown in verbose mode)")
    )

    # List items
    cli.stream.render(Info(cli.theme, "Here's a list:"))
    cli.stream.render(ListItem(cli.theme, "First item"))
    cli.stream.render(ListItem(cli.theme, "Second item"))
    cli.stream.render(ListItem(cli.theme, "Third item with a longer description"))


def showcase_headers_sections(cli):
    """Demonstrate headers and sections."""
    cli.stream.render(
        Header(
            cli.theme,
            "Main Application Title",
            "Version 2.0.0 - Complete Feature Showcase",
            "Clicycle Demo",
        )
    )

    cli.stream.render(Section(cli.theme, "Getting Started"))
    cli.stream.render(Info(cli.theme, "This section demonstrates headers and dividers"))

    cli.stream.render(Section(cli.theme, "Advanced Features"))
    cli.stream.render(
        Info(cli.theme, "Notice the automatic spacing between components")
    )


def showcase_tables(cli):
    """Demonstrate table rendering."""
    cli.stream.render(Section(cli.theme, "Tables"))

    # Simple table
    user_data = [
        {
            "Name": "Alice Johnson",
            "Age": 28,
            "Department": "Engineering",
            "Status": "Active",
        },
        {"Name": "Bob Smith", "Age": 34, "Department": "Marketing", "Status": "Active"},
        {
            "Name": "Charlie Brown",
            "Age": 22,
            "Department": "Sales",
            "Status": "Inactive",
        },
        {
            "Name": "Diana Prince",
            "Age": 31,
            "Department": "Engineering",
            "Status": "Active",
        },
    ]

    cli.stream.render(Table(cli.theme, user_data, title="Employee Directory"))

    # Table with mixed data types
    stats_data = [
        {"Metric": "Total Users", "Value": 1250, "Change": "+12.5%", "Status": "✅"},
        {"Metric": "Active Sessions", "Value": 342, "Change": "+5.2%", "Status": "✅"},
        {"Metric": "Error Rate", "Value": "0.02%", "Change": "-0.5%", "Status": "✅"},
        {"Metric": "Response Time", "Value": "142ms", "Change": "+8ms", "Status": "⚠️"},
    ]

    cli.stream.render(Table(cli.theme, stats_data, title="System Metrics"))


def showcase_code_components(cli):
    """Demonstrate code and JSON rendering."""
    cli.stream.render(Section(cli.theme, "Code Display"))

    # Python code
    python_code = '''def fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Example usage
for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")'''

    cli.stream.render(
        Code(
            cli.theme, python_code, language="python", title="Fibonacci Implementation"
        )
    )

    # JSON data
    config_data = {
        "app": {
            "name": "Clicycle Demo",
            "version": "2.0.0",
            "features": ["components", "themes", "spinners", "tables"],
            "settings": {"debug": False, "timeout": 30, "retries": 3},
        }
    }

    cli.stream.render(json_code(cli.theme, config_data, title="Configuration"))


def showcase_spinners(cli):
    """Demonstrate spinner functionality."""
    cli.stream.render(Section(cli.theme, "Spinners"))

    # Regular spinner
    cli.stream.render(
        Info(cli.theme, "Regular spinner (message remains after completion):")
    )
    spinner = Spinner(cli.theme, "Processing data...", cli.console)
    cli.stream.render(spinner)
    with spinner:
        time.sleep(2)

    cli.stream.render(Success(cli.theme, "Processing complete!"))

    # Different spinner styles
    spinner_styles = ["dots", "line", "star", "bouncingBar"]
    cli.stream.render(Info(cli.theme, "Different spinner styles:"))

    for style in spinner_styles:
        cli.theme.spinner_type = style
        spinner = Spinner(cli.theme, f"Testing {style} spinner...", cli.console)
        cli.stream.render(spinner)
        with spinner:
            time.sleep(1.5)


def showcase_disappearing_spinners(cli):
    """Demonstrate disappearing spinners."""
    cli.stream.render(Section(cli.theme, "Disappearing Spinners"))

    # Create new CLI with disappearing spinners
    theme = Theme(disappearing_spinners=True)
    cli2 = Clicycle(theme=theme)

    cli2.stream.render(
        Info(cli2.theme, "Disappearing spinner (message vanishes after completion):")
    )

    spinner = Spinner(cli2.theme, "This message will disappear...", cli2.console)
    cli2.stream.render(spinner)
    with spinner:
        time.sleep(2)

    cli2.stream.render(Success(cli2.theme, "Notice the spinner message is gone!"))

    # Nested spinners
    cli2.stream.render(Info(cli2.theme, "Nested disappearing spinners:"))

    spinner1 = Spinner(cli2.theme, "Outer operation...", cli2.console)
    cli2.stream.render(spinner1)
    with spinner1:
        time.sleep(1)
        cli2.stream.render(Info(cli2.theme, "Starting inner task"))

        spinner2 = Spinner(cli2.theme, "Inner operation...", cli2.console)
        cli2.stream.render(spinner2)
        with spinner2:
            time.sleep(1)

        cli2.stream.render(Info(cli2.theme, "Inner task complete"))
        time.sleep(1)

    cli2.stream.render(Success(cli2.theme, "All operations complete!"))


def showcase_progress_bars(cli):
    """Demonstrate progress bar functionality."""
    cli.stream.render(Section(cli.theme, "Progress Bars"))

    # Simple progress bar
    progress = ProgressBar(cli.theme, "Downloading files", cli.console)
    cli.stream.render(progress)

    with progress.track() as prog:
        for i in range(101):
            prog.update(i, f"Processing file_{i}.dat")
            time.sleep(0.02)

    cli.stream.render(Success(cli.theme, "Download complete!"))

    # Multiple progress bars
    cli.stream.render(Info(cli.theme, "Processing multiple tasks:"))

    tasks = ["Parsing", "Analyzing", "Optimizing"]
    for task in tasks:
        progress = ProgressBar(cli.theme, task, cli.console)
        cli.stream.render(progress)

        with progress.track() as prog:
            for i in range(101):
                prog.update(i)
                time.sleep(0.01)

        cli.stream.render(Success(cli.theme, f"{task} complete"))


def showcase_summary_component(cli):
    """Demonstrate summary component."""
    cli.stream.render(Section(cli.theme, "Summary Component"))

    summary_data = [
        {"label": "Total Files", "value": 1250},
        {"label": "Processed", "value": 1248},
        {"label": "Failed", "value": 2},
        {"label": "Success Rate", "value": "99.84%"},
        {"label": "Processing Time", "value": "2m 34s"},
        {"label": "Average Speed", "value": "8.1 files/sec"},
    ]

    cli.stream.render(Summary(cli.theme, summary_data))


def showcase_spacing_behavior(cli):
    """Demonstrate automatic spacing behavior."""
    cli.stream.render(Section(cli.theme, "Automatic Spacing"))

    cli.stream.render(Info(cli.theme, "Components automatically manage their spacing."))
    cli.stream.render(
        Info(cli.theme, "Notice: no space between consecutive info messages.")
    )
    cli.stream.render(Info(cli.theme, "This creates a clean, grouped appearance."))

    cli.stream.render(
        Success(cli.theme, "But different component types have appropriate spacing.")
    )

    cli.stream.render(Error(cli.theme, "This error has space before it."))

    cli.stream.render(Section(cli.theme, "New Section"))

    cli.stream.render(
        Info(cli.theme, "Sections always have proper spacing from previous content.")
    )


def main():
    """Run the complete showcase."""
    # Create CLI instance
    cli = Clicycle(app_name="Clicycle Showcase")

    # Run all showcases
    showcase_headers_sections(cli)
    time.sleep(1)

    showcase_text_components(cli)
    time.sleep(1)

    showcase_tables(cli)
    time.sleep(1)

    showcase_code_components(cli)
    time.sleep(1)

    showcase_spinners(cli)
    time.sleep(1)

    showcase_disappearing_spinners(cli)
    time.sleep(1)

    showcase_progress_bars(cli)
    time.sleep(1)

    showcase_summary_component(cli)
    time.sleep(1)

    showcase_spacing_behavior(cli)

    # Final summary
    cli.stream.render(Section(cli.theme, "Showcase Complete"))
    cli.stream.render(Success(cli.theme, "All components demonstrated successfully!"))
    cli.stream.render(
        Info(cli.theme, "Explore the examples directory for more specific use cases.")
    )


if __name__ == "__main__":
    main()
