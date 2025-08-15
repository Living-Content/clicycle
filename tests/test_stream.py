"""Tests for the RenderStream orchestrator."""

from unittest.mock import MagicMock, patch

from rich.console import Console

from clicycle.components.text import Info
from clicycle.rendering.stream import RenderStream
from clicycle.theme import Theme


class TestRenderStream:
    """Test the RenderStream orchestrator."""

    def test_render_stream_init(self):
        """Test RenderStream initialization."""
        console = Console()
        stream = RenderStream(console)

        assert stream.console is console
        assert stream.history == []
        assert stream.in_live_context is False
        assert stream.deferred_component is None

    def test_render_regular_component(self):
        """Test rendering a regular component."""
        console = MagicMock(spec=Console)
        stream = RenderStream(console)
        theme = Theme()

        component = Info(theme, "Test message")

        with patch.object(component, "render_with_spacing") as mock_render:
            stream.render(component)

            # Should have been rendered
            mock_render.assert_called_once_with(console)

            # Should be in history
            assert component in stream.history

    def test_render_deferred_component(self):
        """Test rendering a deferred component (progress/spinner)."""
        console = MagicMock(spec=Console)
        stream = RenderStream(console)
        Theme()

        # Create a mock progress component with deferred_render attribute
        progress = MagicMock()
        progress.deferred_render = True
        progress.set_context = MagicMock()
        progress.render_with_spacing = MagicMock()

        stream.render(progress)

        # Should have been rendered
        progress.render_with_spacing.assert_called_once_with(console)

        # Should be in history
        assert progress in stream.history

        # Should have set deferred tracking
        assert stream.deferred_component is progress
        assert stream.in_live_context is True

    def test_render_after_deferred_clears_tracking(self):
        """Test that rendering after a deferred component clears tracking."""
        console = MagicMock(spec=Console)
        stream = RenderStream(console)
        theme = Theme()

        # First render a mock spinner (deferred component)
        spinner = MagicMock()
        spinner.deferred_render = True
        spinner.set_context = MagicMock()
        spinner.render_with_spacing = MagicMock()
        stream.render(spinner)

        assert stream.deferred_component is spinner
        assert stream.in_live_context is True

        # Then render a regular component
        info = Info(theme, "Done")
        stream.render(info)

        # Deferred tracking should be cleared
        assert stream.deferred_component is None
        assert stream.in_live_context is False

    def test_last_component_property(self):
        """Test the last_component property."""
        console = MagicMock(spec=Console)
        stream = RenderStream(console)
        theme = Theme()

        # Initially should be None
        assert stream.last_component is None

        # After rendering a component
        info1 = Info(theme, "First")
        stream.render(info1)
        assert stream.last_component is info1

        # After rendering another
        info2 = Info(theme, "Second")
        stream.render(info2)
        assert stream.last_component is info2

    def test_clear_history(self):
        """Test clearing render history."""
        console = MagicMock(spec=Console)
        stream = RenderStream(console)
        theme = Theme()

        # Add some components to history
        info1 = Info(theme, "First")
        info2 = Info(theme, "Second")
        stream.render(info1)
        stream.render(info2)

        assert len(stream.history) == 2

        # Clear history
        stream.clear_history()

        assert stream.history == []
        assert stream.last_component is None

    def test_component_gets_context_from_last(self):
        """Test that components get context from the last component."""
        console = MagicMock(spec=Console)
        stream = RenderStream(console)
        theme = Theme()

        # Render first component
        info1 = Info(theme, "First")
        stream.render(info1)

        # Render second component
        info2 = Info(theme, "Second")

        with patch.object(info2, "set_context") as mock_set_context:
            stream.render(info2)

            # Should have been given the first component as context
            mock_set_context.assert_called_once_with(info1)

    def test_deferred_component_gets_context(self):
        """Test that deferred components get context from last component."""
        console = MagicMock(spec=Console)
        stream = RenderStream(console)
        theme = Theme()

        # Render a regular component first
        info = Info(theme, "Info message")
        stream.render(info)

        # Render a mock progress bar (deferred)
        progress = MagicMock()
        progress.deferred_render = True
        progress.render_with_spacing = MagicMock()
        progress.set_context = MagicMock()

        stream.render(progress)

        # Should have been given the info component as context
        progress.set_context.assert_called_once_with(info)

    def test_multiple_deferred_components(self):
        """Test rendering multiple deferred components in sequence."""
        console = MagicMock(spec=Console)
        stream = RenderStream(console)
        Theme()

        # Render first mock progress bar
        progress1 = MagicMock()
        progress1.deferred_render = True
        progress1.set_context = MagicMock()
        progress1.render_with_spacing = MagicMock()
        stream.render(progress1)

        assert stream.deferred_component is progress1
        assert stream.in_live_context is True

        # Render second mock progress bar
        progress2 = MagicMock()
        progress2.deferred_render = True
        progress2.set_context = MagicMock()
        progress2.render_with_spacing = MagicMock()
        stream.render(progress2)

        # Should have updated deferred component
        assert stream.deferred_component is progress2
        assert stream.in_live_context is True

        # Both should be in history
        assert progress1 in stream.history
        assert progress2 in stream.history
