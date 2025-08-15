"""Tests for progress components."""

from unittest.mock import MagicMock, patch

from rich.console import Console

from clicycle.components.progress import ProgressBar
from clicycle.theme import Theme


class TestProgressBar:
    """Test the ProgressBar component."""

    def test_progressbar_init(self):
        """Test ProgressBar initialization."""
        theme = Theme()
        console = MagicMock(spec=Console)

        pb = ProgressBar(theme, "Loading", console)

        assert pb.description == "Loading"
        assert pb.console is console
        assert pb._progress is None
        assert pb._task_id is None

    def test_progressbar_render(self):
        """Test ProgressBar rendering."""
        theme = Theme()
        console = MagicMock(spec=Console)

        pb = ProgressBar(theme, "Progress", console)
        pb.render(console)

        # ProgressBar.render() should not print anything
        # The description is printed in the track() context manager
        console.print.assert_not_called()

    @patch("clicycle.components.progress.Progress")
    def test_progressbar_context_manager(self, mock_progress_class):
        """Test ProgressBar as context manager."""
        theme = Theme()
        console = MagicMock(spec=Console)
        mock_progress_instance = MagicMock()
        mock_progress_class.return_value = mock_progress_instance
        mock_progress_instance.add_task.return_value = 123

        pb = ProgressBar(theme, "Processing", console)

        # Test track context manager
        with pb.track():
            # Should print the description first
            console.print.assert_called_once()
            call_args = console.print.call_args
            assert "Processing" in str(call_args[0][0])
            assert theme.icons.running in str(call_args[0][0])

            # Should create Rich Progress
            mock_progress_class.assert_called_once()
            assert pb._progress is mock_progress_instance
            assert pb._task_id == 123
            mock_progress_instance.__enter__.assert_called_once()

        # Should clean up
        mock_progress_instance.__exit__.assert_called_once()
        assert pb._progress is None
        assert pb._task_id is None

    def test_progressbar_update_with_message(self):
        """Test updating progress with message."""
        theme = Theme()
        console = MagicMock(spec=Console)

        pb = ProgressBar(theme, "Processing", console)
        pb._progress = MagicMock()
        pb._task_id = 456

        # Update progress
        pb.update(50.0, "Halfway there")

        # Should update both description and progress
        pb._progress.update.assert_any_call(456, description="Halfway there")
        pb._progress.update.assert_any_call(456, completed=50.0)

    def test_progressbar_update_no_message(self):
        """Test updating progress without message."""
        theme = Theme()
        console = MagicMock(spec=Console)

        pb = ProgressBar(theme, "Processing", console)
        pb._progress = MagicMock()
        pb._task_id = 789

        # Update progress without message
        pb.update(75.0)

        # Should only update progress
        pb._progress.update.assert_called_once_with(789, completed=75.0)

    def test_progressbar_update_no_progress(self):
        """Test updating when progress is not active."""
        theme = Theme()
        console = MagicMock(spec=Console)

        pb = ProgressBar(theme, "Processing", console)
        # _progress is None

        # Should not raise error
        pb.update(50.0, "Halfway")

    @patch("clicycle.components.progress.Progress")
    def test_progressbar_enter_exit(self, mock_progress_class):
        """Test __enter__ and __exit__ methods."""
        theme = Theme()
        console = MagicMock(spec=Console)
        mock_progress_instance = MagicMock()
        mock_progress_class.return_value = mock_progress_instance
        mock_progress_instance.add_task.return_value = 999

        pb = ProgressBar(theme, "Processing", console)

        # Test using with statement directly on pb
        with pb as progress_bar:
            assert progress_bar is pb
            mock_progress_class.assert_called_once()
            mock_progress_instance.__enter__.assert_called_once()

        # Should exit properly
        mock_progress_instance.__exit__.assert_called_once()

    def test_progressbar_exit_no_progress(self):
        """Test __exit__ when no progress exists."""
        theme = Theme()
        console = MagicMock(spec=Console)

        pb = ProgressBar(theme, "Processing", console)
        # _progress is None

        # Should not raise error
        result = pb.__exit__(None, None, None)
        assert result is False
