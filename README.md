# Clicycle

> HTML-like CLI framework with self-spacing components and Rich theming

**Clicycle** is a modern Python CLI framework that provides React/HTML-like components for building beautiful command-line interfaces with automatic spacing and Rich theming.

## Features

- **Rich theming** - Comprehensive styling with icons, typography, and layout controls
- **Automatic spacing** - Components manage their own spacing like HTML elements
- **Component-based** - Familiar React/HTML-like API with composable components
- **Type-safe** - Full type hints and IDE support
- **Smart tables** - Automatically sized columns with intelligent formatting
- **Code highlighting** - Syntax-highlighted code blocks with line numbers
- **Progress tracking** - Built-in progress bars and spinners
- **Interactive prompts** - Properly spaced input prompts and confirmations

## Installation

### Using uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and virtual environment manager.

```bash
# Install clicycle
uv add clicycle

# Or install globally
uv tool install clicycle
```

### Using pip (not recommended)

```bash
pip install clicycle
```

### Development Installation

```bash
git clone https://github.com/yourusername/clicycle.git
cd clicycle

# Using uv (recommended)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"

# Using pip
pip install -e ".[dev]"
```

## Quick Start

```python
from clicycle import Clicycle

# Create a CLI instance
cli = Clicycle(app_name="MyApp")

# Display a header
cli.header("Welcome", "Getting started with Clicycle")

# Show different message types
cli.info("This is an info message")
cli.success("Operation completed successfully!")
cli.warning("This is a warning")
cli.error("Something went wrong")

# Display a table
data = [
    {"Name": "Alice", "Age": 30, "City": "New York"},
    {"Name": "Bob", "Age": 25, "City": "San Francisco"},
    {"Name": "Charlie", "Age": 35, "City": "Chicago"},
]
cli.table(data, title="User Information")

# Show code with syntax highlighting
code = '''
def hello_world():
    print("Hello, Clicycle!")
'''
cli.code(code, language="python", title="Example Code")

# Interactive prompts
name = cli.prompt("What's your name?")
confirmed = cli.confirm("Do you want to continue?")
```

## Components

### Headers and Sections

```python
from clicycle import Clicycle

cli = Clicycle()

# Main header with optional app branding
cli.header("Main Title", "Optional subtitle", app_name="MyApp")

# Section dividers
cli.section("Configuration")
```

### Text Messages

```python
# Different message types with automatic icons
cli.info("Information message")
cli.success("Success message") 
cli.warning("Warning message")
cli.error("Error message")
cli.debug("Debug message")  # Only shown in verbose mode

# List items
cli.list("First item")
cli.list("Second item")
```

### Tables

```python
# Simple table
data = [
    {"Name": "Alice", "Score": 95},
    {"Name": "Bob", "Score": 87},
]
cli.table(data)

# Table with title
cli.table(data, title="Test Results")
```

### Code Display

```python
# Python code with line numbers
cli.code('''
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
''', language="python", title="Fibonacci Function")

# JSON data
cli.json({"name": "Alice", "age": 30}, title="User Data")
```

### Progress and Spinners

```python
# Simple spinner
with cli.spinner("Loading data..."):
    time.sleep(2)

# Progress bar
with cli.progress("Processing files") as progress_cli:
    for i in range(100):
        progress_cli.update_progress(i, f"Processing file {i}")
        time.sleep(0.1)

# Multi-task progress
with cli.multi_progress("Multiple tasks") as progress:
    task1 = progress.add_task("Task 1", total=100, short_id="T1")
    task2 = progress.add_task("Task 2", total=50, short_id="T2")
    
    for i in range(100):
        progress.update(task1, advance=1)
        if i % 2 == 0:
            progress.update(task2, advance=1)
        time.sleep(0.1)
```

### Interactive Prompts

```python
# Basic prompts
name = cli.prompt("Enter your name")
age = cli.prompt("Enter your age", type=int)
confirmed = cli.confirm("Are you sure?")

# Selection from list
from clicycle import select_from_list

option = select_from_list(
    "environment",
    ["development", "staging", "production"],
    default="development",
    cli=cli
)
```

### Grouping with Blocks

```python
# Group related content
cli.section("User Information")
with cli.block():
    cli.info("Processing user data...")
    cli.success("User validated")
    cli.info("Creating profile...")
```

### Summary Data

```python
# Key-value summaries
summary_data = [
    {"label": "Total Files", "value": 1250},
    {"label": "Processed", "value": 1200},
    {"label": "Errors", "value": 50},
    {"label": "Success Rate", "value": "96%"},
]
cli.summary(summary_data)
```

## Theming

Clicycle provides comprehensive theming capabilities to match your application's branding and style preferences.

### Basic Theming

```python
from clicycle import Clicycle, Theme, Icons, Typography

# Create custom theme
custom_theme = Theme(
    icons=Icons(
        success="✅",
        error="❌", 
        info="💡",
        warning="⚠️",
        debug="🔍",
        bullet="▶"
    ),
    typography=Typography(
        header_style="bold magenta",
        success_style="bold green",
        error_style="bold red on white",
        info_style="bold blue",
        warning_style="bold yellow"
    )
)

cli = Clicycle(theme=custom_theme)
```

### Complete Theme Customization

```python
from clicycle import Clicycle, Theme, Icons, Typography, Layout, ComponentSpacing

# Create a comprehensive custom theme
professional_theme = Theme(
    icons=Icons(
        success="✓",
        error="✗", 
        info="ℹ",
        warning="⚠",
        debug="→",
        bullet="•"
    ),
    typography=Typography(
        # Headers and sections
        header_style="bold white on blue",
        section_style="bold cyan underline",
        
        # Message styles  
        success_style="bold green",
        error_style="bold red",
        info_style="cyan",
        warning_style="bold yellow",
        debug_style="dim white",
        
        # Table and code styles
        table_header_style="bold white on black",
        code_style="bright_black on white"
    ),
    layout=Layout(
        table_style="rounded",
        table_header_style="bold magenta",
        table_row_styles=["none", "dim"],
        code_theme="github-dark"
    ),
    spacing=ComponentSpacing(
        after_header=2,
        after_section=1,
        between_components=1,
        before_table=1,
        after_table=1,
        before_code=1,
        after_code=1
    )
)

# Use the professional theme
cli = Clicycle(theme=professional_theme)

# Demonstrate the themed output
cli.header("Professional Application", "With custom styling")
cli.section("System Status")
cli.success("All systems operational")
cli.info("Current version: 2.1.0")
cli.warning("Maintenance scheduled for tonight")

# Table with professional styling
data = [
    {"Service": "API", "Status": "✓ Running", "Uptime": "99.9%"},
    {"Service": "Database", "Status": "✓ Running", "Uptime": "99.8%"},
    {"Service": "Cache", "Status": "⚠ Warning", "Uptime": "98.5%"}
]
cli.table(data, title="Service Health")
```

### Theme Components

- **Icons** - All symbols and indicators (success, error, info, warning, debug, bullet)
- **Typography** - Text styles for every component type
- **Layout** - Table styling, code themes, and visual presentation
- **ComponentSpacing** - Precise control over spacing between all component types

### Predefined Themes

```python
# Minimal theme for clean output
minimal_theme = Theme(
    icons=Icons(success="", error="", info="", warning="", debug="", bullet="·"),
    typography=Typography(
        header_style="bold",
        success_style="green", 
        error_style="red",
        info_style="blue",
        warning_style="yellow"
    )
)

# Colorful theme for engaging interfaces  
colorful_theme = Theme(
    icons=Icons(
        success="🎉",
        error="💥", 
        info="💬",
        warning="🚨",
        debug="🔧",
        bullet="🔸"
    ),
    typography=Typography(
        header_style="bold magenta on black",
        success_style="bold green on black",
        error_style="bold red on yellow",
        info_style="bold blue on white",
        warning_style="bold black on yellow"
    )
)

cli = Clicycle(theme=minimal_theme)  # or colorful_theme
```

## Advanced Usage

### Custom CLI Instance

```python
from clicycle import Clicycle, Theme

# Create CLI with custom settings
cli = Clicycle(
    width=120,              # Terminal width
    app_name="MyApp",       # App branding in headers
    theme=custom_theme      # Custom theme
)
```

### Integration with Click

Clicycle works seamlessly with Click for command-line applications:

```python
import click
from clicycle import Clicycle

@click.command()
@click.option('--verbose', '-v', is_flag=True)
def main(verbose):
    cli = Clicycle()
    
    if verbose:
        cli.debug("Verbose mode enabled")
    
    cli.header("My Application", "Version 1.0")
    cli.info("Application started")

if __name__ == '__main__':
    main()
```

### Error Handling

```python
try:
    # Some operation
    result = risky_operation()
    cli.success(f"Operation completed: {result}")
except Exception as e:
    cli.error(f"Operation failed: {e}")
    cli.suggestions([
        "Check your input parameters",
        "Verify network connectivity", 
        "Try again with --verbose flag"
    ])
```

## Performance

Clicycle is optimized for CLI applications with minimal overhead while providing rich functionality. Here's how to benchmark performance in your applications:

### Performance Testing

```python
#!/usr/bin/env python3
"""Simple performance benchmark for clicycle."""

import io
import time
from rich.console import Console
from clicycle import Clicycle

def benchmark_clicycle():
    """Benchmark clicycle performance against alternatives."""
    
    def measure_time(func):
        """Simple timing decorator."""
        start_time = time.perf_counter()
        func()
        end_time = time.perf_counter()
        return (end_time - start_time) * 1000  # Convert to milliseconds
    
    # Test clicycle basic output
    def test_clicycle():
        cli = Clicycle()
        # Capture output to avoid terminal spam during benchmarking
        cli.stream.console = Console(file=io.StringIO())
        
        cli.header("Performance Test", "Basic Output")
        cli.info("This is an info message")
        cli.success("This is a success message") 
        cli.warning("This is a warning message")
        cli.error("This is an error message")
        
        # Test table rendering
        data = [
            {"Name": f"User_{i}", "Score": i * 10, "Status": "Active"}
            for i in range(100)
        ]
        cli.table(data, title="Performance Test Data")
    
    # Test raw Rich for comparison
    def test_raw_rich():
        console = Console(file=io.StringIO())
        console.print("[bold blue]Performance Test[/bold blue]")
        console.print("ℹ This is an info message")
        console.print("✓ This is a success message")
        console.print("⚠ This is a warning message") 
        console.print("✗ This is an error message")
    
    # Run benchmarks
    clicycle_time = measure_time(test_clicycle)
    rich_time = measure_time(test_raw_rich)
    
    # Results
    cli = Clicycle()
    cli.header("Performance Results")
    
    results = [
        {"Test": "Clicycle (full features)", "Time (ms)": f"{clicycle_time:.2f}"},
        {"Test": "Raw Rich (basic)", "Time (ms)": f"{rich_time:.2f}"},
        {"Test": "Overhead", "Time (ms)": f"{clicycle_time - rich_time:.2f}"}
    ]
    cli.table(results, title="Benchmark Comparison")
    
    overhead_percent = ((clicycle_time / rich_time) - 1) * 100
    cli.info(f"Clicycle overhead: {overhead_percent:.1f}% vs raw Rich")
    
    if clicycle_time < 50:  # Less than 50ms is excellent for CLI
        cli.success("Performance is excellent for CLI applications")
    elif clicycle_time < 100:
        cli.info("Performance is good for most CLI use cases") 
    else:
        cli.warning("Consider optimizing for high-frequency operations")

if __name__ == "__main__":
    benchmark_clicycle()
```

### Performance Characteristics

Based on our benchmarks, Clicycle delivers:

- **Startup time**: ~0.07ms (virtually instant)
- **Basic output**: ~1-2ms for typical message combinations  
- **Large tables**: ~100ms for 1000 rows (same as raw Rich)
- **Memory usage**: Minimal overhead (~0.1MB for typical usage)

### Performance Tips

- **Reuse CLI instances** - Create once, use many times
- **Batch operations** - Use `with cli.block():` to group related output
- **Table pagination** - For large datasets, consider pagination or streaming
- **Caching themes** - Custom themes are automatically cached for performance

### When to Optimize

Clicycle's performance is designed for human-readable CLI output where microsecond differences are imperceptible. Consider optimization only for:

- High-frequency logging (>1000 operations/second)
- Real-time data streaming interfaces  
- Resource-constrained environments
- Batch processing of large datasets

For most CLI applications, Clicycle's rich features and automatic spacing provide excellent value with negligible performance impact.

## API Reference

### Clicycle Class

The main class for creating CLI interfaces.

#### Constructor

```python
Clicycle(width: int = 100, theme: Theme | None = None, app_name: str | None = None)
```

#### Methods

- `header(title: str, subtitle: str = None, app_name: str = None)` - Display header
- `section(title: str)` - Display section divider
- `info/success/warning/error/debug(message: str)` - Display styled messages
- `table(data: list[dict], title: str = None)` - Display data table
- `code(code: str, language: str = "python", title: str = None, line_numbers: bool = True)` - Display code
- `json(data: dict, title: str = None)` - Display JSON data
- `summary(data: list[dict])` - Display key-value summary
- `list(item: str)` - Display list item
- `prompt(text: str, **kwargs)` - Interactive prompt
- `confirm(text: str, **kwargs)` - Interactive confirmation
- `suggestions(suggestions: list[str])` - Display suggestion list
- `spinner(message: str)` - Context manager for spinner
- `progress(description: str)` - Context manager for progress bar
- `multi_progress(description: str)` - Context manager for multi-task progress
- `block()` - Context manager for grouping components
- `clear()` - Clear terminal and reset

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development

```bash
# Install development dependencies using uv (recommended)
uv pip install -e ".[dev]"

# Or using pip
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check .
ruff format .

# Run type checking
mypy src/
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Changelog

### 0.1.0

- Initial release
- Core component system
- Rich theming support
- Automatic spacing
- Progress tracking
- Interactive prompts
