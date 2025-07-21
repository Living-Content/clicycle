#!/usr/bin/env python3
"""Performance benchmarks for clicycle."""

import io
import os
import sys
import time

import psutil
import rich.console
from rich.table import Table

from clicycle import Clicycle


def measure_time_and_memory(func):
    """Decorator to measure execution time and memory usage."""

    def wrapper(*args, **kwargs):
        # Get initial memory
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        # Measure time
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()

        # Get final memory
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_delta = final_memory - initial_memory

        execution_time = (end_time - start_time) * 1000  # Convert to ms

        return {
            "result": result,
            "time_ms": execution_time,
            "memory_mb": memory_delta,
            "initial_memory_mb": initial_memory,
            "final_memory_mb": final_memory,
        }

    return wrapper


@measure_time_and_memory
def test_clicycle_startup():
    """Test clicycle import and instantiation time."""
    Clicycle()  # Just instantiate, don't assign to variable
    return "clicycle_startup"


@measure_time_and_memory
def test_clicycle_basic_output():
    """Test basic clicycle output."""
    cli = Clicycle()
    # Capture output instead of printing
    cli.stream.console = rich.console.Console(file=io.StringIO())

    cli.header("Performance Test", "Basic Output")
    cli.info("This is an info message")
    cli.success("This is a success message")
    cli.warning("This is a warning message")
    cli.error("This is an error message")
    return "clicycle_basic"


@measure_time_and_memory
def test_clicycle_large_table():
    """Test clicycle with a large table."""
    cli = Clicycle()
    cli.stream.console = rich.console.Console(file=io.StringIO())

    # Generate large dataset
    data = [
        {
            "ID": i,
            "Name": f"User_{i:04d}",
            "Email": f"user{i}@example.com",
            "Score": i % 100,
        }
        for i in range(1000)
    ]
    cli.table(data, title="Large Dataset")
    return "clicycle_large_table"


@measure_time_and_memory
def test_raw_rich_output():
    """Test raw Rich output for comparison."""
    console = rich.console.Console(file=io.StringIO())

    console.print("Performance Test", style="bold magenta")
    console.print("Basic Output", style="dim")
    console.print("ℹ This is an info message", style="blue")
    console.print("✔ This is a success message", style="green")
    console.print("⚠ This is a warning message", style="yellow")
    console.print("✖ This is an error message", style="red")
    return "raw_rich"


@measure_time_and_memory
def test_raw_rich_large_table():
    """Test raw Rich table for comparison."""
    console = rich.console.Console(file=io.StringIO())

    table = Table(title="Large Dataset")
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Email")
    table.add_column("Score")

    for i in range(1000):
        table.add_row(str(i), f"User_{i:04d}", f"user{i}@example.com", str(i % 100))

    console.print(table)
    return "raw_rich_large_table"


@measure_time_and_memory
def test_plain_print():
    """Test plain print statements for baseline."""

    # Redirect to null
    original_stdout = sys.stdout
    sys.stdout = io.StringIO()

    print("Performance Test")
    print("Basic Output")
    print("ℹ This is an info message")
    print("✔ This is a success message")
    print("⚠ This is a warning message")
    print("✖ This is an error message")

    sys.stdout = original_stdout
    return "plain_print"


def run_performance_tests():
    """Run all performance tests and display results."""
    tests = [
        ("Clicycle Startup", test_clicycle_startup),
        ("Clicycle Basic Output", test_clicycle_basic_output),
        ("Clicycle Large Table (1000 rows)", test_clicycle_large_table),
        ("Raw Rich Basic Output", test_raw_rich_output),
        ("Raw Rich Large Table (1000 rows)", test_raw_rich_large_table),
        ("Plain Print Baseline", test_plain_print),
    ]

    print("🚀 Running Clicycle Performance Tests...\n")

    results = []
    for name, test_func in tests:
        print(f"Running {name}...")
        try:
            result = test_func()
            results.append((name, result))
            print(f"  ✓ {result['time_ms']:.2f}ms")
        except Exception as e:
            print(f"  ✗ Error: {e}")
            results.append((name, {"time_ms": 0, "memory_mb": 0, "error": str(e)}))

    # Display results using clicycle
    cli = Clicycle()
    cli.header("Performance Test Results", "Clicycle vs Alternatives")

    # Prepare table data
    table_data = []
    for name, result in results:
        if "error" not in result:
            table_data.append(
                {
                    "Test": name,
                    "Time (ms)": f"{result['time_ms']:.2f}",
                    "Memory Δ (MB)": f"{result['memory_mb']:.2f}",
                    "Status": "✓ Pass",
                }
            )
        else:
            table_data.append(
                {
                    "Test": name,
                    "Time (ms)": "Error",
                    "Memory Δ (MB)": "Error",
                    "Status": "✗ Fail",
                }
            )

    cli.table(table_data, title="Performance Comparison")

    # Analysis
    cli.section("Analysis")

    if len([r for _, r in results if "error" not in r]) >= 3:
        clicycle_basic = next(
            r for n, r in results if "Clicycle Basic" in n and "error" not in r
        )
        rich_basic = next(
            r for n, r in results if "Raw Rich Basic" in n and "error" not in r
        )
        plain_basic = next(
            r for n, r in results if "Plain Print" in n and "error" not in r
        )

        cli.info(
            f"Clicycle overhead vs Raw Rich: {(clicycle_basic['time_ms'] / rich_basic['time_ms'] - 1) * 100:.1f}%"
        )
        cli.info(
            f"Clicycle overhead vs Plain Print: {(clicycle_basic['time_ms'] / plain_basic['time_ms'] - 1) * 100:.1f}%"
        )

        if clicycle_basic["time_ms"] < 50:
            cli.success("Clicycle basic output is very fast (< 50ms)")
        elif clicycle_basic["time_ms"] < 100:
            cli.success("Clicycle basic output is fast (< 100ms)")
        else:
            cli.warning("Clicycle basic output is slower than expected")

    # Recommendations
    cli.section("Recommendations")
    cli.suggestions(
        [
            "For simple output: clicycle overhead is minimal",
            "For large tables: consider pagination or streaming",
            "For high-frequency calls: cache clicycle instances",
            "For scripts: startup cost is negligible",
            "Memory usage is reasonable for typical CLI use",
        ]
    )


if __name__ == "__main__":
    run_performance_tests()
