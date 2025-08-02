"""Tests for clicycle.__init__ module functions."""

from unittest.mock import MagicMock, patch

import clicycle


class TestInitFunctions:
    """Test all the convenience functions in __init__.py."""

    @patch("clicycle.get_default_cli")
    def test_header(self, mock_get_cli):
        """Test header function."""
        mock_cli = MagicMock()
        mock_get_cli.return_value = mock_cli

        clicycle.header("Title", "Subtitle", "App")
        mock_cli.header.assert_called_once_with("Title", "Subtitle", "App")

    @patch("clicycle.get_default_cli")
    def test_section(self, mock_get_cli):
        """Test section function."""
        mock_cli = MagicMock()
        mock_get_cli.return_value = mock_cli

        clicycle.section("Section Title")
        mock_cli.section.assert_called_once_with("Section Title")

    @patch("clicycle.get_default_cli")
    def test_info(self, mock_get_cli):
        """Test info function."""
        mock_cli = MagicMock()
        mock_get_cli.return_value = mock_cli

        clicycle.info("Info message")
        mock_cli.info.assert_called_once_with("Info message")

    @patch("clicycle.get_default_cli")
    def test_success(self, mock_get_cli):
        """Test success function."""
        mock_cli = MagicMock()
        mock_get_cli.return_value = mock_cli

        clicycle.success("Success message")
        mock_cli.success.assert_called_once_with("Success message")

    @patch("clicycle.get_default_cli")
    def test_error(self, mock_get_cli):
        """Test error function."""
        mock_cli = MagicMock()
        mock_get_cli.return_value = mock_cli

        clicycle.error("Error message")
        mock_cli.error.assert_called_once_with("Error message")

    @patch("clicycle.get_default_cli")
    def test_warning(self, mock_get_cli):
        """Test warning function."""
        mock_cli = MagicMock()
        mock_get_cli.return_value = mock_cli

        clicycle.warning("Warning message")
        mock_cli.warning.assert_called_once_with("Warning message")

    @patch("clicycle.get_default_cli")
    def test_debug(self, mock_get_cli):
        """Test debug function."""
        mock_cli = MagicMock()
        mock_get_cli.return_value = mock_cli

        clicycle.debug("Debug message")
        mock_cli.debug.assert_called_once_with("Debug message")

    @patch("clicycle.get_default_cli")
    def test_prompt(self, mock_get_cli):
        """Test prompt function."""
        mock_cli = MagicMock()
        mock_cli.prompt.return_value = "user input"
        mock_get_cli.return_value = mock_cli

        result = clicycle.prompt("Enter text:", default="test")
        assert result == "user input"
        mock_cli.prompt.assert_called_once_with("Enter text:", default="test")

    @patch("clicycle.get_default_cli")
    def test_confirm(self, mock_get_cli):
        """Test confirm function."""
        mock_cli = MagicMock()
        mock_cli.confirm.return_value = True
        mock_get_cli.return_value = mock_cli

        result = clicycle.confirm("Are you sure?", abort=True)
        assert result is True
        mock_cli.confirm.assert_called_once_with("Are you sure?", abort=True)

    @patch("clicycle.get_default_cli")
    def test_summary(self, mock_get_cli):
        """Test summary function."""
        mock_cli = MagicMock()
        mock_get_cli.return_value = mock_cli

        data = [{"label": "Name", "value": "Test"}]
        clicycle.summary(data)
        mock_cli.summary.assert_called_once_with(data)

    @patch("clicycle.get_default_cli")
    def test_list_item(self, mock_get_cli):
        """Test list_item function."""
        mock_cli = MagicMock()
        mock_get_cli.return_value = mock_cli

        clicycle.list_item("Item 1")
        mock_cli.list_item.assert_called_once_with("Item 1")

    @patch("clicycle.get_default_cli")
    def test_spinner(self, mock_get_cli):
        """Test spinner context manager."""
        mock_cli = MagicMock()
        mock_spinner = MagicMock()
        mock_cli.spinner.return_value.__enter__.return_value = mock_spinner
        mock_get_cli.return_value = mock_cli

        with clicycle.spinner("Loading...") as s:
            assert s == mock_spinner
        mock_cli.spinner.assert_called_once_with("Loading...")

    @patch("clicycle.get_default_cli")
    def test_table(self, mock_get_cli):
        """Test table function."""
        mock_cli = MagicMock()
        mock_get_cli.return_value = mock_cli

        data = [{"col1": "val1", "col2": "val2"}]
        clicycle.table(data, title="Test Table")
        mock_cli.table.assert_called_once_with(data, "Test Table")

    @patch("clicycle.get_default_cli")
    def test_code(self, mock_get_cli):
        """Test code function."""
        mock_cli = MagicMock()
        mock_get_cli.return_value = mock_cli

        clicycle.code("print('hello')", "python", "Example", True)
        mock_cli.code.assert_called_once_with("print('hello')", "python", "Example", True)

    @patch("clicycle.get_default_cli")
    def test_json(self, mock_get_cli):
        """Test json function."""
        mock_cli = MagicMock()
        mock_get_cli.return_value = mock_cli

        data = {"key": "value"}
        clicycle.json(data, "JSON Data")
        mock_cli.json.assert_called_once_with(data, "JSON Data")

    @patch("clicycle.get_default_cli")
    def test_progress(self, mock_get_cli):
        """Test progress context manager."""
        mock_cli = MagicMock()
        mock_progress = MagicMock()
        mock_cli.progress.return_value.__enter__.return_value = mock_progress
        mock_get_cli.return_value = mock_cli

        with clicycle.progress("Processing") as p:
            assert p == mock_progress
        mock_cli.progress.assert_called_once_with("Processing")

    @patch("clicycle.get_default_cli")
    def test_multi_progress(self, mock_get_cli):
        """Test multi_progress context manager."""
        mock_cli = MagicMock()
        mock_progress = MagicMock()
        mock_cli.multi_progress.return_value.__enter__.return_value = mock_progress
        mock_get_cli.return_value = mock_cli

        with clicycle.multi_progress("Processing") as p:
            assert p == mock_progress
        mock_cli.multi_progress.assert_called_once_with("Processing")

    @patch("clicycle.get_default_cli")
    def test_update_progress(self, mock_get_cli):
        """Test update_progress function."""
        mock_cli = MagicMock()
        mock_get_cli.return_value = mock_cli

        clicycle.update_progress(50.0, "Halfway")
        mock_cli.update_progress.assert_called_once_with(50.0, "Halfway")

    @patch("clicycle.get_default_cli")
    def test_suggestions(self, mock_get_cli):
        """Test suggestions function."""
        mock_cli = MagicMock()
        mock_get_cli.return_value = mock_cli

        items = ["Option 1", "Option 2"]
        clicycle.suggestions(items)
        mock_cli.suggestions.assert_called_once_with(items)

    @patch("clicycle.get_default_cli")
    def test_block(self, mock_get_cli):
        """Test block context manager."""
        mock_cli = MagicMock()
        mock_block = MagicMock()
        mock_cli.block.return_value.__enter__.return_value = mock_block
        mock_get_cli.return_value = mock_cli

        with clicycle.block() as b:
            assert b == mock_block
        mock_cli.block.assert_called_once()

    @patch("clicycle.get_default_cli")
    def test_clear(self, mock_get_cli):
        """Test clear function."""
        mock_cli = MagicMock()
        mock_get_cli.return_value = mock_cli

        clicycle.clear()
        mock_cli.clear.assert_called_once()

    def test_exports(self):
        """Test that all expected exports are available."""
        expected = [
            "Clicycle",
            "Theme",
            "Icons",
            "Typography",
            "Layout",
            "ComponentSpacing",
            "select_from_list",
            "configure",
            "header",
            "section",
            "info",
            "success",
            "error",
            "warning",
            "debug",
            "prompt",
            "confirm",
            "summary",
            "list_item",
            "spinner",
            "table",
            "code",
            "json",
            "progress",
            "multi_progress",
            "update_progress",
            "suggestions",
            "block",
            "clear",
        ]
        for export in expected:
            assert hasattr(clicycle, export)
