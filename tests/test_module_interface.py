"""Tests for the module interface and convenience API."""

from unittest.mock import MagicMock, patch

import clicycle as cc
from clicycle import _ModuleInterface


class TestModuleInterface:
    """Test the module interface wrapper."""

    def test_module_replacement(self):
        """Test that the module is replaced with _ModuleInterface."""
        import sys
        assert isinstance(sys.modules['clicycle'], _ModuleInterface)

    def test_original_attributes_preserved(self):
        """Test that original module attributes are preserved."""
        # These should still exist
        assert hasattr(cc, 'Clicycle')
        assert hasattr(cc, 'Theme')
        assert hasattr(cc, '__version__')

    def test_cli_instance_created(self):
        """Test that _cli instance is created."""
        assert hasattr(cc, '_cli')
        assert isinstance(cc._cli, cc.Clicycle)

    def test_direct_attributes_available(self):
        """Test that direct attributes are available."""
        # Console is exposed via special attribute handler
        assert hasattr(cc, 'console')
        assert cc.console is cc._cli.console

        # Theme exists but it's the module, not the instance
        # The theme module was imported and is a module attribute
        assert hasattr(cc, 'theme')
        import clicycle.theme
        assert cc.theme is clicycle.theme

        # To get the CLI's theme instance:
        assert hasattr(cc._cli, 'theme')
        assert isinstance(cc._cli.theme, cc.Theme)

    def test_clear_method(self):
        """Test clear method."""
        with patch.object(cc._cli, 'clear') as mock_clear:
            cc.clear()
            mock_clear.assert_called_once()

    def test_configure_method(self):
        """Test configure method updates _cli."""
        new_theme = cc.Theme()
        cc.configure(width=120, theme=new_theme, app_name="Test")

        assert cc._cli.width == 120
        assert cc._cli.theme is new_theme
        assert cc._cli.app_name == "Test"
        assert cc._cli.console.width == 120

    def test_component_discovery(self):
        """Test that components are discovered and cached."""
        import sys
        interface = sys.modules['clicycle']

        # Clear cache to test discovery
        interface._component_cache.clear()
        interface._discover_components()

        # Should have discovered header
        assert 'header' in interface._component_cache
        assert 'clicycle.components.header' in interface._component_cache['header'][0]
        assert 'Header' in interface._component_cache['header'][1]

    @patch('clicycle.rendering.stream.RenderStream.render')
    def test_simple_component_wrapper(self, mock_render):
        """Test wrapper for simple components."""
        # Access a simple component like text (through info)
        cc.info("Test message")

        # Should have rendered an Info component
        mock_render.assert_called_once()
        component = mock_render.call_args[0][0]
        assert component.__class__.__name__ == 'Info'
        assert hasattr(component, 'message')
        assert component.message == "Test message"

    @patch('clicycle.rendering.stream.RenderStream.render')
    def test_context_manager_component(self, mock_render):
        """Test wrapper for context manager components."""
        # Spinner is a context manager
        spinner = cc.spinner("Loading...")

        # Should have rendered and returned the spinner object
        mock_render.assert_called_once()
        assert hasattr(spinner, '__enter__')
        assert hasattr(spinner, '__exit__')

    def test_special_function_json(self):
        """Test special json function."""
        with patch('clicycle.rendering.stream.RenderStream.render') as mock_render:
            cc.json({"key": "value"}, "Title")

            # Should render a Code component
            mock_render.assert_called_once()
            component = mock_render.call_args[0][0]
            assert component.__class__.__name__ == 'Code'

    def test_interactive_select(self):
        """Test interactive select is available."""
        assert hasattr(cc, 'select')
        # It should be the actual function
        from clicycle.interactive.select import interactive_select
        assert cc.select is interactive_select

    def test_interactive_multi_select(self):
        """Test interactive multi_select is available."""
        assert hasattr(cc, 'multi_select')
        # It should be the actual function
        from clicycle.interactive.multi_select import interactive_multi_select
        assert cc.multi_select is interactive_multi_select

    def test_multi_progress(self):
        """Test multi_progress returns a Progress object."""
        with (
            patch('clicycle.components.multi_progress.MultiProgress') as mock_mp_class,
            patch('clicycle.rendering.stream.RenderStream.render') as mock_render
        ):
            mock_mp_instance = MagicMock()
            mock_mp_class.return_value = mock_mp_instance

            result = cc.multi_progress("Processing tasks")

            # Should create and render MultiProgress component
            mock_mp_class.assert_called_once_with(cc._cli.theme, "Processing tasks", cc._cli.console)
            mock_render.assert_called_once_with(mock_mp_instance)

            # Should return the MultiProgress instance
            assert result is mock_mp_instance

    def test_attribute_error_for_unknown(self):
        """Test that unknown attributes raise AttributeError."""
        try:
            _ = cc.unknown_attribute
            raise AssertionError("Should have raised AttributeError")
        except AttributeError as e:
            assert "unknown_attribute" in str(e)

    def test_wrapper_function_names(self):
        """Test that wrapper functions have correct names."""
        # Access some components to create wrappers
        _ = cc.header
        _ = cc.section
        _ = cc.info

        # Check they have the right names
        assert cc.header.__name__ == 'header'
        assert cc.section.__name__ == 'section'
        assert cc.info.__name__ == 'info'

    def test_component_with_multiple_args(self):
        """Test components that take multiple arguments."""
        with patch('clicycle.rendering.stream.RenderStream.render') as mock_render:
            cc.header("Title", "Subtitle", "App")

            mock_render.assert_called_once()
            component = mock_render.call_args[0][0]
            assert component.title == "Title"
            assert component.subtitle == "Subtitle"
            assert component.app_name == "App"

    @patch('click.get_current_context')
    def test_debug_respects_verbose(self, mock_get_context):
        """Test debug component respects verbose mode."""
        # Test when verbose is False
        mock_ctx = MagicMock()
        mock_ctx.obj = {"verbose": False}
        mock_get_context.return_value = mock_ctx

        with patch('clicycle.components.text.Text.render') as mock_text_render:
            cc.debug("Debug message")
            # Debug component should not call parent's render when not verbose
            mock_text_render.assert_not_called()

        # Test when verbose is True
        mock_ctx.obj = {"verbose": True}

        with patch('clicycle.components.text.Text.render') as mock_text_render:
            cc.debug("Debug message in verbose")
            # Should call parent's render when verbose
            mock_text_render.assert_called_once()

    @patch('click.get_current_context')
    def test_debug_no_click_context(self, mock_get_context):
        """Test debug when no click context exists."""
        mock_get_context.side_effect = RuntimeError("No context")

        with patch('clicycle.components.text.Text.render') as mock_text_render:
            cc.debug("Debug without context")
            # Should not render when no context
            mock_text_render.assert_not_called()
