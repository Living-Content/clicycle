#!/usr/bin/env python3
"""Interactive menu system to run clicycle examples.

This menu demonstrates the interactive select functionality by creating a
hierarchical navigation system. It scans the examples directory for organized
categories and presents them using the vertical arrow-key navigation.

Features:
- Auto-discovery of example files from organized directories
- Category-based organization (basics/, features/, advanced/)
- Description extraction from docstrings
- Clean navigation without screen clearing issues
- Proper handling of interrupts and errors
- Subprocess execution of selected examples

Usage:
    python examples/menu.py

Navigation:
- Use ↑/↓ arrows to navigate
- Enter to select
- q or Ctrl+C to cancel/exit
- Automatically returns to previous menu levels

Directory Structure Expected:
    examples/
    ├── menu.py (this file)
    ├── basics/
    │   ├── hello.py
    │   └── colors.py
    ├── features/
    │   ├── spinners.py
    │   └── themes.py
    └── advanced/
        └── complex.py

Example Integration:
This menu showcases how to build hierarchical interfaces using clicycle's
interactive components, including proper error handling and clean transitions
between menu levels.
"""

import ast
import subprocess
import sys
import termios
from contextlib import suppress
from pathlib import Path

import clicycle as cc


def get_docstring_from_file(py_file: Path) -> str:
    """Extract the first line of the module docstring from a Python file."""
    try:
        with py_file.open("r", encoding="utf-8") as f:
            content = f.read()
        tree = ast.parse(content)
        docstring = ast.get_docstring(tree)
        if docstring:
            return docstring.strip().split("\n")[0]
    except (OSError, SyntaxError):
        # Ignore errors for files that can't be read or parsed.
        pass
    return "No description"


def get_examples():
    """Find all example files organized by category."""
    examples_dir = Path(__file__).parent
    categories = {}

    # Scan each category
    for category_dir in ["basics", "features", "advanced"]:
        category_path = examples_dir / category_dir
        if category_path.exists():
            examples = []
            for py_file in sorted(category_path.glob("*.py")):
                examples.append(
                    {
                        "name": py_file.stem.replace("_", " ").title(),
                        "file": py_file,
                        "description": get_docstring_from_file(py_file),
                    }
                )

            if examples:
                categories[category_dir.title()] = examples

    return categories


def select_category(categories):
    """Select a category from the menu."""
    category_options = [
        {"label": name, "value": name, "description": f"{len(examples)} examples"}
        for name, examples in categories.items()
    ]
    category_options.append(
        {"label": "Exit", "value": None, "description": "Quit the menu"}
    )

    try:
        return cc.select("", category_options)
    except KeyboardInterrupt:
        print()  # New line after potential ^C
        cc.warning("Menu cancelled")
        return "EXIT"


def select_example(examples):
    """Select an example from a category."""
    example_options = [
        {
            "label": ex["name"],
            "value": str(ex["file"]),
            "description": ex["description"],
        }
        for ex in examples
    ]
    example_options.append(
        {"label": "← Back", "value": None, "description": "Return to categories"}
    )

    try:
        return cc.select("", example_options)
    except KeyboardInterrupt:
        print()  # New line after potential ^C
        return None


def run_example(selected_example):
    """Run the selected example."""
    cc.section(f"Running: {Path(selected_example).name}")
    cc.info("Press Ctrl+C to stop the example")

    try:
        subprocess.run([sys.executable, selected_example], check=True)
        cc.success("Example completed!")
    except KeyboardInterrupt:
        # Clear the ^C that appears in terminal
        print()  # New line after ^C
        cc.warning("Example interrupted")
    except Exception as e:
        cc.error(f"Failed to run example: {e}")

    # Pause before returning to menu
    try:
        cc.info("Press Enter to continue...")
        # Flush stdin to clear any buffered arrow key sequences
        with suppress(ImportError, OSError):
            termios.tcflush(sys.stdin, termios.TCIFLUSH)
        input()
    except KeyboardInterrupt:
        # User hit Ctrl+C at the prompt
        print()  # New line after ^C


def main():
    """Run the example menu."""
    while True:
        # Get categories and examples
        categories = get_examples()

        if not categories:
            cc.error("No examples found!")
            break

        # Choose category
        selected_category = select_category(categories)

        if selected_category == "EXIT":
            break

        if selected_category is None:
            cc.info("Goodbye!")
            break

        # Choose example from category
        examples = categories[selected_category]
        selected_example = select_example(examples)

        if selected_example is None:
            continue

        # Run the example
        run_example(selected_example)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cc.warning("Menu interrupted")
    except Exception as e:
        cc.error(f"Menu error: {e}")
