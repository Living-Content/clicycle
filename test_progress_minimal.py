#!/usr/bin/env python
"""Minimal test to show the blank line issue."""

import time
import clicycle as cc

print("Before progress bar")
print("Line right before:")
with cc.progress('Deploying to Kubernetes...') as p:
    time.sleep(1)
    p.update(100, 'Deployment complete.')
print("Line right after")
print("After progress bar")