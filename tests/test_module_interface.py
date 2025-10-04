"""Tests for the module interface and convenience API."""

import sys
from unittest.mock import MagicMock, patch

import clicycle as cc
import clicycle.theme
from clicycle import _initialize_module_interface, _ModuleInterface


class TestModuleInterface:
    """Test the module interface wrapper."""

    def test_module_replacement(self):
        """Test that the module is replaced with _ModuleInterface."""
        assert isinstance(sys.modules["clicycle"], _ModuleInterface)

    def test_original_attributes_preserved(self):
        """Test that original module attributes are preserved."""
        # These should still exist
        assert hasattr(cc, "Clicycle")
        assert hasattr(cc, "Theme")
        assert hasattr(cc, "__version__")

    def test_cli_instance_created(self):
        """Test that _cli instance is created."""
        assert hasattr(cc, "_cli")
        assert isinstance(cc._cli, cc.Clicycle)

    def test_direct_attributes_available(self):
        """Test that direct attributes are available."""
        # Console is exposed via special attribute handler
        assert hasattr(cc, "console")
        assert cc.console is cc._cli.console

        # Theme exists but it's the module, not the instance
        # The theme module was imported and is a module attribute
        assert hasattr(cc, "theme")
        assert cc.theme is clicycle.theme

        # To get the CLI's theme instance:
        assert hasattr(cc._cli, "theme")
        assert isinstance(cc._cli.theme, cc.Theme)

    def test_clear_method(self):
        """Test clear method."""
        with patch.object(cc._cli, "clear") as mock_clear:
            cc.clear()
            mock_clear.assert_called_once()

    def test_configure_method(self):
        """Test configure method updates _cli."""
        new_theme = cc.Theme()
        cc.configure(width=120, theme=new_theme, app_name="Test")

        assert cc._cli.width == 120
        assert cc._cli.theme is new_theme
        assert cc._cli.app_name == "Test"
        # Note: cc._cli.console.width is determined by terminal size, not the width parameter
        # The width parameter controls rendering behavior, not console dimensions

    def test_component_discovery(self):
        """Test that components are discovered and cached."""
        interface = sys.modules["clicycle"]

        # Clear cache to test discovery
        interface._component_cache.clear()
        interface._discover_components()

        # Should have discovered header
        assert "header" in interface._component_cache
        assert "clicycle.components.header" in interface._component_cache["header"][0]
        assert "Header" in interface._component_cache["header"][1]

    @patch("clicycle.rendering.stream.RenderStream.render")
    def test_simple_component_wrapper(self, mock_render):
        """Test wrapper for simple components."""
        # Access a simple component like text (through info)
        cc.info("Test message")

        # Should have rendered an Info component
        mock_render.assert_called_once()
        component = mock_render.call_args[0][0]
        assert component.__class__.__name__ == "Info"
        assert hasattr(component, "message")
        assert component.message == "Test message"

    @patch("clicycle.rendering.stream.RenderStream.render")
    def test_context_manager_component(self, mock_render):
        """Test wrapper for context manager components."""
        # Spinner is a context manager
        spinner = cc.spinner("Loading...")

        # Should have rendered and returned the spinner object
        mock_render.assert_called_once()
        assert hasattr(spinner, "__enter__")
        assert hasattr(spinner, "__exit__")

    def test_special_function_json(self):
        """Test special json function."""
        with patch("clicycle.rendering.stream.RenderStream.render") as mock_render:
            cc.json({"key": "value"}, "Title")

            # Should render a Code component
            mock_render.assert_called_once()
            component = mock_render.call_args[0][0]
            assert component.__class__.__name__ == "Code"

    def test_interactive_select(self):
        """Test interactive select is available."""
        assert hasattr(cc, "select")
        # It should be the actual function
        from clicycle.interactive.select import interactive_select

        assert cc.select is interactive_select

    def test_interactive_multi_select(self):
        """Test interactive multi_select is available."""
        assert hasattr(cc, "multi_select")
        # It should be the actual function
        from clicycle.interactive.multi_select import interactive_multi_select

        assert cc.multi_select is interactive_multi_select

    def test_multi_progress(self):
        """Test multi_progress returns a Progress object."""
        with (
            patch("clicycle.components.multi_progress.MultiProgress") as mock_mp_class,
            patch("clicycle.rendering.stream.RenderStream.render") as mock_render,
        ):
            mock_mp_instance = MagicMock()
            mock_mp_class.return_value = mock_mp_instance

            result = cc.multi_progress("Processing tasks")

            # Should create and render MultiProgress component
            mock_mp_class.assert_called_once_with(
                cc._cli.theme, "Processing tasks", cc._cli.console
            )
            mock_render.assert_called_once_with(mock_mp_instance)

            # Should return the MultiProgress instance
            assert result is mock_mp_instance

    def test_multi_progress_function_creation(self):
        """Test that multi_progress function is created by __getattr__."""
        # Clear any cached function
        if hasattr(cc, "multi_progress"):
            delattr(cc, "multi_progress")

        # Access multi_progress to trigger __getattr__
        func = cc.multi_progress

        # Should be a callable function
        assert callable(func)
        assert func.__name__ == "multi_progress"

    def test_special_attributes(self):
        """Test access to special attributes that go through __getattr__."""
        # Test console attribute (handled by _handle_special_attribute)
        console = cc.console
        assert console is cc._cli.console

        # Test configure function (handled by _handle_special_attribute)
        configure_func = cc.configure
        assert callable(configure_func)

        # Test clear function (handled by _handle_special_attribute)
        clear_func = cc.clear
        assert callable(clear_func)

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
        assert cc.header.__name__ == "header"
        assert cc.section.__name__ == "section"
        assert cc.info.__name__ == "info"

    def test_component_with_multiple_args(self):
        """Test components that take multiple arguments."""
        with patch("clicycle.rendering.stream.RenderStream.render") as mock_render:
            cc.header("Title", "Subtitle", app_name="App")

            mock_render.assert_called_once()
            component = mock_render.call_args[0][0]
            assert component.title == "Title"
            assert component.subtitle == "Subtitle"
            assert component.app_name == "App"

    def test_header_app_name_injection(self):
        """Test that app_name is injected into headers when configured."""
        # Configure with app_name
        cc.configure(app_name="MyApp")

        with patch("clicycle.rendering.stream.RenderStream.render") as mock_render:
            # Create header without explicit app_name
            cc.header("Title", "Subtitle")

            mock_render.assert_called_once()
            component = mock_render.call_args[0][0]
            assert component.title == "Title"
            assert component.subtitle == "Subtitle"
            # Should have injected app_name from configuration
            assert component.app_name == "MyApp"

        # Test that explicit app_name overrides configured one
        with patch("clicycle.rendering.stream.RenderStream.render") as mock_render:
            cc.header("Title2", app_name="Override")

            mock_render.assert_called_once()
            component = mock_render.call_args[0][0]
            assert component.title == "Title2"
            assert (
                component.app_name == "Override"
            )  # Should use explicit, not configured

    def test_prompt_function(self):
        """Test prompt function wrapper."""
        assert hasattr(cc, "prompt")

        with (
            patch("clicycle.rendering.stream.RenderStream.render") as mock_render,
            patch("clicycle.components.prompt.Prompt.ask") as mock_ask,
        ):
            mock_ask.return_value = "test input"
            result = cc.prompt("Enter something")

            # Should have rendered the prompt component
            mock_render.assert_called_once()
            component = mock_render.call_args[0][0]
            assert component.__class__.__name__ == "Prompt"
            assert component.text == "Enter something"

            # Should return the result from ask()
            assert result == "test input"
            mock_ask.assert_called_once()

    def test_confirm_function(self):
        """Test confirm function wrapper."""
        assert hasattr(cc, "confirm")

        with (
            patch("clicycle.rendering.stream.RenderStream.render") as mock_render,
            patch("clicycle.components.prompt.Confirm.ask") as mock_ask,
        ):
            mock_ask.return_value = True
            result = cc.confirm("Are you sure?")

            # Should have rendered the confirm component
            mock_render.assert_called_once()
            component = mock_render.call_args[0][0]
            assert component.__class__.__name__ == "Confirm"
            assert component.text == "Are you sure?"

            # Should return the result from ask()
            assert result is True
            mock_ask.assert_called_once()

    def test_select_list_function(self):
        """Test select_list function wrapper."""
        assert hasattr(cc, "select_list")

        with (
            patch("clicycle.rendering.stream.RenderStream.render") as mock_render,
            patch("clicycle.components.prompt.SelectList.ask") as mock_ask,
        ):
            mock_ask.return_value = "option2"
            result = cc.select_list("item", ["option1", "option2", "option3"])

            # Should have rendered the select_list component
            mock_render.assert_called_once()
            component = mock_render.call_args[0][0]
            assert component.__class__.__name__ == "SelectList"
            assert component.item_name == "item"
            assert component.options == ["option1", "option2", "option3"]

            # Should return the result from ask()
            assert result == "option2"
            mock_ask.assert_called_once()

    def test_pyinstaller_fallback(self):
        """Test that module interface initialization returns correct value."""
        # Test the normal path (should return True)
        # The module is already initialized when clicycle imports
        # Just test that calling it again doesn't break
        result = _initialize_module_interface()
        assert isinstance(result, bool)  # Should return True or False

        # Verify that the module has the expected methods
        assert hasattr(cc, "header")
        assert hasattr(cc, "info")
        assert hasattr(cc, "success")
        assert hasattr(cc, "error")
