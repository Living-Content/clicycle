#!/usr/bin/env python3
"""Example showing all available components in clicycle."""

import time

import clicycle as cc

# Header with full information
cc.header("Clicycle Components", "Complete Reference", "Demo App")

# Text components
cc.section("Text Components")
cc.info("This is an info message - general information")
cc.success("This is a success message - operation completed")
cc.error("This is an error message - something went wrong")
cc.warning("This is a warning message - be careful")
cc.debug("This is a debug message - only shown in verbose mode")

# List items
cc.info("Here's a list of features:")
cc.list_item("Automatic spacing between components")
cc.list_item("Rich formatting and colors")
cc.list_item("Disappearing spinners")
cc.list_item("Progress bars with descriptions")

# Data display
cc.section("Data Display")

# Tables
users = [
    {"Name": "Alice Johnson", "Department": "Engineering", "Years": 5},
    {"Name": "Bob Smith", "Department": "Marketing", "Years": 3},
    {"Name": "Charlie Brown", "Department": "Sales", "Years": 7},
]
cc.table(users, title="Employee Directory")

# Code display
cc.code(
    """def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)""",
    language="python",
    title="Fibonacci Function",
)

# JSON display
config = {
    "app": {
        "name": "Clicycle Demo",
        "version": "2.0.0",
        "features": ["components", "themes", "spinners"],
    }
}
cc.json(config, title="Application Config")

# Summary data
cc.summary(
    [
        {"label": "Total Users", "value": 1250},
        {"label": "Active Sessions", "value": 342},
        {"label": "CPU Usage", "value": "45%"},
        {"label": "Memory", "value": "2.1 GB"},
    ]
)

# Progress indicators
cc.section("Progress Indicators")

# Spinner
cc.info("Regular spinner (message remains):")
with cc.spinner("Processing data..."):
    time.sleep(2)
cc.success("Processing complete!")

# Progress bar
cc.info("Progress bar with updates:")
with cc.progress("Downloading files") as prog:
    for i in range(101):
        prog.update(i, f"file_{i}.dat")
        time.sleep(0.02)
cc.success("Download complete!")

# Spacing demonstration
cc.section("Automatic Spacing")
cc.info("Components manage their own spacing.")
cc.info("Notice: no space between consecutive info messages.")
cc.info("This creates a clean, grouped appearance.")
cc.success("But different component types have appropriate spacing.")
cc.error("This error has space before it.")

# Clear example (commented out to not clear the demo)
# cc.clear()  # Would clear the screen

cc.section("Demo Complete")
cc.success("All components demonstrated!")
