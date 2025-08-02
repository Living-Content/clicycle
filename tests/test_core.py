"""Unit tests for clicycle.core module."""

from unittest.mock import MagicMock, patch

from rich.console import Console
from rich.progress import Progress

from clicycle.core import Clicycle
from clicycle.render import Header, Section
from clicycle.theme import ComponentIndentation, Theme


class TestClicycleCore:
    """Test the core Clicycle class."""

    def test_init_defaults(self):
        """Test initialization with default values."""
        cli = Clicycle()
        assert cli.width == 100
        assert isinstance(cli.theme, Theme)
        assert cli.app_name is None
        assert isinstance(cli.console, Console)
        assert cli._progress is None
        assert cli._task_id is None

    def test_init_custom(self):
        """Test initialization with custom values."""
        theme = Theme()
        cli = Clicycle(width=120, theme=theme, app_name="TestApp")
        assert cli.width == 120
        assert cli.theme is theme
        assert cli.app_name == "TestApp"

    @patch("clicycle.core.RenderStream")
    def test_header(self, mock_stream_class):
        """Test header method."""
        mock_stream = MagicMock()
        mock_stream_class.return_value = mock_stream

        cli = Clicycle()
        cli.stream = mock_stream

        cli.header("Title", "Subtitle", "App")
        mock_stream.render.assert_called_once()
        args = mock_stream.render.call_args[0]
        assert isinstance(args[0], Header)
        assert args[0].title == "Title"
        assert args[0].subtitle == "Subtitle"
        assert args[0].app_name == "App"

    @patch("clicycle.core.RenderStream")
    def test_header_uses_instance_app_name(self, mock_stream_class):
        """Test header uses instance app_name when not provided."""
        mock_stream = MagicMock()
        mock_stream_class.return_value = mock_stream

        cli = Clicycle(app_name="DefaultApp")
        cli.stream = mock_stream

        cli.header("Title")
        args = mock_stream.render.call_args[0]
        assert args[0].app_name == "DefaultApp"

    @patch("clicycle.core.RenderStream")
    def test_section(self, mock_stream_class):
        """Test section method."""
        mock_stream = MagicMock()
        mock_stream_class.return_value = mock_stream

        cli = Clicycle()
        cli.stream = mock_stream

        cli.section("Section Title")
        mock_stream.render.assert_called_once()
        args = mock_stream.render.call_args[0]
        assert isinstance(args[0], Section)
        assert args[0].title == "Section Title"

    def test_info_fast_path(self):
        """Test info method using fast path."""
        cli = Clicycle()
        cli.console = MagicMock()
        cli.stream = MagicMock()
        cli.stream.last_component = None

        cli.info("Test message")

        # Check console.print was called with the message
        calls = cli.console.print.call_args_list
        assert len(calls) >= 1
        assert "Test message" in str(calls[-1])

    def test_info_with_spacing(self):
        """Test info method with spacing."""
        cli = Clicycle()
        cli.console = MagicMock()
        cli.stream = MagicMock()
        # Create a mock component that returns spacing > 0
        mock_component = MagicMock()
        cli.stream.last_component = mock_component
        cli.stream.history = MagicMock()

        # First call info to set up a component
        cli.info("First")

        # Now the second call should add spacing
        cli.info("Second")

        # Check that newlines were printed for spacing
        calls = cli.console.print.call_args_list
        # Should have spacing call and message call
        assert len(calls) >= 2

    def test_success_fast_path(self):
        """Test success method using fast path."""
        cli = Clicycle()
        cli.console = MagicMock()
        cli.stream = MagicMock()
        cli.stream.last_component = None

        cli.success("Success!")

        calls = cli.console.print.call_args_list
        assert len(calls) >= 1
        assert "Success!" in str(calls[-1])

    def test_error_fast_path(self):
        """Test error method using fast path."""
        cli = Clicycle()
        cli.console = MagicMock()
        cli.stream = MagicMock()
        cli.stream.last_component = None

        cli.error("Error!")

        calls = cli.console.print.call_args_list
        assert len(calls) >= 1
        assert "Error!" in str(calls[-1])

    def test_warning_fast_path(self):
        """Test warning method using fast path."""
        cli = Clicycle()
        cli.console = MagicMock()
        cli.stream = MagicMock()
        cli.stream.last_component = None

        cli.warning("Warning!")

        calls = cli.console.print.call_args_list
        assert len(calls) >= 1
        assert "Warning!" in str(calls[-1])

    def test_list_item_fast_path(self):
        """Test list_item method using fast path."""
        cli = Clicycle()
        cli.console = MagicMock()
        cli.stream = MagicMock()
        cli.stream.last_component = None

        cli.list_item("Item 1")

        calls = cli.console.print.call_args_list
        assert len(calls) >= 1
        assert "Item 1" in str(calls[-1])

    def test_list_item_with_spacing(self):
        """Test list_item method with spacing."""
        cli = Clicycle()
        cli.console = MagicMock()
        cli.stream = MagicMock()
        cli.stream.history = MagicMock()

        # First set up a previous component
        cli.info("Setup")

        # Now call list_item which should add spacing
        cli.list_item("Item with spacing")

        # Check calls
        calls = cli.console.print.call_args_list
        assert len(calls) >= 2

    @patch("click.get_current_context")
    def test_debug_verbose_mode(self, mock_get_context):
        """Test debug method in verbose mode."""
        mock_ctx = MagicMock()
        mock_ctx.obj = {"verbose": True}
        mock_get_context.return_value = mock_ctx

        cli = Clicycle()
        cli.console = MagicMock()
        cli.stream = MagicMock()
        cli.stream.last_component = None

        cli.debug("Debug info")

        calls = cli.console.print.call_args_list
        assert len(calls) >= 1
        assert "Debug info" in str(calls[-1])

    @patch("click.get_current_context")
    def test_debug_verbose_with_spacing(self, mock_get_context):
        """Test debug method with spacing in verbose mode."""
        mock_ctx = MagicMock()
        mock_ctx.obj = {"verbose": True}
        mock_get_context.return_value = mock_ctx

        cli = Clicycle()
        cli.console = MagicMock()
        cli.stream = MagicMock()
        cli.stream.history = MagicMock()

        # Set up previous component
        cli.info("Setup")

        # Now debug should add spacing
        cli.debug("Debug with spacing")

        calls = cli.console.print.call_args_list
        assert len(calls) >= 2

    @patch("click.get_current_context")
    def test_debug_non_verbose_mode(self, mock_get_context):
        """Test debug method when not in verbose mode."""
        mock_ctx = MagicMock()
        mock_ctx.obj = {"verbose": False}
        mock_get_context.return_value = mock_ctx

        cli = Clicycle()
        cli.console = MagicMock()
        cli.stream = MagicMock()

        cli.debug("Debug info")

        # Should not print anything
        cli.console.print.assert_not_called()

    @patch("click.prompt")
    @patch("clicycle.core.RenderStream")
    def test_prompt(self, mock_stream_class, mock_click_prompt):
        """Test prompt method."""
        mock_stream = MagicMock()
        mock_stream_class.return_value = mock_stream
        mock_click_prompt.return_value = "user input"

        cli = Clicycle()
        cli.stream = mock_stream

        result = cli.prompt("Enter value:", default="test")

        assert result == "user input"
        mock_click_prompt.assert_called_once_with("Enter value:", default="test")
        mock_stream.render.assert_called_once()

    @patch("click.confirm")
    @patch("clicycle.core.RenderStream")
    def test_confirm(self, mock_stream_class, mock_click_confirm):
        """Test confirm method."""
        mock_stream = MagicMock()
        mock_stream_class.return_value = mock_stream
        mock_click_confirm.return_value = True

        cli = Clicycle()
        cli.stream = mock_stream

        result = cli.confirm("Are you sure?", abort=True)

        assert result is True
        mock_click_confirm.assert_called_once_with("Are you sure?", abort=True)
        mock_stream.render.assert_called_once()

    def test_block_context_manager(self):
        """Test block context manager."""
        cli = Clicycle()
        original_stream = cli.stream
        original_console = cli.console

        with cli.block() as block_cli:
            assert block_cli is cli
            # Inside the block, stream and console should be temporary
            assert cli.stream != original_stream
            assert cli.console != original_console

        # After block, stream and console should be restored
        assert cli.stream is original_stream
        assert cli.console is original_console

    def test_clear(self):
        """Test clear method."""
        cli = Clicycle()
        cli.console = MagicMock()
        cli.stream = MagicMock()

        cli.clear()

        cli.console.clear.assert_called_once()
        cli.stream.clear_history.assert_called_once()

    def test_suggestions(self):
        """Test suggestions method."""
        cli = Clicycle()
        cli.section = MagicMock()
        cli.list_item = MagicMock()

        cli.suggestions(["Option 1", "Option 2"])

        cli.section.assert_called_once_with("Suggestions")
        assert cli.list_item.call_count == 2

    @patch("clicycle.core.RenderStream")
    def test_summary(self, mock_stream_class):
        """Test summary method."""
        mock_stream = MagicMock()
        mock_stream_class.return_value = mock_stream

        cli = Clicycle()
        cli.stream = mock_stream

        data = [{"label": "Name", "value": "Test"}]
        cli.summary(data)

        mock_stream.render.assert_called_once()

    @patch("click.get_current_context")
    def test_spinner_verbose_mode(self, mock_get_context):
        """Test spinner in verbose mode."""
        mock_ctx = MagicMock()
        mock_ctx.obj = {"verbose": True}
        mock_get_context.return_value = mock_ctx

        cli = Clicycle()
        cli.info = MagicMock()

        with cli.spinner("Loading..."):
            pass

        cli.info.assert_called_once_with("Loading...")

    def test_spinner_normal_mode(self):
        """Test spinner in normal mode."""
        cli = Clicycle()
        cli.console = MagicMock()
        cli.stream = MagicMock()
        cli._progress = None

        mock_status = MagicMock()
        cli.console.status.return_value = mock_status

        with cli.spinner("Loading..."):
            pass

        cli.console.status.assert_called_once()
        mock_status.__enter__.assert_called_once()
        mock_status.__exit__.assert_called_once()

    def test_spinner_inside_progress(self):
        """Test spinner when inside progress context."""
        cli = Clicycle()
        cli._progress = MagicMock()  # Simulate being inside progress
        cli.console = MagicMock()

        with cli.spinner("Loading..."):
            pass

        # Should not create status when inside progress
        cli.console.status.assert_not_called()

    def test_progress_context_manager(self):
        """Test progress context manager."""
        cli = Clicycle()
        cli.console = MagicMock()
        cli.stream = MagicMock()

        with cli.progress("Processing") as p:
            assert p is cli
            assert cli._progress is not None
            assert cli._task_id is not None

        assert cli._progress is None
        assert cli._task_id is None

    def test_progress_nested(self):
        """Test nested progress contexts are squelched."""
        cli = Clicycle()
        cli.console = MagicMock()
        cli.stream = MagicMock()

        with cli.progress("Outer"):
            outer_progress = cli._progress
            with cli.progress("Inner") as inner:
                # Inner progress should be squelched
                assert cli._progress is outer_progress
                assert inner is cli

    def test_multi_progress_context_manager(self):
        """Test multi_progress context manager."""
        cli = Clicycle()
        cli.console = MagicMock()
        cli.stream = MagicMock()

        with cli.multi_progress("Processing") as p:
            assert isinstance(p, Progress)

    @patch("clicycle.core.RenderStream")
    def test_table(self, mock_stream_class):
        """Test table method."""
        mock_stream = MagicMock()
        mock_stream_class.return_value = mock_stream

        cli = Clicycle()
        cli.stream = mock_stream

        data = [{"col1": "val1"}]
        cli.table(data, "Title")

        mock_stream.render.assert_called_once()

    @patch("clicycle.core.RenderStream")
    def test_code(self, mock_stream_class):
        """Test code method."""
        mock_stream = MagicMock()
        mock_stream_class.return_value = mock_stream

        cli = Clicycle()
        cli.stream = mock_stream

        cli.code("print('hello')", "python", "Title", True)

        mock_stream.render.assert_called_once()

    @patch("clicycle.core.RenderStream")
    def test_json(self, mock_stream_class):
        """Test json method."""
        mock_stream = MagicMock()
        mock_stream_class.return_value = mock_stream

        cli = Clicycle()
        cli.stream = mock_stream

        cli.json({"key": "value"}, "Title")

        mock_stream.render.assert_called_once()

    @patch("click.get_current_context")
    def test_is_verbose_true(self, mock_get_context):
        """Test is_verbose property when verbose is True."""
        mock_ctx = MagicMock()
        mock_ctx.obj = {"verbose": True}
        mock_get_context.return_value = mock_ctx

        cli = Clicycle()
        assert cli.is_verbose is True

    @patch("click.get_current_context")
    def test_is_verbose_false(self, mock_get_context):
        """Test is_verbose property when verbose is False."""
        mock_ctx = MagicMock()
        mock_ctx.obj = {"verbose": False}
        mock_get_context.return_value = mock_ctx

        cli = Clicycle()
        assert cli.is_verbose is False

    @patch("click.get_current_context")
    def test_is_verbose_no_context(self, mock_get_context):
        """Test is_verbose property when no context exists."""
        mock_get_context.side_effect = RuntimeError

        cli = Clicycle()
        assert cli.is_verbose is False

    def test_update_progress(self):
        """Test update_progress method."""
        cli = Clicycle()
        cli._progress = MagicMock()
        cli._task_id = 1

        cli.update_progress(50.0, "Halfway")

        cli._progress.update.assert_any_call(1, description="Halfway")
        cli._progress.update.assert_any_call(1, completed=50.0)

    def test_update_progress_no_message(self):
        """Test update_progress without message."""
        cli = Clicycle()
        cli._progress = MagicMock()
        cli._task_id = 1

        cli.update_progress(75.0)

        cli._progress.update.assert_called_once_with(1, completed=75.0)

    def test_update_progress_no_active(self):
        """Test update_progress when no progress is active."""
        cli = Clicycle()
        cli._progress = None
        cli._task_id = None

        # Should not raise error
        cli.update_progress(50.0, "Test")

    def test_text_indentation(self):
        """Test that text methods respect indentation settings."""
        theme = Theme()
        theme.indentation = ComponentIndentation(
            info=2,
            success=4,
            error=0,
            warning=3,
            list=6
        )

        cli = Clicycle(theme=theme)
        cli.console = MagicMock()
        cli.stream = MagicMock()
        cli.stream.last_component = None

        # Test each method
        cli.info("Info")
        cli.success("Success")
        cli.error("Error")
        cli.warning("Warning")
        cli.list_item("Item")

        calls = cli.console.print.call_args_list

        # Check that appropriate indentation was applied
        # Info should have 2 spaces
        assert "  " in str(calls[0]) and "Info" in str(calls[0])
        # Success should have 4 spaces
        assert "    " in str(calls[1]) and "Success" in str(calls[1])
        # Error should have no indentation
        assert "Error" in str(calls[2])
        # Warning should have 3 spaces
        assert "   " in str(calls[3]) and "Warning" in str(calls[3])
        # List should have 6 spaces
        assert "      " in str(calls[4]) and "Item" in str(calls[4])
