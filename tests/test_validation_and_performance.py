"""Tests for v3.1.0 improvements."""

from unittest.mock import MagicMock

import pytest
from rich.console import Console

from clicycle import Clicycle, Theme
from clicycle.components.text import Info, Text
from clicycle.rendering.stream import RenderStream


class TestInputValidation:
    """Test input validation for components."""

    def test_text_invalid_type(self):
        """Test that Text component rejects non-string messages."""
        theme = Theme()
        with pytest.raises(TypeError, match="Message must be a string"):
            Text(theme, 123)

    def test_text_empty_message(self):
        """Test that Text component rejects empty messages."""
        theme = Theme()
        with pytest.raises(ValueError, match="Message cannot be empty"):
            Text(theme, "")

    def test_info_invalid_type(self):
        """Test that Info component validates input."""
        theme = Theme()
        with pytest.raises(TypeError):
            Info(theme, None)


class TestThemeValidation:
    """Test theme validation."""

    def test_width_too_small(self):
        """Test that theme rejects width < 20."""
        with pytest.raises(ValueError, match="Width must be an integer >= 20"):
            Theme(width=10)

    def test_width_invalid_type(self):
        """Test that theme rejects non-integer width."""
        with pytest.raises(ValueError, match="Width must be an integer >= 20"):
            Theme(width="100")

    def test_invalid_spinner_type(self):
        """Test that theme rejects invalid spinner types."""
        with pytest.raises(ValueError, match="Invalid spinner type"):
            Theme(spinner_type="invalid")

    def test_valid_spinner_types(self):
        """Test that theme accepts valid spinner types."""
        for spinner in [
            "dots",
            "dots2",
            "dots3",
            "line",
            "star",
            "bouncingBar",
            "arc",
            "arrow",
        ]:
            theme = Theme(spinner_type=spinner)
            assert theme.spinner_type == spinner


class TestConsoleCaching:
    """Test console caching optimization."""

    def test_console_reused_same_width(self):
        """Test that console is reused for same width."""
        # Clear cache first
        Clicycle._console_cache.clear()

        cli1 = Clicycle(width=80)
        cli2 = Clicycle(width=80)

        assert cli1.console is cli2.console

    def test_console_different_width(self):
        """Test that different widths get different consoles."""
        cli1 = Clicycle(width=80)
        cli2 = Clicycle(width=100)

        assert cli1.console is not cli2.console

    def test_cache_persists(self):
        """Test that cache persists across instances."""
        Clicycle._console_cache.clear()
        cli1 = Clicycle(width=90)
        console1 = cli1.console

        # Create and destroy instance
        cli2 = Clicycle(width=90)
        del cli2

        # New instance should still get cached console
        cli3 = Clicycle(width=90)
        assert cli3.console is console1


class TestHistoryLimit:
    """Test render stream history limiting."""

    def test_default_history_limit(self):
        """Test that history is limited to default 100."""
        console = MagicMock(spec=Console)
        stream = RenderStream(console)

        theme = Theme()
        for i in range(150):
            component = Info(theme, f"Message {i}")
            component.render = MagicMock()  # Mock render to avoid output
            stream.render(component)

        assert len(stream.history) == 100
        # Should have kept the most recent
        assert stream.history[-1].message == "Message 149"
        assert stream.history[0].message == "Message 50"

    def test_custom_history_limit(self):
        """Test custom history limit."""
        console = MagicMock(spec=Console)
        stream = RenderStream(console, max_history=50)

        theme = Theme()
        for i in range(100):
            component = Info(theme, f"Message {i}")
            component.render = MagicMock()
            stream.render(component)

        assert len(stream.history) == 50
        assert stream.history[-1].message == "Message 99"
        assert stream.history[0].message == "Message 50"

    def test_history_limit_with_deferred(self):
        """Test history limit with deferred components."""
        console = MagicMock(spec=Console)
        stream = RenderStream(console, max_history=10)

        theme = Theme()

        # Create a mock deferred component
        class DeferredComponent:
            component_type = "test"
            deferred_render = True

            def set_context(self, prev):
                pass

            def render_with_spacing(self, console):
                pass

        # Add regular and deferred components
        for i in range(20):
            if i % 2 == 0:
                component = Info(theme, f"Message {i}")
                component.render = MagicMock()
                stream.render(component)
            else:
                deferred = DeferredComponent()
                stream.render(deferred)

        assert len(stream.history) <= 10
