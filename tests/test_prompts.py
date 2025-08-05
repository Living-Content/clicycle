"""Tests for prompt components."""

from unittest.mock import patch

import pytest

from clicycle import Clicycle


class TestSelectFromList:
    """Test the select_from_list method."""

    @patch("rich.prompt.Prompt.ask")
    def test_select_from_list_basic(self, mock_ask):
        """Test basic select_from_list functionality."""
        mock_ask.return_value = "2"
        cli = Clicycle()
        options = ["apple", "banana", "cherry"]

        result = cli.select_from_list("fruit", options)

        assert result == "banana"
        mock_ask.assert_called_once()

    @patch("rich.prompt.Prompt.ask")
    def test_select_from_list_with_default(self, mock_ask):
        """Test select_from_list with default option."""
        mock_ask.return_value = 1  # User selects default
        cli = Clicycle()
        options = ["apple", "banana", "cherry"]

        result = cli.select_from_list("fruit", options, default="apple")

        assert result == "apple"

    @patch("rich.prompt.Prompt.ask")
    def test_select_from_list_invalid_choice_low(self, mock_ask):
        """Test select_from_list with choice too low."""
        mock_ask.return_value = "0"
        cli = Clicycle()
        options = ["apple", "banana", "cherry"]

        with pytest.raises(ValueError, match="Invalid selection"):
            cli.select_from_list("fruit", options)

    @patch("rich.prompt.Prompt.ask")
    def test_select_from_list_invalid_choice_high(self, mock_ask):
        """Test select_from_list with choice too high."""
        mock_ask.return_value = "4"
        cli = Clicycle()
        options = ["apple", "banana", "cherry"]

        with pytest.raises(ValueError, match="Invalid selection"):
            cli.select_from_list("fruit", options)

    @patch("rich.prompt.Prompt.ask")
    def test_select_from_list_default_not_in_options(self, mock_ask):
        """Test select_from_list when default is not in options."""
        mock_ask.return_value = "2"
        cli = Clicycle()
        options = ["apple", "banana", "cherry"]

        result = cli.select_from_list("fruit", options, default="orange")

        assert result == "banana"

    @patch("rich.prompt.Prompt.ask")
    def test_select_from_list_non_numeric_input(self, mock_ask):
        """Test select_from_list with non-numeric input."""
        mock_ask.return_value = "not a number"
        cli = Clicycle()
        options = ["apple", "banana", "cherry"]

        with pytest.raises(ValueError, match="Invalid selection"):
            cli.select_from_list("fruit", options)

    @patch("rich.prompt.Prompt.ask")
    def test_select_from_list_empty_options(self, mock_ask):
        """Test select_from_list with empty options list."""
        mock_ask.return_value = "1"
        cli = Clicycle()
        options = []

        with pytest.raises(ValueError, match="Invalid selection"):
            cli.select_from_list("item", options)

    @patch("rich.prompt.Prompt.ask")
    def test_select_from_list_single_option(self, mock_ask):
        """Test select_from_list with single option."""
        mock_ask.return_value = "1"
        cli = Clicycle()
        options = ["only_choice"]

        result = cli.select_from_list("item", options)

        assert result == "only_choice"
