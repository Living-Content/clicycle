#!/usr/bin/env python3
"""Quick start example for clicycle."""

import time

import clicycle as cc

# Simple usage
cc.header("My CLI App", "v1.0.0")

cc.info("Starting application...")

# Show progress with a spinner
with cc.spinner("Loading configuration..."):
    time.sleep(2)

cc.success("Configuration loaded!")

# Display some data
cc.section("User Data")
users = [
    {"Name": "Alice", "Role": "Admin", "Active": True},
    {"Name": "Bob", "Role": "User", "Active": True},
    {"Name": "Charlie", "Role": "User", "Active": False},
]
cc.table(users)

# Show statistics
cc.info(f"Total Users: {len(users)}")
cc.info(f"Active Users: {sum(1 for u in users if u['Active'])}")

# Final message
cc.success("Application ready!")
