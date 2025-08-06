#!/usr/bin/env python3
"""Example showing disappearing spinners functionality."""

import time

import clicycle as cc

cc.header("Disappearing Spinners Demo")

# Regular spinners first
cc.section("Regular Spinners")
cc.info("Regular spinners leave their message visible after completion:")

with cc.spinner("Loading configuration..."):
    time.sleep(2)

with cc.spinner("Connecting to database..."):
    time.sleep(1.5)

with cc.spinner("Fetching user data..."):
    time.sleep(1)

cc.success("All tasks completed - notice the spinner messages above remain visible")

# Configure for disappearing spinners
cc.configure(theme=cc.Theme(disappearing_spinners=True))

cc.section("Disappearing Spinners")
cc.info("Now spinners will completely vanish when done:")

with cc.spinner("Loading configuration..."):
    time.sleep(2)

with cc.spinner("Connecting to database..."):
    time.sleep(1.5)

with cc.spinner("Fetching user data..."):
    time.sleep(1)

cc.success("All tasks completed - notice the spinner messages are gone!")

# Practical example
cc.section("Practical Example")

with cc.spinner("Initializing application..."):
    time.sleep(1)

cc.info("Configuration loaded from config.yml")

with cc.spinner("Connecting to services..."):
    time.sleep(2)
    services = ["Database", "Redis", "Message Queue", "API Gateway"]

cc.success("Connected to all services")
cc.table([{"Service": s, "Status": "Connected"} for s in services])

# Nested operations
cc.section("Nested Operations")

with cc.spinner("Processing batch job..."):
    time.sleep(1)

    cc.info("Processing 3 files...")

    for i in range(3):
        with cc.spinner(f"Processing file_{i + 1}.csv..."):
            time.sleep(1)
        cc.success(f"file_{i + 1}.csv processed")

    time.sleep(1)

cc.success("Batch job completed!")

# Show the results
cc.section("Results")
cc.info("Disappearing spinners are great for:")
cc.list_item("Keeping output clean and focused")
cc.list_item("Temporary status messages that don't need to persist")
cc.list_item("Reducing visual clutter in logs")
cc.list_item("Professional, polished CLI output")

cc.success("Demo complete!")
