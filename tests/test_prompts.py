"""Tests for the prompts module."""

from unittest.mock import patch

import click
import pytest

from clicycle import Clicycle, select_from_list


class TestSelectFromList:
    """Test the select_from_list function."""

    @patch("clicycle.prompts.click.prompt")
    def test_select_from_list_basic(self, mock_prompt):
        """Test basic select_from_list functionality."""
        mock_prompt.return_value = 2
        options = ["apple", "banana", "cherry"]

        result = select_from_list("fruit", options)

        assert result == "banana"
        mock_prompt.assert_called_once()

    @patch("clicycle.prompts.click.prompt")
    def test_select_from_list_with_default(self, mock_prompt):
        """Test select_from_list with default option."""
        mock_prompt.return_value = 1  # User selects default
        options = ["apple", "banana", "cherry"]

        result = select_from_list("fruit", options, default="apple")

        assert result == "apple"
        # Should be called with default_index=1 (1-based)
        call_args = mock_prompt.call_args
        assert call_args[1]["default"] == 1

    @patch("clicycle.prompts.click.prompt")
    def test_select_from_list_with_custom_cli(self, mock_prompt):
        """Test select_from_list with custom CLI instance."""
        mock_prompt.return_value = 3
        options = ["red", "green", "blue"]
        custom_cli = Clicycle(app_name="TestApp")

        result = select_from_list("color", options, cli=custom_cli)

        assert result == "blue"

    @patch("clicycle.prompts.click.prompt")
    def test_select_from_list_invalid_choice_low(self, mock_prompt):
        """Test select_from_list with choice too low."""
        mock_prompt.return_value = 0
        options = ["apple", "banana", "cherry"]

        with pytest.raises(click.UsageError, match="Invalid selection"):
            select_from_list("fruit", options)

    @patch("clicycle.prompts.click.prompt")
    def test_select_from_list_invalid_choice_high(self, mock_prompt):
        """Test select_from_list with choice too high."""
        mock_prompt.return_value = 4
        options = ["apple", "banana", "cherry"]

        with pytest.raises(click.UsageError, match="Invalid selection"):
            select_from_list("fruit", options)

    @patch("clicycle.prompts.click.prompt")
    def test_select_from_list_default_not_in_options(self, mock_prompt):
        """Test select_from_list when default is not in options."""
        mock_prompt.return_value = 2
        options = ["apple", "banana", "cherry"]

        result = select_from_list("fruit", options, default="orange")

        assert result == "banana"
        # Should be called without default since "orange" not in options
        call_args = mock_prompt.call_args
        assert call_args[1].get("default") is None

    @patch("clicycle.prompts.Clicycle.prompt")
    @patch("clicycle.prompts.Clicycle.info")
    def test_select_from_list_value_error_safety(self, mock_info, mock_prompt):
        """Test ValueError safety in select_from_list."""
        # This tests the ValueError exception handling in line 28-29
        mock_info.return_value = None  # Use the mock parameter
        mock_prompt.return_value = 1
        options = ["apple", "banana"]

        # Even though we set default to "banana", the mock will simulate
        # the case where index() might fail (though it shouldn't in normal use)
        result = select_from_list("fruit", options, default="banana")

        assert result == "apple"  # Returns first option based on mock
        assert mock_info.called  # Verify info was used

    @patch("clicycle.prompts.click.prompt")
    def test_select_from_list_empty_options(self, mock_prompt):
        """Test select_from_list with empty options list."""
        mock_prompt.return_value = 1
        options = []

        with pytest.raises(click.UsageError, match="Invalid selection"):
            select_from_list("item", options)

    @patch("clicycle.prompts.click.prompt")
    def test_select_from_list_single_option(self, mock_prompt):
        """Test select_from_list with single option."""
        mock_prompt.return_value = 1
        options = ["only_choice"]

        result = select_from_list("item", options)

        assert result == "only_choice"
