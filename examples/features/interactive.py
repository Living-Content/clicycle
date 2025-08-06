#!/usr/bin/env python3
"""Interactive components demonstration."""

import time

import clicycle as cc

cc.header("Interactive Components Demo", "Arrow keys, checkboxes, and more!")

# Simple select
cc.section("Simple Select")
cc.info("Use arrow keys to navigate and Enter to select:")

frameworks = ["Django", "FastAPI", "Flask", "Pyramid", "Tornado"]
selected_framework = cc.select("Choose a Python Web Framework", frameworks)

if selected_framework:
    cc.success(f"You selected: {selected_framework}")
else:
    cc.warning("Selection cancelled")

# Select with descriptions
cc.section("Select with Descriptions")
cc.info("Options can include descriptions for more context:")

databases = [
    {
        "label": "PostgreSQL",
        "value": "postgres",
        "description": "Advanced open-source relational database",
    },
    {
        "label": "MySQL",
        "value": "mysql",
        "description": "Popular open-source relational database",
    },
    {
        "label": "MongoDB",
        "value": "mongo",
        "description": "Document-oriented NoSQL database",
    },
    {
        "label": "Redis",
        "value": "redis",
        "description": "In-memory data structure store",
    },
    {
        "label": "SQLite",
        "value": "sqlite",
        "description": "Embedded relational database",
    },
]

selected_db = cc.select("Choose a Database", databases, default_index=0)

if selected_db:
    cc.success(f"You selected: {selected_db}")

    # Show connection example
    cc.code(
        f"""# Example connection
import {selected_db}_connector

conn = {selected_db}_connector.connect(
    host='localhost',
    database='myapp'
)""",
        language="python",
    )
else:
    cc.warning("No database selected")

# Multi-select
cc.section("Multi-Select")
cc.info("Use Space to toggle selections and Enter to confirm:")

features = [
    "Authentication",
    "API Documentation",
    "Database Migrations",
    "Caching",
    "Rate Limiting",
    "WebSocket Support",
    "Background Tasks",
    "File Uploads",
]

selected_features = cc.multi_select(
    "Select Features to Include",
    features,
    default_selected=[0, 2],  # Auth and Migrations pre-selected
    min_selection=1,
    max_selection=5,
)

if selected_features:
    cc.success(f"Selected {len(selected_features)} features:")
    for feature in selected_features:
        cc.list_item(feature)
else:
    cc.warning("Feature selection cancelled")

# Practical example - Git workflow
cc.section("Practical Example: Git Workflow")

# Simulate git status
changes = [
    {"label": "src/main.py", "value": "src/main.py"},
    {"label": "src/utils.py", "value": "src/utils.py"},
    {"label": "tests/test_main.py", "value": "tests/test_main.py"},
    {"label": "README.md", "value": "README.md"},
    {"label": ".gitignore", "value": ".gitignore"},
]

cc.info("Modified files:")
for file in changes:
    cc.list_item(file["label"])

files_to_commit = cc.multi_select(
    "Select files to stage for commit", changes, min_selection=1
)

if files_to_commit:
    cc.success(f"Staged {len(files_to_commit)} files")

    commit_type = cc.select(
        "Select commit type",
        [
            {"label": "feat: A new feature", "value": "feat"},
            {"label": "fix: A bug fix", "value": "fix"},
            {"label": "docs: Documentation changes", "value": "docs"},
            {"label": "style: Code style changes", "value": "style"},
            {"label": "refactor: Code refactoring", "value": "refactor"},
            {"label": "test: Test changes", "value": "test"},
            {"label": "chore: Build/tooling changes", "value": "chore"},
        ],
    )

    if commit_type:
        cc.info(f"Creating {commit_type} commit with {len(files_to_commit)} files...")
        with cc.spinner("Committing changes..."):
            time.sleep(1)
        cc.success("Changes committed successfully!")
    else:
        cc.error("Commit cancelled")
else:
    cc.error("No files selected")

# Results
cc.section("Results")
cc.info("Interactive components provide:")
cc.list_item("Keyboard navigation with arrow keys")
cc.list_item("Visual feedback for current selection")
cc.list_item("Multi-select with checkboxes")
cc.list_item("Descriptions and metadata support")
cc.list_item("Min/max selection constraints")
cc.list_item("Clean, intuitive interface")

cc.success("Interactive demo complete!")
