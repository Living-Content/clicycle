"""Tests for the main Clicycle class."""

from unittest.mock import MagicMock, patch

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
        assert cli.console.width == 120

    def test_clear(self):
        """Test clear functionality."""
        cli = Clicycle()
        cli.console = MagicMock()
        cli.stream = MagicMock()

        cli.clear()

        cli.console.clear.assert_called_once()
        cli.stream.clear_history.assert_called_once()

    def test_is_verbose_no_context(self):
        """Test verbose check when no Click context exists."""
        cli = Clicycle()

        # Should return False when no context
        assert cli.is_verbose is False

    @patch("click.get_current_context")
    def test_is_verbose_with_context(self, mock_get_context):
        """Test verbose check with Click context."""
        cli = Clicycle()

        # Mock context with verbose=True
        mock_context = MagicMock()
        mock_context.obj = {"verbose": True}
        mock_get_context.return_value = mock_context

        assert cli.is_verbose is True

        # Mock context with verbose=False
        mock_context.obj = {"verbose": False}
        assert cli.is_verbose is False

        # Mock context with no obj
        mock_context.obj = None
        assert cli.is_verbose is False

    @patch("click.get_current_context")
    def test_is_verbose_with_non_dict_obj(self, mock_get_context):
        """Test verbose check when obj is not a dict."""
        cli = Clicycle()

        mock_context = MagicMock()
        mock_context.obj = "not a dict"
        mock_get_context.return_value = mock_context

        assert cli.is_verbose is False

    @patch("click.get_current_context")
    def test_is_verbose_runtime_error(self, mock_get_context):
        """Test verbose check when get_current_context raises RuntimeError."""
        cli = Clicycle()

        mock_get_context.side_effect = RuntimeError("No context")

        assert cli.is_verbose is False
