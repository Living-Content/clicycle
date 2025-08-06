#!/usr/bin/env python
"""Test to reproduce the blank line appearing after progress starts."""

import time
import clicycle as cc

print("=" * 60)
print("TEST: Blank line appears after first update?")
print("=" * 60)
print("Watch closely - does a blank line appear after update?")
print("---")

with cc.progress('Deploying to Kubernetes...') as p:
    # Initial state - no update yet
    print("(Progress bar should be visible above, no update yet)")
    time.sleep(2)  # Wait so you can see initial state
    
    # First update - this is where the blank line might appear
    print("(Now updating to 10%...)")
    p.update(10, 'Starting...')
    time.sleep(2)
    
    # More updates
    p.update(50, 'Half way...')
    time.sleep(1)
    p.update(100, 'Complete')

print("---")
print("Test complete")

print("\n" + "=" * 60)
print("TEST 2: What if we don't print during progress?")
print("=" * 60)

with cc.progress('Running health check...') as p:
    # Just updates, no prints
    time.sleep(1)
    p.update(10, 'Starting...')
    time.sleep(1)
    p.update(50, 'Half way...')
    time.sleep(1)
    p.update(100, 'Complete')

print("Test 2 complete")