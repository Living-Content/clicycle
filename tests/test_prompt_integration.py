"""Integration tests for prompt components through clicycle."""

from unittest.mock import patch

from rich.console import Console

import clicycle as cc


class TestPromptIntegration:
    """Test prompts through the full clicycle flow."""

    def test_prompt_full_flow(self):
        """Test prompt through clicycle wrapper."""
        with patch("rich.prompt.Prompt.ask") as mock_rich_ask:
            mock_rich_ask.return_value = "user input"

            result = cc.prompt("Enter name", default="John")

            # Rich should be called with the correct parameters
            mock_rich_ask.assert_called_once()
            call_args = mock_rich_ask.call_args
            assert call_args[0][0] == "Enter name"
            assert call_args.kwargs.get("default") == "John"
            assert isinstance(call_args.kwargs.get("console"), Console)

            # Should return the user input
            assert result == "user input"

    def test_confirm_full_flow(self):
        """Test confirm through clicycle wrapper."""
        with patch("rich.prompt.Confirm.ask") as mock_rich_ask:
            mock_rich_ask.return_value = True

            result = cc.confirm("Are you sure?", default=False)

            # Rich should be called with the correct parameters
            mock_rich_ask.assert_called_once()
            call_args = mock_rich_ask.call_args
            assert call_args[0][0] == "Are you sure?"
            assert call_args.kwargs.get("default") is False
            assert isinstance(call_args.kwargs.get("console"), Console)

            # Should return the boolean result
            assert result is True

    def test_select_list_full_flow(self):
        """Test select_list through clicycle wrapper."""
        options = ["option1", "option2", "option3"]

        with patch("rich.prompt.Prompt.ask") as mock_rich_ask:
            mock_rich_ask.return_value = "2"

            result = cc.select_list("item", options, default="option2")

            # Rich should be called with the correct parameters
            mock_rich_ask.assert_called_once()
            call_args = mock_rich_ask.call_args
            assert "Select a item" in call_args[0][0]
            assert call_args.kwargs.get("default") == "2"  # Default index
            assert isinstance(call_args.kwargs.get("console"), Console)

            # Should return the selected option
            assert result == "option2"

    def test_prompt_spacing(self):
        """Test that prompts get proper spacing through the stream."""
        with (
            patch("rich.prompt.Prompt.ask") as mock_rich_ask,
            patch("clicycle.rendering.stream.RenderStream.render") as mock_render,
        ):
            mock_rich_ask.return_value = "test"

            cc.prompt("Test prompt")

            # Should have rendered through the stream
            mock_render.assert_called_once()

    def test_multiple_prompts_in_sequence(self):
        """Test multiple prompts in sequence work correctly."""
        with (
            patch("rich.prompt.Prompt.ask") as mock_prompt,
            patch("rich.prompt.Confirm.ask") as mock_confirm,
        ):
            mock_prompt.return_value = "John"
            mock_confirm.return_value = True

            name = cc.prompt("Enter name")
            confirmed = cc.confirm("Is this correct?")

            assert name == "John"
            assert confirmed is True
            assert mock_prompt.call_count == 1
            assert mock_confirm.call_count == 1

    def test_select_list_with_console_output(self):
        """Test that select_list prints options to console."""
        options = ["red", "green", "blue"]

        with (
            patch("rich.prompt.Prompt.ask") as mock_rich_ask,
            patch.object(cc._cli.console, "print") as mock_print,
        ):
            mock_rich_ask.return_value = "1"

            result = cc.select_list("color", options)

            # Should print the list of options
            mock_print.assert_any_call("Available colors:")
            mock_print.assert_any_call("  1. red")
            mock_print.assert_any_call("  2. green")
            mock_print.assert_any_call("  3. blue")

            assert result == "red"

    def test_prompt_with_kwargs(self):
        """Test that prompt passes through all kwargs correctly."""
        with patch("rich.prompt.Prompt.ask") as mock_rich_ask:
            mock_rich_ask.return_value = "password123"

            result = cc.prompt(
                "Enter password", password=True, default="", show_default=False
            )

            # Check kwargs were passed through
            call_kwargs = mock_rich_ask.call_args.kwargs
            assert call_kwargs.get("password") is True
            assert call_kwargs.get("default") == ""
            assert call_kwargs.get("show_default") is False

            assert result == "password123"

    def test_confirm_with_kwargs(self):
        """Test that confirm passes through all kwargs correctly."""
        with patch("rich.prompt.Confirm.ask") as mock_rich_ask:
            mock_rich_ask.return_value = False

            result = cc.confirm("Delete file?", default=False, show_default=True)

            # Check kwargs were passed through
            call_kwargs = mock_rich_ask.call_args.kwargs
            assert call_kwargs.get("default") is False
            assert call_kwargs.get("show_default") is True

            assert result is False
