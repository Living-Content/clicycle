#!/usr/bin/env python3
"""Interactive components demo - run in a real terminal for best experience."""

import os
import sys

import clicycle as cc

# Force interactive mode for testing
os.environ.pop("TERM", None)
if hasattr(sys.stdin, "isatty"):
    sys.stdin.isatty = lambda: True

cc.header("Interactive Components", "Arrow keys & checkboxes")

# Simple select
frameworks = ["Django", "FastAPI", "Flask", "Pyramid", "Tornado"]
selected = cc.select("Choose a Python Web Framework", frameworks)

if selected:
    cc.success(f"You selected: {selected}")
else:
    cc.warning("Selection cancelled")

# Multi-select
features = [
    "Authentication",
    "API Documentation",
    "Database Migrations",
    "Caching",
    "Rate Limiting",
]

selected_features = cc.multi_select(
    "Select Features to Include",
    features,
    default_selected=[0, 2],  # Auth and Migrations pre-selected
    min_selection=1,
    max_selection=3,
)

if selected_features:
    cc.success(f"Selected {len(selected_features)} features:")
    for feature in selected_features:
        cc.list_item(feature)
else:
    cc.warning("No features selected")
