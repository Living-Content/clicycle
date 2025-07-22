#!/usr/bin/env python3
"""Basic usage example for Clicycle CLI framework."""

import time

from clicycle import Clicycle


def main():
    """Demonstrate basic Clicycle features."""
    # Create Clicycle instance with app branding
    cli = Clicycle(app_name="Demo App", width=100)

    # Clear terminal and show header
    cli.clear()
    cli.header("Clicycle Demo", "Basic features showcase")

    # Section: Messages
    cli.section("Message Types")
    cli.info("This is an informational message")
    cli.success("Operation completed successfully!")
    cli.warning("This is a warning message")
    cli.error("This is an error message")

    # Section: Lists
    cli.section("Lists")
    with cli.block():
        cli.info("Here are some list items:")
        cli.list_item("First item in the list")
        cli.list_item("Second item in the list")
        cli.list_item("Third item in the list")

    # Section: Data Display
    cli.section("Data Display")

    # Table example
    sample_data = [
        {"Name": "Alice Johnson", "Age": 30, "City": "New York", "Score": 95},
        {"Name": "Bob Smith", "Age": 25, "City": "San Francisco", "Score": 87},
        {"Name": "Charlie Brown", "Age": 35, "City": "Chicago", "Score": 92},
        {"Name": "Diana Wilson", "Age": 28, "City": "Boston", "Score": 98},
    ]
    cli.table(sample_data, title="User Performance Data")

    # Summary example
    summary_data = [
        {"label": "Total Users", "value": len(sample_data)},
        {
            "label": "Average Score",
            "value": f"{sum(item['Score'] for item in sample_data) / len(sample_data):.1f}",
        },
        {"label": "Highest Score", "value": max(item["Score"] for item in sample_data)},
        {"label": "Status", "value": "Active"},
    ]
    cli.summary(summary_data)

    # Section: Code Display
    cli.section("Code Examples")

    python_code = '''
def fibonacci(n):
    """Calculate the nth Fibonacci number."""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Example usage
for i in range(10):
    print(f"fib({i}) = {fibonacci(i)}")
'''
    cli.code(python_code, language="python", title="Fibonacci Function")

    # JSON example
    config_data = {
        "app_name": "demo_app",
        "version": "1.0.0",
        "settings": {
            "debug": False,
            "max_connections": 100,
            "features": ["logging", "caching", "monitoring"],
        },
    }
    cli.json(config_data, title="Configuration Example")

    # Section: Progress & Spinners
    cli.section("Progress Indicators")

    # Spinner example
    with cli.spinner("Loading data from API..."):
        time.sleep(2)
    cli.success("Data loaded successfully!")

    # Progress bar example
    with cli.progress("Processing files") as progress_cli:
        for i in range(101):
            progress_cli.update_progress(i, f"Processing file {i}/100")
            time.sleep(0.05)
    cli.success("All files processed!")

    # Section: Interactive Elements
    cli.section("Interactive Examples")

    cli.info("The following would be interactive in a real application:")
    cli.info("• name = cli.prompt('What is your name?')")
    cli.info("• confirmed = cli.confirm('Do you want to continue?')")
    cli.info("• choice = select_from_list_item('option', ['A', 'B', 'C'])")

    # Section: Suggestions
    cli.suggestions(
        [
            "Try modifying the theme colors",
            "Experiment with different table data",
            "Add your own progress indicators",
            "Create custom CLI applications",
        ]
    )


if __name__ == "__main__":
    main()
