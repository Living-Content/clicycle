"""Tests for prompt components."""

from unittest.mock import MagicMock, patch

from rich.console import Console

from clicycle.components.prompt import Confirm, Prompt, SelectList
from clicycle.theme import Theme


class TestPrompt:
    """Test the Prompt component."""

    def test_prompt_init(self):
        """Test Prompt initialization."""
        theme = Theme()
        console = MagicMock(spec=Console)

        prompt = Prompt(theme, "Enter name", console, default="John")

        assert prompt.text == "Enter name"
        assert prompt.console is console
        assert prompt.kwargs == {"default": "John"}

    def test_prompt_render_does_nothing(self):
        """Test that render method does nothing."""
        theme = Theme()
        console = MagicMock(spec=Console)

        prompt = Prompt(theme, "Enter name", console)
        prompt.render(console)

        # Should not call console
        console.print.assert_not_called()

    @patch('clicycle.components.prompt.RichPrompt')
    def test_prompt_ask(self, mock_rich_prompt):
        """Test asking for input."""
        theme = Theme()
        console = MagicMock(spec=Console)
        mock_rich_prompt.ask.return_value = "user input"

        prompt = Prompt(theme, "Enter name", console, default="John")
        result = prompt.ask()

        assert result == "user input"
        mock_rich_prompt.ask.assert_called_once_with(
            f"{theme.icons.info} Enter name",
            console=console,
            default="John"
        )


class TestConfirm:
    """Test the Confirm component."""

    def test_confirm_init(self):
        """Test Confirm initialization."""
        theme = Theme()
        console = MagicMock(spec=Console)

        confirm = Confirm(theme, "Continue?", console, default=True)

        assert confirm.text == "Continue?"
        assert confirm.console is console
        assert confirm.kwargs == {"default": True}

    def test_confirm_render_does_nothing(self):
        """Test that render method does nothing."""
        theme = Theme()
        console = MagicMock(spec=Console)

        confirm = Confirm(theme, "Continue?", console)
        confirm.render(console)

        # Should not call console
        console.print.assert_not_called()

    @patch('clicycle.components.prompt.RichConfirm')
    def test_confirm_ask(self, mock_rich_confirm):
        """Test asking for confirmation."""
        theme = Theme()
        console = MagicMock(spec=Console)
        mock_rich_confirm.ask.return_value = True

        confirm = Confirm(theme, "Continue?", console, default=False)
        result = confirm.ask()

        assert result is True
        mock_rich_confirm.ask.assert_called_once_with(
            f"{theme.icons.warning} Continue?",
            console=console,
            default=False
        )


class TestSelectList:
    """Test the SelectList component."""

    def test_selectlist_init(self):
        """Test SelectList initialization."""
        theme = Theme()
        console = MagicMock(spec=Console)
        options = ["Option A", "Option B", "Option C"]

        select = SelectList(theme, "option", options, console, default="Option B")

        assert select.item_name == "option"
        assert select.options == options
        assert select.console is console
        assert select.default == "Option B"

    def test_selectlist_render(self):
        """Test rendering the options list."""
        theme = Theme()
        console = MagicMock(spec=Console)
        options = ["Red", "Green", "Blue"]

        select = SelectList(theme, "color", options, console)
        select.render(console)

        # Should print header and all options
        calls = console.print.call_args_list
        assert len(calls) == 4  # Header + 3 options

        # Check header
        assert f"{theme.icons.info} Available colors:" in str(calls[0])

        # Check options
        assert "1. Red" in str(calls[1])
        assert "2. Green" in str(calls[2])
        assert "3. Blue" in str(calls[3])

    @patch('clicycle.components.prompt.RichPrompt')
    def test_selectlist_ask_valid_choice(self, mock_rich_prompt):
        """Test asking for a valid selection."""
        theme = Theme()
        console = MagicMock(spec=Console)
        options = ["Red", "Green", "Blue"]
        mock_rich_prompt.ask.return_value = "2"

        select = SelectList(theme, "color", options, console)
        result = select.ask()

        assert result == "Green"
        mock_rich_prompt.ask.assert_called_once_with(
            f"{theme.icons.info} Select a color",
            console=console,
            default=None
        )

    @patch('clicycle.components.prompt.RichPrompt')
    def test_selectlist_ask_with_default(self, mock_rich_prompt):
        """Test asking with a default option."""
        theme = Theme()
        console = MagicMock(spec=Console)
        options = ["Red", "Green", "Blue"]
        mock_rich_prompt.ask.return_value = "3"

        select = SelectList(theme, "color", options, console, default="Blue")
        result = select.ask()

        assert result == "Blue"
        # Should show default index (3)
        mock_rich_prompt.ask.assert_called_once_with(
            f"{theme.icons.info} Select a color (default: 3)",
            console=console,
            default='3'
        )

    @patch('clicycle.components.prompt.RichPrompt')
    def test_selectlist_ask_invalid_choice_too_high(self, mock_rich_prompt):
        """Test invalid selection - number too high."""
        theme = Theme()
        console = MagicMock(spec=Console)
        options = ["Red", "Green", "Blue"]
        mock_rich_prompt.ask.return_value = "5"

        select = SelectList(theme, "color", options, console)

        try:
            select.ask()
            raise AssertionError("Should have raised ValueError")
        except ValueError as e:
            assert "Invalid selection" in str(e)
            assert "between 1 and 3" in str(e)

    @patch('clicycle.components.prompt.RichPrompt')
    def test_selectlist_ask_invalid_choice_too_low(self, mock_rich_prompt):
        """Test invalid selection - number too low."""
        theme = Theme()
        console = MagicMock(spec=Console)
        options = ["Red", "Green", "Blue"]
        mock_rich_prompt.ask.return_value = "0"

        select = SelectList(theme, "color", options, console)

        try:
            select.ask()
            raise AssertionError("Should have raised ValueError")
        except ValueError as e:
            assert "Invalid selection" in str(e)

    @patch('clicycle.components.prompt.RichPrompt')
    def test_selectlist_ask_invalid_choice_not_number(self, mock_rich_prompt):
        """Test invalid selection - not a number."""
        theme = Theme()
        console = MagicMock(spec=Console)
        options = ["Red", "Green", "Blue"]
        mock_rich_prompt.ask.return_value = "abc"

        select = SelectList(theme, "color", options, console)

        try:
            select.ask()
            raise AssertionError("Should have raised ValueError")
        except ValueError as e:
            assert "Invalid selection" in str(e)

    @patch('clicycle.components.prompt.RichPrompt')
    def test_selectlist_ask_edge_cases(self, mock_rich_prompt):
        """Test edge cases for selection."""
        theme = Theme()
        console = MagicMock(spec=Console)
        options = ["Only Option"]

        # Test selecting the only option
        mock_rich_prompt.ask.return_value = "1"
        select = SelectList(theme, "item", options, console)
        result = select.ask()
        assert result == "Only Option"
