#!/usr/bin/env python3
"""Demonstrate the group() context manager for controlling component spacing."""

import clicycle as cc

# Show normal spacing behavior
cc.header("Group Context Manager", "Control Component Spacing")

cc.section("Normal Spacing")
cc.info("By default, components have intelligent spacing:")
cc.info("Multiple info messages stay together")
cc.info("They form a visual group")
cc.success("But different types get spacing")
cc.warning("This helps with visual hierarchy")
cc.error("Each type is visually distinct")

# Demonstrate group() to remove spacing
cc.section("Grouped Components")
cc.info("The group() context manager removes spacing between components:")

with cc.group():
    cc.info("This is info")
    cc.success("This is success")
    cc.warning("This is warning")
    cc.error("This is error")

cc.info("Normal spacing resumes after the group.")

# Practical example: status report
cc.section("Practical Example: Status Report")

with cc.group():
    cc.info("System Status Report")
    cc.info("━" * 40)
    cc.success("Database: Connected")
    cc.success("API: Responding (45ms)")
    cc.warning("Cache: High memory usage (87%)")
    cc.success("Queue: 12 jobs pending")
    cc.error("Backup: Last run failed")
    cc.info("━" * 40)
    cc.info("Generated at: 2024-12-09 15:30:45")

cc.info("")
cc.info("The report above is tightly grouped for better readability.")

# Nested groups
cc.section("Nested Groups")
cc.info("Groups can contain mixed content:")

with cc.group():
    cc.header("Mini Report", "Compact View")
    cc.list_item("First item in the list")
    cc.list_item("Second item in the list")
    cc.list_item("Third item in the list")
    cc.info("Total: 42")
    cc.info("Completed: 38")
    cc.info("Pending: 4")

cc.success("Groups are useful for creating compact, related content blocks!")
