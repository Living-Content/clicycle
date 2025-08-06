#!/usr/bin/env python3
"""Demonstrate input validation and error handling."""

from contextlib import suppress

import clicycle as cc

cc.header("Input Validation")

# Valid usage
cc.section("Valid Usage")
cc.success("Messages with proper string input work perfectly")
cc.info("The library validates inputs to catch errors early")

# Input validation examples
cc.section("Input Validation")

cc.info("Clicycle validates component inputs to prevent runtime errors:")

# Example 1: Type validation
cc.list_item("Type checking: Messages must be strings")
with suppress(TypeError):
    # This would fail:
    # cc.info(123)
    cc.error("❌ cc.info(123) → TypeError: Message must be a string")

# Example 2: Empty validation
cc.list_item("Non-empty: Messages cannot be empty strings")
with suppress(ValueError):
    # This would fail:
    # cc.info("")
    cc.error("❌ cc.info('') → ValueError: Message cannot be empty")

# Theme validation examples
cc.section("Theme Validation")

cc.info("Themes are validated to ensure proper configuration:")

# Example 1: Width validation
cc.list_item("Console width must be at least 20 characters")
with suppress(ValueError):
    # This would fail:
    # theme = Theme(width=10)
    cc.error("❌ Theme(width=10) → ValueError: Width must be >= 20")

# Example 2: Spinner validation
cc.list_item("Spinner types must be from the supported list")
valid_spinners = [
    "dots",
    "dots2",
    "dots3",
    "line",
    "star",
    "bouncingBar",
    "arc",
    "arrow",
]
cc.info(f"Valid spinners: {', '.join(valid_spinners)}")
with suppress(ValueError):
    # This would fail:
    # theme = Theme(spinner_type="invalid")
    cc.error("❌ Theme(spinner_type='invalid') → ValueError: Invalid spinner type")

# Best practices
cc.section("Best Practices")

cc.success("✓ Always pass strings to text components")
cc.success("✓ Validate user input before passing to components")
cc.success("✓ Use appropriate component types for your content")
cc.success("✓ Configure themes with valid parameters")

# Error recovery
cc.section("Error Recovery")

cc.info("When validation fails, Clicycle provides clear error messages:")


# Show a practical example
def safe_display(value):
    """Safely display a value with type checking."""
    try:
        cc.info(value)
    except TypeError as e:
        cc.error(f"Cannot display {type(value).__name__}: {e}")
    except ValueError as e:
        cc.error(f"Invalid value: {e}")


cc.info("Example: safe_display function")
safe_display("This works fine")
safe_display(123)  # This will show an error message
safe_display("")  # This will show an error message

cc.section("Summary")
cc.success(
    "Input validation helps catch errors early and provides better developer experience!"
)
