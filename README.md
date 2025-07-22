# Clicycle

> A Python CLI framework with self-spacing components and Rich theming

**Clicycle** is a modern Python CLI framework that provides a simple functional API and powerful component-based system for building beautiful command-line interfaces.

It features automatic spacing, Rich theming, and an intuitive API that lets you focus on your application's logic instead of its presentation.

## Features

- **Simple Functional API** - Import and use functions directly (e.g., `clicycle.info()`).
- **Rich theming** - Comprehensive styling with icons, typography, and layout controls.
- **Automatic spacing** - Components manage their own spacing like HTML elements.
- **Component-based** - Familiar React/HTML-like API with composable components.
- **Type-safe** - Full type hints and IDE support.
- **Smart tables** - Automatically sized columns with intelligent formatting.
- **Code highlighting** - Syntax-highlighted code blocks with line numbers.
- **Progress tracking** - Built-in progress bars and spinners.
- **Interactive prompts** - Properly spaced input prompts and confirmations.

## Installation

```bash
pip install clicycle
```

## Quick Start

Get started in seconds with Clicycle's functional API.

```python
import clicycle
import time

# (Optional) Configure the app name and theme once
clicycle.configure(app_name="MyApp")

# Display a header
clicycle.header("Welcome", "Getting started with Clicycle")

# Show different message types
clicycle.info("This is an info message")
clicycle.success("Operation completed successfully!")
clicycle.warning("This is a warning")
clicycle.error("Something went wrong")

# Display a table
data = [
    {"Name": "Alice", "Age": 30, "City": "New York"},
    {"Name": "Bob", "Age": 25, "City": "San Francisco"},
]
clicycle.table(data, title="User Information")

# Show code with syntax highlighting
code_snippet = '''
def hello_world():
    print("Hello, Clicycle!")
'''
clicycle.code(code_snippet, language="python", title="Example Code")

# Use a spinner for long-running operations
with clicycle.spinner("Processing..."):
    time.sleep(2)

# Interactive prompts
name = clicycle.prompt("What's your name?")
if clicycle.confirm("Do you want to continue?"):
    clicycle.success(f"Great, let's proceed, {name}!")
```

## How to Use Clicycle

Clicycle offers two ways to build your CLI: a simple **functional API** for most use cases and an **object-oriented API** for advanced scenarios.

### 1. Functional API (Recommended)

This is the easiest way to use Clicycle. Simply import the functions you need and call them. A global `Clicycle` instance is managed for you.

#### Configuration

Call `clicycle.configure()` at the start of your app to set a global app name or theme.

```python
import clicycle
from clicycle import Theme

# Set a custom app name to appear in headers
clicycle.configure(app_name="My Awesome App")

# Or configure a full theme
custom_theme = Theme() # Fill with your theme options
clicycle.configure(theme=custom_theme)
```

#### Usage

```python
import clicycle

clicycle.header("My App")
clicycle.info("Starting process...")
```

### 2. Object-Oriented API

For advanced use cases, such as managing multiple, separate CLI outputs with different themes, you can instantiate the `Clicycle` class directly.

```python
from clicycle import Clicycle, Theme

# Create a custom instance for a specific task
reporter_theme = Theme() # Fill with your theme options
reporter_cli = Clicycle(theme=reporter_theme)

reporter_cli.info("Reporting task status...")

# Use the default API for other tasks
clicycle.info("This uses the default global instance.")
```

## Components

All components are available through the functional API.

### Headers and Sections

```python
import clicycle

# Main header with optional app branding
clicycle.header("Main Title", "Optional subtitle")

# Section dividers
clicycle.section("Configuration")
```

### Text Messages

```python
import clicycle

# Different message types with automatic icons
clicycle.info("Information message")
clicycle.success("Success message")
clicycle.warning("Warning message")
clicycle.error("Error message")
clicycle.debug("Debug message")  # Only shown in verbose mode

# List items
clicycle.list_item("First item")
clicycle.list_item("Second item")
```

### Tables

```python
import clicycle

data = [
    {"Name": "Alice", "Score": 95},
    {"Name": "Bob", "Score": 87},
]

# Simple table
clicycle.table(data)

# Table with title
clicycle.table(data, title="Test Results")
```

### Code Display

```python
import clicycle

# Python code with line numbers
clicycle.code('''
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
''', language="python", title="Fibonacci Function")

# JSON data
clicycle.json({"name": "Alice", "age": 30}, title="User Data")
```

### Progress and Spinners

```python
import clicycle
import time

# Simple spinner
with clicycle.spinner("Loading data..."):
    time.sleep(2)

# Progress bar
with clicycle.progress("Processing files") as p:
    for i in range(100):
        p.update_progress(i, f"Processing file {i}")
        time.sleep(0.02)
```

### Interactive Prompts

```python
import clicycle
from clicycle import select_from_list

# Basic prompts
name = clicycle.prompt("Enter your name")
age = clicycle.prompt("Enter your age", type=int)
confirmed = clicycle.confirm("Are you sure?")

# Selection from a list
option = select_from_list(
    item_name="environment",
    options=["development", "staging", "production"],
    default="development",
)
```

### Grouping with Blocks

```python
import clicycle

# Group related content
clicycle.section("User Information")
with clicycle.block():
    clicycle.info("Processing user data...")
    clicycle.success("User validated")
    clicycle.info("Creating profile...")
```

### Summary Data

```python
import clicycle

# Key-value summaries
summary_data = [
    {"label": "Total Files", "value": 1250},
    {"label": "Success Rate", "value": "96%"},
]
clicycle.summary(summary_data)
```

## Theming

Clicycle's theming is highly customizable. You can pass a `Theme` object to `clicycle.configure()` or a `Clicycle` instance.

```python
from clicycle import Theme, Icons, Typography, configure

# Create a custom theme
custom_theme = Theme(
    icons=Icons(
        success="✅",
        error="❌",
    ),
    typography=Typography(
        header_style="bold magenta",
        info_style="bold blue",
    )
)

# Apply the theme globally
configure(theme=custom_theme)

# Now all functional calls will use the new theme
clicycle.success("Theme updated successfully!")
```

## Advanced Usage

### Integration with Click

Clicycle works seamlessly with Click. The `debug` function automatically respects Click's verbose flag.

```python
import click
import clicycle

@click.command()
@click.option('--verbose', '-v', is_flag=True, help="Enable verbose output.")
def main(verbose):
    # This is a basic example. For robust integration,
    # you might pass the verbose flag through the click context object.
    if verbose:
        # A simple way to let clicycle know about verbosity
        # is to configure it or handle it in your logic.
        # For this example, we'll just print a warning message.
        clicycle.warning("Verbose mode enabled.")

    clicycle.configure(app_name="MyApp")
    clicycle.header("My Application", "Version 1.0")
    clicycle.info("Application started")
    clicycle.debug("This will only show if --verbose is used.")

if __name__ == '__main__':
    main()
```

You can access the verbose flag in your Click command by using the `click.get_current_context()` function.

```python
import click

@click.command()
@click.option('--verbose', '-v', is_flag=True, help="Enable verbose output.")
def main(verbose):
    context = click.get_current_context()
    if context.params.get('verbose'):
        clicycle.warning("Verbose mode enabled.")
        # more logic here
```

## API Reference

### Top-Level Functions

These functions are available for direct import from `clicycle`.

- `configure(app_name: str, theme: Theme)` - Configure the global instance.
- `header(title: str, subtitle: str, app_name: str)` - Display header.
- `section(title: str)` - Display section divider.
- `info/success/warning/error/debug(message: str)` - Display styled messages.
- `table(data: list[dict], title: str)` - Display data table.
- `code(code: str, language: str, title: str)` - Display code.
- `json(data: dict, title: str)` - Display JSON data.
- `summary(data: list[dict])` - Display key-value summary.
- `list_item(item: str)` - Display list item.
- `prompt(text: str, **kwargs)` - Interactive prompt.
- `confirm(text: str, **kwargs)` - Interactive confirmation.
- `spinner(message: str)` - Context manager for spinner.
- `progress(description: str)` - Context manager for progress bar.
- `block()` - Context manager for grouping components.
- `clear()` - Clear terminal and reset.

### Clicycle Class

For advanced use, you can create separate instances.

```python
from clicycle import Clicycle

cli = Clicycle(width: int = 100, theme: Theme | None = None, app_name: str | None = None)
```

The methods on the `Clicycle` class instance mirror the top-level functions.
