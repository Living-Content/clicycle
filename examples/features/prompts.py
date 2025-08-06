#!/usr/bin/env python
"""Example demonstrating prompt components in Clicycle."""

import clicycle as cc

# Clear the console and show header
cc.clear()
cc.header("PROMPT COMPONENTS DEMO", subtitle="Interactive user input examples")

# Basic text prompt
cc.section("TEXT PROMPT")
cc.info("Enter your name for a personalized greeting")
name = cc.prompt("What is your name?")
cc.success(f"Hello, {name}! Welcome to Clicycle!")

# Confirmation prompt
cc.section("CONFIRMATION PROMPT")
cc.info("Let's test a yes/no confirmation")
if cc.confirm("Do you like Python?"):
    cc.success("Great choice! Python is awesome!")
else:
    cc.warning("That's okay, everyone has their preferences!")

# Select from list
cc.section("SELECT FROM LIST")
cc.info("Choose your favorite programming language")
languages = ["Python", "JavaScript", "Go", "Rust", "TypeScript"]
choice = cc.select_list("language", languages, default="Python")
cc.success(f"You selected: {choice}")

# Password prompt (using Rich's features)
cc.section("PASSWORD PROMPT")
cc.info("Prompts can also handle passwords securely")
password = cc.prompt("Enter a password", password=True)
cc.success(f"Password received (length: {len(password)} characters)")

# Prompt with default value
cc.section("PROMPT WITH DEFAULT")
cc.info("Press Enter to use the default value")
color = cc.prompt("What's your favorite color?", default="blue")
cc.success(f"Your favorite color is: {color}")

# Multiple confirmations
cc.section("MULTIPLE CONFIRMATIONS")
cc.info("Let's gather some preferences")
preferences = {
    "dark_mode": cc.confirm("Enable dark mode?", default=True),
    "notifications": cc.confirm("Enable notifications?", default=False),
    "auto_save": cc.confirm("Enable auto-save?", default=True),
}

cc.info("Your preferences:")
for key, value in preferences.items():
    status = "Enabled" if value else "Disabled"
    cc.list_item(f"{key.replace('_', ' ').title()}: {status}")

cc.success("All prompts completed successfully!")
