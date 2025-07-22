"""Tests for the main Clicycle class."""

from unittest.mock import patch

from clicycle import Clicycle, Theme


class TestClicycle:
    """Test the main Clicycle class."""

    def test_init_default(self):
        """Test Clicycle initialization with defaults."""
        cli = Clicycle()

        assert cli.width == 100
        assert cli.theme is not None
        assert cli.app_name is None
        assert cli.console is not None
        assert cli.stream is not None

    def test_init_custom_params(self):
        """Test Clicycle initialization with custom parameters."""
        custom_theme = Theme()
        cli = Clicycle(width=120, theme=custom_theme, app_name="TestApp")

        assert cli.width == 120
        assert cli.theme is custom_theme
        assert cli.app_name == "TestApp"

    def test_header_without_app_name(self):
        """Test header rendering without app name."""
        cli = Clicycle()

        # This should not raise an exception
        cli.header("Test Title", "Test Subtitle")

    def test_header_with_app_name(self):
        """Test header rendering with app name."""
        cli = Clicycle(app_name="TestApp")

        # This should not raise an exception
        cli.header("Test Title", "Test Subtitle")

    def test_message_methods(self):
        """Test all message type methods."""
        cli = Clicycle()

        # These should not raise exceptions
        cli.info("Info message")
        cli.success("Success message")
        cli.warning("Warning message")
        cli.error("Error message")
        cli.debug("Debug message")  # Only shows in verbose mode

    def test_list_items(self):
        """Test list item rendering."""
        cli = Clicycle()

        # This should not raise an exception
        cli.list_item("First item")
        cli.list_item("Second item")

    def test_section(self):
        """Test section rendering."""
        cli = Clicycle()

        # This should not raise an exception
        cli.section("Test Section")

    def test_table_empty_data(self):
        """Test table with empty data."""
        cli = Clicycle()

        # Should handle empty data gracefully
        cli.table([])

    def test_table_with_data(self):
        """Test table with actual data."""
        cli = Clicycle()
        data = [
            {"Name": "Alice", "Age": 30},
            {"Name": "Bob", "Age": 25},
        ]

        # This should not raise an exception
        cli.table(data, title="Test Table")

    def test_summary(self):
        """Test summary rendering."""
        cli = Clicycle()
        data = [
            {"label": "Total", "value": 100},
            {"label": "Active", "value": 85},
        ]

        # This should not raise an exception
        cli.summary(data)

    def test_code_display(self):
        """Test code display."""
        cli = Clicycle()
        code = "def hello():\n    print('Hello, World!')"

        # This should not raise an exception
        cli.code(code, language="python", title="Test Code")

    def test_json_display(self):
        """Test JSON display."""
        cli = Clicycle()
        data = {"name": "test", "value": 42}

        # This should not raise an exception
        cli.json(data, title="Test JSON")

    def test_suggestions(self):
        """Test suggestions rendering."""
        cli = Clicycle()
        suggestions = ["First suggestion", "Second suggestion"]

        # This should not raise an exception
        cli.suggestions(suggestions)

    def test_clear(self):
        """Test clear functionality."""
        cli = Clicycle()

        # This should not raise an exception
        cli.clear()

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
        mock_context = type("MockContext", (), {"obj": {"verbose": True}})()
        mock_get_context.return_value = mock_context

        assert cli.is_verbose is True

        # Mock context with verbose=False
        mock_context.obj = {"verbose": False}
        assert cli.is_verbose is False

        # Mock context with no obj
        mock_context.obj = None
        assert cli.is_verbose is False

    def test_block_context_manager(self):
        """Test block context manager."""
        cli = Clicycle()

        # This should not raise an exception
        with cli.block():
            cli.info("Inside block")
            cli.success("Still inside block")
