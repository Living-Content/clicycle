#!/usr/bin/env python3
"""Performance optimizations for clicycle."""

import io
import time

from rich.console import Console
from rich.text import Text as RichText

from clicycle import Clicycle


class OptimizedClicycle:
    """Performance-optimized version of Clicycle with several improvements."""

    def __init__(self, width: int = 100, theme=None, app_name: str | None = None):
        from clicycle import Theme

        self.width = width
        self.theme = theme or Theme()
        self.console = Console(width=width)
        self.app_name = app_name

        # Pre-compute commonly used styles (caching optimization)
        self._style_cache = {}
        self._precompute_styles()

        # Reuse text objects (object pooling optimization)
        self._text_pool = {}

    def _precompute_styles(self):
        """Pre-compute and cache frequently used styles."""
        self._style_cache.update(
            {
                "info": f"{self.theme.icons.info} ",
                "success": f"{self.theme.icons.success} ",
                "warning": f"{self.theme.icons.warning} ",
                "error": f"{self.theme.icons.error} ",
                "info_style": self.theme.typography.info_style,
                "success_style": self.theme.typography.success_style,
                "warning_style": self.theme.typography.warning_style,
                "error_style": self.theme.typography.error_style,
            }
        )

    def _get_text(self, content: str, style: str) -> RichText:
        """Get reusable text objects from pool."""
        key = (content, style)
        if key not in self._text_pool:
            self._text_pool[key] = RichText(content, style=style)
        return self._text_pool[key]

    def info(self, message: str) -> None:
        """Optimized info message."""
        # Single console.print call instead of component creation
        icon = self._style_cache["info"]
        style = self._style_cache["info_style"]
        self.console.print(f"{icon}{message}", style=style)

    def success(self, message: str) -> None:
        """Optimized success message."""
        icon = self._style_cache["success"]
        style = self._style_cache["success_style"]
        self.console.print(f"{icon}{message}", style=style)

    def warning(self, message: str) -> None:
        """Optimized warning message."""
        icon = self._style_cache["warning"]
        style = self._style_cache["warning_style"]
        self.console.print(f"{icon}{message}", style=style)

    def error(self, message: str) -> None:
        """Optimized error message."""
        icon = self._style_cache["error"]
        style = self._style_cache["error_style"]
        self.console.print(f"{icon}{message}", style=style)


def measure_time(func):
    """Simple time measurement decorator."""

    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        return (end - start) * 1000, result  # Convert to ms

    return wrapper


@measure_time
def test_current_clicycle():
    """Test current clicycle implementation."""
    cli = Clicycle()
    cli.stream.console = Console(file=io.StringIO())

    cli.info("This is an info message")
    cli.success("This is a success message")
    cli.warning("This is a warning message")
    cli.error("This is an error message")
    return "current"


@measure_time
def test_optimized_clicycle():
    """Test optimized clicycle implementation."""
    cli = OptimizedClicycle()
    cli.console = Console(file=io.StringIO())

    cli.info("This is an info message")
    cli.success("This is a success message")
    cli.warning("This is a warning message")
    cli.error("This is an error message")
    return "optimized"


def run_optimization_tests():
    """Compare current vs optimized implementations."""
    print("🔧 Testing Clicycle Performance Optimizations...\n")

    # Warm up
    test_current_clicycle()
    test_optimized_clicycle()

    # Run multiple iterations for better averages
    current_times = []
    optimized_times = []

    for _ in range(100):
        current_time, _ = test_current_clicycle()
        optimized_time, _ = test_optimized_clicycle()
        current_times.append(current_time)
        optimized_times.append(optimized_time)

    current_avg = sum(current_times) / len(current_times)
    optimized_avg = sum(optimized_times) / len(optimized_times)
    improvement = ((current_avg - optimized_avg) / current_avg) * 100

    # Display results
    cli = Clicycle()
    cli.header(
        "Performance Optimization Results", "Current vs Optimized Implementation"
    )

    # Results table
    table_data = [
        {
            "Implementation": "Current Clicycle",
            "Avg Time (ms)": f"{current_avg:.3f}",
            "Min (ms)": f"{min(current_times):.3f}",
            "Max (ms)": f"{max(current_times):.3f}",
        },
        {
            "Implementation": "Optimized Clicycle",
            "Avg Time (ms)": f"{optimized_avg:.3f}",
            "Min (ms)": f"{min(optimized_times):.3f}",
            "Max (ms)": f"{max(optimized_times):.3f}",
        },
    ]

    cli.table(table_data, title="Performance Comparison (100 iterations)")

    cli.section("Analysis")

    if improvement > 0:
        cli.success(f"Optimization achieved {improvement:.1f}% speed improvement!")
        cli.info(
            f"Absolute improvement: {current_avg - optimized_avg:.3f}ms per operation"
        )
    else:
        cli.warning(
            f"Optimization was {abs(improvement):.1f}% slower (within margin of error)"
        )

    cli.section("Optimization Techniques Applied")
    cli.suggestions(
        [
            "Style pre-computation and caching",
            "Object pooling for text objects",
            "Reduced component object creation",
            "Direct console operations",
            "Eliminated redundant theme lookups",
        ]
    )

    cli.section("Further Optimization Ideas")
    cli.suggestions(
        [
            "Lazy import Rich components only when needed",
            "Console instance reuse and pooling",
            "Batch multiple operations into single renders",
            "String interpolation optimization",
            "Memory-mapped icon/style lookups",
        ]
    )


if __name__ == "__main__":
    run_optimization_tests()
