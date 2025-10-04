"""Tests for the main Clicycle class."""

from unittest.mock import MagicMock

from rich.console import Console

from clicycle import Clicycle, Theme
from clicycle.rendering.stream import RenderStream


class TestClicycle:
    """Test the main Clicycle class."""

    def test_init_default(self):
        """Test Clicycle initialization with defaults."""
        cli = Clicycle()

        assert cli.width == 100
        assert isinstance(cli.theme, Theme)
        assert cli.app_name is None
        assert isinstance(cli.console, Console)
        assert isinstance(cli.stream, RenderStream)

    def test_init_custom_params(self):
        """Test Clicycle initialization with custom parameters."""
        custom_theme = Theme()
        cli = Clicycle(width=120, theme=custom_theme, app_name="TestApp")

        assert cli.width == 120
        assert cli.theme is custom_theme
        assert cli.app_name == "TestApp"
        # Note: cli.console.width is determined by terminal size, not the width parameter
        # The width parameter controls rendering behavior, not console dimensions

    def test_clear(self):
        """Test clear functionality."""
        cli = Clicycle()
        cli.console = MagicMock()
        cli.stream = MagicMock()

        cli.clear()

        cli.console.clear.assert_called_once()
        cli.stream.clear_history.assert_called_once()
