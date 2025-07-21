# Clicycle Examples

This directory contains example scripts demonstrating various features and use cases of the Clicycle CLI framework.

## Running the Examples

Make sure you have Clicycle installed (see [README](../README.md))

Then run any example:

```bash
python examples/basic_usage.py
python examples/theming_example.py
python examples/click_integration.py --help
```

## Available Examples

### 1. Basic Usage (`basic_usage.py`)

**What it shows:** Core Clicycle components in action
**Run with:** `python examples/basic_usage.py`

Demonstrates:

- Headers and sections
- Message types (info, success, warning, error)
- Data tables and summaries
- Code highlighting and JSON formatting
- Progress bars and spinners

### 2. Theming (`theming_example.py`)

**What it shows:** How to customize Clicycle's appearance
**Run with:** `python examples/theming_example.py`

Demonstrates:

- Default theme
- Custom emoji theme
- Minimal text-only theme
- Corporate professional theme

### 3. Click Integration (`click_integration.py`)

**What it shows:** Full CLI application combining Click and Clicycle
**Run with:** `python examples/click_integration.py --help`

Try these commands:

```bash
python examples/click_integration.py status
```

```bash
python examples/click_integration.py process -i /input -o /output --dry-run
```

```bash
python examples/click_integration.py validate -p /some/path
```

```bash
python examples/click_integration.py report --format json
```

## What to Look For

When running the examples, pay attention to:

- **Automatic spacing** between components
- **Consistent styling** across different message types
- **Smart table formatting** that adapts to content
- **Progress feedback** during long operations
- **Theme customization** possibilities
