#!/usr/bin/env python3
"""Complete showcase (VERBOSE) - Shows all components with debug messages."""

import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    # Run the full_app.py with --verbose flag
    full_app_path = Path(__file__).parent / "full_app.py"
    subprocess.run([sys.executable, str(full_app_path), "--verbose"])
