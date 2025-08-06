#!/usr/bin/env python
"""Test progress bar display to check for spacing issues."""

import time
import clicycle as cc

print("=" * 60)
print("TEST 1: Basic progress bar")
print("=" * 60)

with cc.progress('Deploying to Kubernetes...') as p:
    time.sleep(0.5)
    p.update(25, 'Starting deployment')
    time.sleep(0.5)
    p.update(50, 'Containers launching')
    time.sleep(0.5)
    p.update(75, 'Services configuring')
    time.sleep(0.5)
    p.update(100, 'Deployment complete.')

print("\n" + "=" * 60)
print("TEST 2: Progress bar with variable assignment (like lco-devops)")
print("=" * 60)

progress_bar = cc.progress('Running system health check...')
with progress_bar as p:
    time.sleep(0.5)
    p.update(33, 'Checking GCP auth')
    time.sleep(0.5)
    p.update(66, 'Checking Docker')
    time.sleep(0.5)
    p.update(100, 'Complete')

print("\n" + "=" * 60)
print("TEST 3: Multiple progress bars in sequence")
print("=" * 60)

with cc.progress('First task...') as p:
    time.sleep(0.3)
    p.update(50, 'Processing')
    time.sleep(0.3)
    p.update(100, 'Done')

with cc.progress('Second task...') as p:
    time.sleep(0.3)
    p.update(50, 'Processing')
    time.sleep(0.3)
    p.update(100, 'Done')

print("\n" + "=" * 60)
print("TEST 4: Direct Rich Progress (for comparison)")
print("=" * 60)

from rich.console import Console
from rich.progress import Progress, BarColumn, TaskProgressColumn, TextColumn

console = Console()
print('→ Direct Rich Progress test...')
progress = Progress(
    BarColumn(),
    TaskProgressColumn(),
    TextColumn('[progress.description]{task.description}'),
    console=console,
)
task = progress.add_task('', total=100)
with progress:
    time.sleep(0.5)
    progress.update(task, completed=50, description='In progress')
    time.sleep(0.5)
    progress.update(task, completed=100, description='Complete')

print("\nAll tests complete!")