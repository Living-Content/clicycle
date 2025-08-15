"""Tests for multi_progress component."""

from unittest.mock import MagicMock, patch

from rich.console import Console
from rich.progress import Progress

from clicycle.components.multi_progress import MultiProgress
from clicycle.theme import Theme


class TestMultiProgress:
    """Test the MultiProgress component."""

    def test_multi_progress_init(self):
        """Test MultiProgress initialization."""
        theme = Theme()
        console = MagicMock(spec=Console)

        mp = MultiProgress(theme, "Processing tasks", console)

        assert mp.description == "Processing tasks"
        assert mp.console is console
        assert mp._progress is None

    def test_multi_progress_render(self):
        """Test MultiProgress rendering."""
        theme = Theme()
        console = MagicMock(spec=Console)

        mp = MultiProgress(theme, "Processing", console)
        mp.render(console)

        # Should print progress description
        console.print.assert_called_once()
        call_args = console.print.call_args
        assert "Processing" in str(call_args)
        assert str(theme.icons.running) in str(call_args)

    @patch("clicycle.components.multi_progress.Progress")
    def test_multi_progress_track_context(self, mock_progress_class):
        """Test MultiProgress track context manager."""
        theme = Theme()
        console = MagicMock(spec=Console)
        mock_progress_instance = MagicMock(spec=Progress)
        mock_progress_class.return_value = mock_progress_instance
        # Mock the __enter__ to return the instance itself (as Rich Progress does)
        mock_progress_instance.__enter__.return_value = mock_progress_instance

        mp = MultiProgress(theme, "Processing", console)

        # Test track context manager
        with mp.track() as progress:
            # Should return what __enter__ returns (the Progress instance)
            assert progress is mock_progress_instance
            # Should create Rich Progress with correct columns
            mock_progress_class.assert_called_once()
            mock_progress_instance.__enter__.assert_called_once()

        # Should clean up
        mock_progress_instance.__exit__.assert_called_once()
        assert mp._progress is None

    @patch("clicycle.components.multi_progress.Progress")
    def test_multi_progress_enter_exit(self, mock_progress_class):
        """Test __enter__ and __exit__ methods."""
        theme = Theme()
        console = MagicMock(spec=Console)
        mock_progress_instance = MagicMock(spec=Progress)
        mock_progress_class.return_value = mock_progress_instance
        # Mock the __enter__ to return the instance itself (as Rich Progress does)
        mock_progress_instance.__enter__.return_value = mock_progress_instance

        mp = MultiProgress(theme, "Processing", console)

        # Test using with statement directly on mp
        with mp as progress:
            # Should return what __enter__ returns (the Progress instance)
            assert progress is mock_progress_instance
            mock_progress_class.assert_called_once()
            mock_progress_instance.__enter__.assert_called_once()

        # Should exit properly
        mock_progress_instance.__exit__.assert_called_once()

    def test_multi_progress_exit_no_context(self):
        """Test __exit__ when no context exists."""
        theme = Theme()
        console = MagicMock(spec=Console)

        mp = MultiProgress(theme, "Processing", console)
        # _context doesn't exist

        # Should not raise error
        result = mp.__exit__(None, None, None)
        assert result is False

    @patch("clicycle.components.multi_progress.Progress")
    def test_multi_progress_columns(self, mock_progress_class):
        """Test that Progress is created with correct columns."""
        theme = Theme()
        console = MagicMock(spec=Console)

        mp = MultiProgress(theme, "Processing", console)

        with mp.track():
            # Check the columns passed to Progress
            call_args = mock_progress_class.call_args
            columns = call_args[0] if call_args[0] else []

            # Should have multiple columns for multi-task display
            assert len(columns) >= 4  # short_id, description, bar, progress

            # Check console is passed
            assert call_args[1]["console"] is console
