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

        prompt = Prompt(theme, "Enter name", default="John")

        assert prompt.text == "Enter name"
        assert prompt.kwargs == {"default": "John"}

    def test_prompt_render_asks_for_input(self):
        """Test that render method asks for input."""
        theme = Theme()
        console = MagicMock(spec=Console)

        prompt = Prompt(theme, "Enter name")

        with patch("rich.prompt.Prompt.ask") as mock_ask:
            mock_ask.return_value = "test value"
            prompt.render(console)

            assert prompt.result == "test value"
            mock_ask.assert_called_once_with("Enter name", console=console)

    def test_prompt_ask_returns_result(self):
        """Test ask returns the result from render."""
        theme = Theme()
        console = MagicMock(spec=Console)

        prompt = Prompt(theme, "Enter name")

        with patch("rich.prompt.Prompt.ask") as mock_ask:
            mock_ask.return_value = "John Doe"
            prompt.render(console)
            result = prompt.ask()

            assert result == "John Doe"


class TestConfirm:
    """Test the Confirm component."""

    def test_confirm_init(self):
        """Test Confirm initialization."""
        theme = Theme()

        confirm = Confirm(theme, "Are you sure?", default=True)

        assert confirm.text == "Are you sure?"
        assert confirm.kwargs == {"default": True}

    def test_confirm_render_asks_for_confirmation(self):
        """Test that render method asks for confirmation."""
        theme = Theme()
        console = MagicMock(spec=Console)

        confirm = Confirm(theme, "Continue?")

        with patch("rich.prompt.Confirm.ask") as mock_ask:
            mock_ask.return_value = True
            confirm.render(console)

            assert confirm.result is True
            mock_ask.assert_called_once_with("Continue?", console=console)

    def test_confirm_ask_returns_result(self):
        """Test ask returns the result from render."""
        theme = Theme()
        console = MagicMock(spec=Console)

        confirm = Confirm(theme, "Continue?")

        with patch("rich.prompt.Confirm.ask") as mock_ask:
            mock_ask.return_value = False
            confirm.render(console)
            result = confirm.ask()

            assert result is False


class TestSelectList:
    """Test the SelectList component."""

    def test_selectlist_init(self):
        """Test SelectList initialization."""
        theme = Theme()
        options = ["opt1", "opt2", "opt3"]

        select_list = SelectList(theme, "item", options, default="opt2")

        assert select_list.item_name == "item"
        assert select_list.options == options
        assert select_list.default == "opt2"

    def test_selectlist_render(self):
        """Test rendering the options list."""
        theme = Theme()
        console = MagicMock(spec=Console)
        options = ["opt1", "opt2"]

        select_list = SelectList(theme, "item", options)

        with patch("rich.prompt.Prompt.ask") as mock_ask:
            mock_ask.return_value = "1"
            select_list.render(console)

            # Check that options were printed
            console.print.assert_any_call("Available items:")
            console.print.assert_any_call("  1. opt1")
            console.print.assert_any_call("  2. opt2")

            # Check result
            assert select_list.result == "opt1"

    def test_selectlist_ask_returns_result(self):
        """Test ask returns the result from render."""
        theme = Theme()
        console = MagicMock(spec=Console)
        options = ["opt1", "opt2", "opt3"]

        select_list = SelectList(theme, "item", options)

        with patch("rich.prompt.Prompt.ask") as mock_ask:
            mock_ask.return_value = "2"
            select_list.render(console)
            result = select_list.ask()

            assert result == "opt2"

    def test_selectlist_with_default(self):
        """Test select list with default value."""
        theme = Theme()
        console = MagicMock(spec=Console)
        options = ["opt1", "opt2", "opt3"]

        select_list = SelectList(theme, "item", options, default="opt2")

        with patch("rich.prompt.Prompt.ask") as mock_ask:
            mock_ask.return_value = "2"
            select_list.render(console)

            # Check that default was included in prompt
            mock_ask.assert_called_once_with(
                "Select a item (default: 2)", console=console, default="2"
            )

    def test_selectlist_invalid_choice_raises(self):
        """Test invalid choice raises ValueError."""
        theme = Theme()
        console = MagicMock(spec=Console)
        options = ["opt1", "opt2"]

        select_list = SelectList(theme, "item", options)

        with patch("rich.prompt.Prompt.ask") as mock_ask:
            mock_ask.return_value = "5"  # Invalid choice

            try:
                select_list.render(console)
                raise AssertionError("Should have raised ValueError")
            except ValueError as e:
                assert "Invalid selection" in str(e)

    def test_selectlist_non_numeric_choice_raises(self):
        """Test non-numeric choice raises ValueError."""
        theme = Theme()
        console = MagicMock(spec=Console)
        options = ["opt1", "opt2"]

        select_list = SelectList(theme, "item", options)

        with patch("rich.prompt.Prompt.ask") as mock_ask:
            mock_ask.return_value = "abc"  # Non-numeric

            try:
                select_list.render(console)
                raise AssertionError("Should have raised ValueError")
            except ValueError as e:
                assert "Invalid selection" in str(e)

    def test_selectlist_edge_cases(self):
        """Test edge cases for SelectList."""
        theme = Theme()
        console = MagicMock(spec=Console)

        # Test with empty string
        select_list = SelectList(theme, "item", ["opt1"])

        with patch("rich.prompt.Prompt.ask") as mock_ask:
            mock_ask.return_value = None  # Empty input

            try:
                select_list.render(console)
                raise AssertionError("Should have raised ValueError")
            except ValueError:
                pass  # Expected
