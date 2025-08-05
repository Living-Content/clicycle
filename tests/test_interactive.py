"""Unit tests for interactive components."""

from unittest.mock import MagicMock, patch

from clicycle.interactive.multi_select import (
    _MultiSelectRenderer,
    interactive_multi_select,
)
from clicycle.interactive.select import _SelectRenderer, interactive_select
from clicycle.theme import Theme


class TestBaseRenderer:
    """Test the base renderer class."""

    def test_normalize_options_strings(self):
        """Test normalizing string options."""
        cli = MagicMock()
        renderer = _SelectRenderer("Title", ["Option 1", "Option 2"], 0, cli)

        assert len(renderer.options) == 2
        assert renderer.options[0] == {"label": "Option 1", "value": "Option 1"}
        assert renderer.options[1] == {"label": "Option 2", "value": "Option 2"}

    def test_normalize_options_dicts(self):
        """Test normalizing dict options."""
        cli = MagicMock()
        options = [
            {"label": "Option 1", "value": "opt1"},
            {"label": "Option 2", "value": "opt2", "description": "Description"},
        ]
        renderer = _SelectRenderer("Title", options, 0, cli)

        assert renderer.options == options

    def test_get_key_arrow_up(self):
        """Test parsing up arrow key."""
        cli = MagicMock()
        renderer = _SelectRenderer("Title", ["A", "B"], 0, cli)

        with patch("sys.stdin.read") as mock_read:
            mock_read.side_effect = ["\x1b", "[", "A"]
            key = renderer._get_key()
            assert key == "up"

    def test_get_key_arrow_down(self):
        """Test parsing down arrow key."""
        cli = MagicMock()
        renderer = _SelectRenderer("Title", ["A", "B"], 0, cli)

        with patch("sys.stdin.read") as mock_read:
            mock_read.side_effect = ["\x1b", "[", "B"]
            key = renderer._get_key()
            assert key == "down"

    def test_get_key_enter(self):
        """Test parsing enter key."""
        cli = MagicMock()
        renderer = _SelectRenderer("Title", ["A", "B"], 0, cli)

        with patch("sys.stdin.read") as mock_read:
            mock_read.return_value = "\r"
            key = renderer._get_key()
            assert key == "enter"

    def test_get_key_space(self):
        """Test parsing space key."""
        cli = MagicMock()
        renderer = _SelectRenderer("Title", ["A", "B"], 0, cli)

        with patch("sys.stdin.read") as mock_read:
            mock_read.return_value = " "
            key = renderer._get_key()
            assert key == "space"

    def test_get_key_quit(self):
        """Test parsing quit keys."""
        cli = MagicMock()
        renderer = _SelectRenderer("Title", ["A", "B"], 0, cli)

        # Test 'q'
        with patch("sys.stdin.read") as mock_read:
            mock_read.return_value = "q"
            key = renderer._get_key()
            assert key == "quit"

        # Test Ctrl+C
        with patch("sys.stdin.read") as mock_read:
            mock_read.return_value = "\x03"
            key = renderer._get_key()
            assert key == "quit"


class TestSelectRenderer:
    """Test the select renderer."""

    def test_format_label_special_cases(self):
        """Test special label formatting."""
        cli = MagicMock()
        cli.theme = Theme()

        renderer = _SelectRenderer("Title", ["Normal", "← Back", "Exit"], 0, cli)

        assert renderer._format_label(renderer.options[0]) == "Normal"
        assert renderer._format_label(renderer.options[1]) == "Back ←"
        assert "Exit" in renderer._format_label(renderer.options[2])
        assert str(cli.theme.icons.error) in renderer._format_label(renderer.options[2])

    @patch("sys.stdout.write")
    @patch("sys.stdout.flush")
    def test_setup_terminal(self, _mock_flush, mock_write):
        """Test terminal setup."""
        cli = MagicMock()
        cli.console = MagicMock()
        cli.theme = Theme()

        renderer = _SelectRenderer("Test Title", ["A", "B", "C"], 1, cli)
        renderer._setup_terminal()

        # Should print title
        cli.console.print.assert_called_with("\nTest Title")
        # Should hide cursor
        cli.console.show_cursor.assert_called_with(False)
        # Should write options
        assert mock_write.call_count >= 3  # At least one per option

    @patch("termios.tcgetattr")
    @patch("termios.tcsetattr")
    @patch("tty.setraw")
    @patch("sys.stdout.write")
    @patch("sys.stdout.flush")
    @patch("sys.stdin")
    def test_render_full_flow(
        self,
        mock_stdin,
        _mock_flush,
        _mock_write,
        _mock_setraw,
        mock_tcsetattr,
        mock_tcgetattr,
    ):
        """Test full render flow with selection."""
        # Mock stdin with fileno
        mock_stdin.fileno.return_value = 0
        mock_stdin.read.side_effect = ["\x1b", "[", "B", "\r"]

        cli = MagicMock()
        cli.console = MagicMock()
        cli.theme = Theme()

        # Mock terminal settings
        mock_tcgetattr.return_value = "old_settings"

        renderer = _SelectRenderer("Title", ["Option A", "Option B"], 0, cli)
        result = renderer.render()

        # Should select the second option (after moving down)
        assert result == "Option B"

        # Terminal should be restored
        mock_tcsetattr.assert_called()
        cli.console.show_cursor.assert_called_with(True)


class TestMultiSelectRenderer:
    """Test the multi-select renderer."""

    def test_init_with_defaults(self):
        """Test initialization with default selections."""
        cli = MagicMock()
        renderer = _MultiSelectRenderer(
            "Title",
            ["A", "B", "C"],
            [0, 2],  # Pre-select first and third
            0,
            None,
            cli,
        )

        assert renderer.selected_indices == {0, 2}
        assert renderer.min_selection == 0
        assert renderer.max_selection is None

    @patch("sys.stdout.write")
    @patch("sys.stdout.flush")
    def test_draw_line_option(self, _mock_flush, mock_write):
        """Test drawing an option line."""
        cli = MagicMock()
        cli.theme = Theme()

        renderer = _MultiSelectRenderer(
            "Title", ["Option A", "Option B"], None, 0, None, cli
        )
        renderer.selected_indices = {0}  # First option selected

        # Draw selected option
        renderer._draw_line(0, True)
        # Should show arrow, checkbox with checkmark, and label
        calls = [call[0][0] for call in mock_write.call_args_list]
        output = "".join(calls)
        assert "→" in output
        assert str(cli.theme.icons.success) in output
        assert "Option A" in output

    @patch("sys.stdout.write")
    @patch("sys.stdout.flush")
    def test_draw_line_submit(self, _mock_flush, mock_write):
        """Test drawing submit button."""
        cli = MagicMock()
        cli.theme = Theme()

        renderer = _MultiSelectRenderer("Title", ["A"], None, 0, None, cli)

        # Draw submit button (index = len(options))
        renderer._draw_line(1, True)
        calls = [call[0][0] for call in mock_write.call_args_list]
        output = "".join(calls)
        assert "→" in output
        assert "[Submit]" in output

    def test_toggle_selection(self):
        """Test toggling selection."""
        cli = MagicMock()
        cli.theme = Theme()

        renderer = _MultiSelectRenderer("Title", ["A", "B", "C"], None, 0, 2, cli)
        renderer.current_index = 1

        # Toggle on
        with patch.object(renderer, "_draw_line"):
            renderer._toggle_selection()
            assert 1 in renderer.selected_indices

        # Toggle off
        with patch.object(renderer, "_draw_line"):
            renderer._toggle_selection()
            assert 1 not in renderer.selected_indices

    def test_toggle_selection_max_limit(self):
        """Test toggle respects max selection."""
        cli = MagicMock()
        cli.theme = Theme()

        renderer = _MultiSelectRenderer("Title", ["A", "B", "C"], [0, 1], 0, 2, cli)
        renderer.current_index = 2

        # Should not add third selection (max is 2)
        with patch.object(renderer, "_draw_line"):
            renderer._toggle_selection()
            assert 2 not in renderer.selected_indices
            assert len(renderer.selected_indices) == 2

    @patch("termios.tcgetattr")
    @patch("termios.tcsetattr")
    @patch("tty.setraw")
    @patch("sys.stdout.write")
    @patch("sys.stdout.flush")
    @patch("sys.stdin")
    def test_render_with_selection(
        self,
        mock_stdin,
        _mock_flush,
        _mock_write,
        _mock_setraw,
        _mock_tcsetattr,
        _mock_tcgetattr,
    ):
        """Test full multi-select flow."""
        # Mock stdin with fileno
        mock_stdin.fileno.return_value = 0
        # Simulate: space (toggle first), down to B, down to C, down to Submit, enter
        mock_stdin.read.side_effect = [
            " ",
            "\x1b",
            "[",
            "B",
            "\x1b",
            "[",
            "B",
            "\x1b",
            "[",
            "B",
            "\r",
        ]

        cli = MagicMock()
        cli.console = MagicMock()
        cli.theme = Theme()

        _mock_tcgetattr.return_value = "old_settings"

        renderer = _MultiSelectRenderer("Title", ["A", "B", "C"], None, 0, None, cli)
        result = renderer.render()

        # Should have first item selected (toggled with space)
        assert result == ["A"]


class TestInteractiveFunctions:
    """Test the public interactive functions."""

    @patch("clicycle._cli")
    @patch("clicycle.interactive.select._SelectRenderer")
    def test_interactive_select(self, mock_renderer_class, mock_cli):
        """Test interactive_select function."""
        mock_renderer = MagicMock()
        mock_renderer.render.return_value = "selected_value"
        mock_renderer_class.return_value = mock_renderer

        result = interactive_select("Choose:", ["A", "B"], 1)

        assert result == "selected_value"
        mock_renderer_class.assert_called_once_with("Choose:", ["A", "B"], 1, mock_cli)
        mock_renderer.render.assert_called_once()

    @patch("clicycle._cli")
    @patch("clicycle.interactive.multi_select._MultiSelectRenderer")
    def test_interactive_multi_select(self, mock_renderer_class, mock_cli):
        """Test interactive_multi_select function."""
        mock_renderer = MagicMock()
        mock_renderer.render.return_value = ["A", "C"]
        mock_renderer_class.return_value = mock_renderer

        result = interactive_multi_select(
            "Choose multiple:",
            ["A", "B", "C"],
            [0, 2],
            min_selection=1,
            max_selection=3,
        )

        assert result == ["A", "C"]
        mock_renderer_class.assert_called_once_with(
            "Choose multiple:", ["A", "B", "C"], [0, 2], 1, 3, mock_cli
        )
