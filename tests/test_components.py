"""Unit tests for clicycle components."""

from unittest.mock import MagicMock, patch

from rich.console import Console
from rich.syntax import Syntax
from rich.table import Table as RichTable

from clicycle.components.code import Code
from clicycle.components.header import Header
from clicycle.components.section import Section
from clicycle.components.spinner import Spinner
from clicycle.components.table import Table
from clicycle.components.text import Debug, Text
from clicycle.theme import Theme


class TestBaseComponent:
    """Test the base Component class."""

    def test_get_spacing_before_no_previous(self):
        """Test spacing calculation with no previous component."""
        theme = Theme()
        comp = Text(theme, "test", "info")
        comp.set_context(None)
        assert comp.get_spacing_before() == 0

    def test_get_spacing_before_with_rules(self):
        """Test spacing calculation with defined rules."""
        theme = Theme()
        theme.spacing.info = {"error": 2}

        prev_comp = Text(theme, "error", "error")
        comp = Text(theme, "info", "info")
        comp.set_context(prev_comp)

        assert comp.get_spacing_before() == 2

    def test_get_spacing_before_default(self):
        """Test default spacing when no rule defined."""
        theme = Theme()
        prev_comp = Text(theme, "test", "custom")
        comp = Text(theme, "info", "info")
        comp.set_context(prev_comp)

        assert comp.get_spacing_before() == 1

    def test_get_spacing_before_transient_reduction(self):
        """Test spacing reduction when previous component was transient."""
        theme = Theme()
        prev_comp = MagicMock()
        prev_comp.component_type = "spinner"
        prev_comp.was_transient = True

        comp = Text(theme, "info", "info")
        comp.set_context(prev_comp)
        # Default spacing is 1, reduced by 1 for transient = 0
        assert comp.get_spacing_before() == 0


class TestText:
    """Test the Text component."""

    def test_text_render(self):
        """Test text component rendering."""
        theme = Theme()
        console = MagicMock(spec=Console)

        text = Text(theme, "Hello", "info")
        text.render(console)

        console.print.assert_called_once()
        call_args = console.print.call_args[0]
        assert "Hello" in str(call_args)

    def test_text_with_indentation(self):
        """Test text component with indentation."""
        theme = Theme()
        theme.indentation.info = 4
        console = MagicMock(spec=Console)

        text = Text(theme, "Indented", "info")
        text.render(console)

        console.print.assert_called_once()
        call_args = console.print.call_args[0]
        assert "    " in str(call_args)  # 4 spaces


class TestHeader:
    """Test the Header component."""

    def test_header_basic(self):
        """Test basic header rendering."""
        theme = Theme()
        console = MagicMock(spec=Console)

        header = Header(theme, "Title")
        header.render(console)

        # Header calls print multiple times
        assert console.print.call_count >= 1

    def test_header_with_subtitle_and_app(self):
        """Test header with all fields."""
        theme = Theme()
        console = MagicMock(spec=Console)

        header = Header(theme, "Title", "Subtitle", "AppName")
        header.render(console)

        # Check that all parts were printed
        calls = [str(call) for call in console.print.call_args_list]
        all_calls = " ".join(calls)
        assert "TITLE" in all_calls  # Header converts to uppercase
        assert "Subtitle" in all_calls
        assert "AppName" in all_calls


class TestSection:
    """Test the Section component."""

    def test_section_render(self):
        """Test section rendering."""
        theme = Theme()
        console = MagicMock(spec=Console)

        section = Section(theme, "Section Title")
        section.render(console)

        # Section uses console.rule(), not print()
        console.rule.assert_called_once()
        call_args = console.rule.call_args
        # Check the actual call content
        assert "SECTION TITLE" in str(call_args)  # Title is transformed to uppercase


class TestListItem:
    """Test list_item functionality through text component."""

    def test_list_item_style(self):
        """Test that list items use the list style."""
        theme = Theme()
        console = MagicMock(spec=Console)

        # list_item creates a Text component with "list" style
        text = Text(theme, "Item 1", "list")
        text.render(console)

        console.print.assert_called_once()
        call_args = console.print.call_args[0]
        assert "Item 1" in str(call_args)

    def test_list_item_indentation(self):
        """Test list item indentation."""
        theme = Theme()
        theme.indentation.list = 6
        console = MagicMock(spec=Console)

        text = Text(theme, "Indented item", "list")
        text.render(console)

        console.print.assert_called_once()
        call_args = console.print.call_args[0]
        assert "      " in str(call_args)  # 6 spaces


class TestTable:
    """Test the Table component."""

    def test_table_render(self):
        """Test table rendering."""
        theme = Theme()
        console = MagicMock(spec=Console)

        data = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25}
        ]
        table = Table(theme, data, title="Users")
        table.render(console)

        console.print.assert_called()
        # Should create a Rich Table
        call_args = console.print.call_args[0]
        assert isinstance(call_args[0], RichTable)

    def test_table_empty(self):
        """Test table with no data."""
        theme = Theme()
        console = MagicMock(spec=Console)

        table = Table(theme, [], title="Empty")
        table.render(console)

        # Empty table returns early and doesn't print anything
        console.print.assert_not_called()


class TestCode:
    """Test the Code component."""

    def test_code_render(self):
        """Test code rendering."""
        theme = Theme()
        console = MagicMock(spec=Console)

        code = Code(theme, "print('hello')", language="python", title="Example")
        code.render(console)

        console.print.assert_called()
        # Should create a Syntax object
        call_args = console.print.call_args[0]
        assert isinstance(call_args[0], Syntax)

    def test_code_with_line_numbers(self):
        """Test code with line numbers."""
        theme = Theme()
        console = MagicMock(spec=Console)

        code = Code(theme, "line1\nline2", language="text", line_numbers=True)
        code.render(console)

        console.print.assert_called()


class TestDebug:
    """Test the Debug component."""

    @patch('click.get_current_context')
    def test_debug_verbose_true(self, mock_get_context):
        """Test debug renders when verbose is True."""
        theme = Theme()
        console = MagicMock(spec=Console)

        mock_ctx = MagicMock()
        mock_ctx.obj = {"verbose": True}
        mock_get_context.return_value = mock_ctx

        debug = Debug(theme, "Debug info")
        debug.render(console)

        # Should render the message
        console.print.assert_called_once()

    @patch('click.get_current_context')
    def test_debug_verbose_false(self, mock_get_context):
        """Test debug doesn't render when verbose is False."""
        theme = Theme()
        console = MagicMock(spec=Console)

        mock_ctx = MagicMock()
        mock_ctx.obj = {"verbose": False}
        mock_get_context.return_value = mock_ctx

        debug = Debug(theme, "Debug info")
        debug.render(console)

        # Should not render
        console.print.assert_not_called()

    @patch('click.get_current_context')
    def test_debug_no_context(self, mock_get_context):
        """Test debug doesn't render when no context."""
        theme = Theme()
        console = MagicMock(spec=Console)

        mock_get_context.side_effect = RuntimeError("No context")

        debug = Debug(theme, "Debug info")
        debug.render(console)

        # Should not render
        console.print.assert_not_called()


class TestSpinner:
    """Test the Spinner component."""

    def test_spinner_context_manager(self):
        """Test spinner as context manager."""
        theme = Theme()
        console = MagicMock()
        console.is_jupyter = False
        console._live_stack = []
        console.set_live = MagicMock(return_value=True)
        console.set_alt_screen = MagicMock(return_value=False)
        console.show_cursor = MagicMock()
        console.push_render_hook = MagicMock()
        console.pop_render_hook = MagicMock()
        console.print = MagicMock()
        console.status = MagicMock()

        spinner = Spinner(theme, "Loading...", console)

        # Test context manager
        with spinner:
            assert spinner._context is not None

        # After exit, context should be cleaned up
        assert spinner._context is not None  # But reference remains

    def test_spinner_disappearing(self):
        """Test disappearing spinner mode."""
        theme = Theme(disappearing_spinners=True)
        console = MagicMock(spec=Console)

        spinner = Spinner(theme, "Loading...", console)
        assert spinner.was_transient is True

    def test_spinner_persistent(self):
        """Test persistent spinner mode."""
        theme = Theme(disappearing_spinners=False)
        console = MagicMock(spec=Console)

        spinner = Spinner(theme, "Loading...", console)
        assert spinner.was_transient is False

    @patch("clicycle.components.spinner.Live")
    def test_spinner_disappearing_live(self, mock_live):
        """Test disappearing spinner uses Live with transient."""
        theme = Theme(disappearing_spinners=True)
        console = MagicMock(spec=Console)

        spinner = Spinner(theme, "Loading...", console)
        mock_context = MagicMock()
        mock_live.return_value = mock_context

        with spinner:
            mock_live.assert_called_once()
            # Check that transient=True was passed
            call_kwargs = mock_live.call_args[1]
            assert call_kwargs["transient"] is True

    def test_spinner_persistent_status(self):
        """Test persistent spinner uses console.status."""
        theme = Theme(disappearing_spinners=False)
        console = MagicMock(spec=Console)
        mock_status = MagicMock()
        console.status.return_value = mock_status

        spinner = Spinner(theme, "Loading...", console)

        with spinner:
            console.status.assert_called_once_with(
                "Loading...",
                spinner=theme.spinner_type,
                spinner_style=theme.typography.info_style
            )
