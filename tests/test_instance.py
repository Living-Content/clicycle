"""Unit tests for clicycle.instance module."""

from unittest.mock import MagicMock, patch

from clicycle.core import Clicycle
from clicycle.instance import configure, get_default_cli
from clicycle.theme import Theme


class TestInstance:
    """Test the instance management functions."""

    def setup_method(self):
        """Reset the global instance before each test."""
        # Access the private module variable to reset it
        import clicycle.instance
        clicycle.instance._default_cli = None

    def test_get_default_cli_creates_instance(self):
        """Test that get_default_cli creates a new instance if none exists."""
        cli = get_default_cli()

        assert isinstance(cli, Clicycle)
        assert cli.width == 100
        assert isinstance(cli.theme, Theme)

    def test_get_default_cli_returns_same_instance(self):
        """Test that get_default_cli returns the same instance."""
        cli1 = get_default_cli()
        cli2 = get_default_cli()

        assert cli1 is cli2

    def test_configure_creates_new_instance(self):
        """Test that configure creates a new configured instance."""
        theme = Theme()

        configure(width=120, theme=theme, app_name="TestApp")

        cli = get_default_cli()
        assert cli.width == 120
        assert cli.theme is theme
        assert cli.app_name == "TestApp"

    def test_configure_replaces_existing_instance(self):
        """Test that configure replaces an existing instance."""
        # Get initial instance
        cli1 = get_default_cli()
        assert cli1.width == 100

        # Configure with new settings
        configure(width=80)

        # Get new instance
        cli2 = get_default_cli()
        assert cli2.width == 80
        assert cli1 is not cli2

    def test_configure_with_no_args(self):
        """Test that configure with no args creates default instance."""
        configure()

        cli = get_default_cli()
        assert cli.width == 100
        assert isinstance(cli.theme, Theme)
        assert cli.app_name is None

    def test_configure_partial_args(self):
        """Test configure with partial arguments."""
        configure(app_name="MyApp")

        cli = get_default_cli()
        assert cli.width == 100  # Default
        assert cli.app_name == "MyApp"

    @patch("clicycle.instance.Clicycle")
    def test_get_default_cli_lazy_initialization(self, mock_clicycle):
        """Test that get_default_cli uses lazy initialization."""
        mock_instance = MagicMock()
        mock_clicycle.return_value = mock_instance

        # First call should create instance
        cli1 = get_default_cli()
        assert cli1 is mock_instance
        mock_clicycle.assert_called_once()

        # Second call should not create new instance
        cli2 = get_default_cli()
        assert cli2 is mock_instance
        assert mock_clicycle.call_count == 1  # Still only called once
