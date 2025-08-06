"""Clicycle - Component-based CLI rendering with automatic spacing."""

from __future__ import annotations

import inspect
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

from clicycle.clicycle import Clicycle
from clicycle.theme import (
    ComponentIndentation,
    ComponentSpacing,
    Icons,
    Layout,
    Theme,
    Typography,
)

__version__ = "2.1.2"

# Core exports
__all__ = [
    "Clicycle",
    "Theme",
    "Icons",
    "Typography",
    "Layout",
    "ComponentSpacing",
    "ComponentIndentation",
]


class _ModuleInterface(ModuleType):
    """Module wrapper that provides convenience API."""

    def __init__(self, module: ModuleType) -> None:
        self.__dict__.update(module.__dict__)
        self._cli = Clicycle()
        self._component_cache: dict[str, tuple[str, str]] = {}
        self._discover_components()

    def _discover_components(self) -> None:
        """Discover all components in the components directory."""
        components_dir = Path(__file__).parent / "components"

        for py_file in components_dir.glob("*.py"):
            if py_file.name.startswith("_") or py_file.name == "base.py":
                continue

            module_name = f"clicycle.components.{py_file.stem}"
            module = __import__(module_name, fromlist=["*"])

            # Find all classes that inherit from Component
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if hasattr(obj, "component_type") and obj.__module__ == module_name:
                    # Skip interactive components that need ask()
                    if hasattr(obj, "ask"):
                        continue
                    # Use component_type as the convenience name
                    self._component_cache[obj.component_type] = (module_name, name)

    def __getattr__(self, name: str) -> Any:
        """Get attribute from module, component cache, or special handlers."""
        # Dispatch to handlers
        for handler in [
            self._handle_special_attribute,
            self._handle_cached_component,
            self._handle_special_function,
        ]:
            # The sentinel is used to distinguish from a handler returning None
            sentinel = object()
            result = handler(name, sentinel)
            if result is not sentinel:
                return result

        raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

    def _handle_special_attribute(self, name: str, sentinel: object) -> Any:
        """Handle special attributes like 'console', 'theme', etc."""
        if name == "console":
            return self._cli.console
        if name == "theme":
            return self._cli.theme
        if name == "configure":

            def configure(**kwargs: Any) -> None:
                self._cli = Clicycle(**kwargs)

            return configure
        if name == "clear":
            return self._cli.clear
        return sentinel

    def _handle_cached_component(self, name: str, sentinel: object) -> Any:
        """Handle components that are in the cache."""
        if name not in self._component_cache:
            return sentinel

        module_name, class_name = self._component_cache[name]
        module = __import__(module_name, fromlist=[class_name])
        component_class = getattr(module, class_name)

        # Create wrapper function based on component type
        if hasattr(component_class, "__enter__"):
            # Context managers need console
            def context_wrapper(message: str) -> Any:
                obj = component_class(self._cli.theme, message, self._cli.console)
                self._cli.stream.render(obj)
                return obj
            wrapper = context_wrapper
        else:
            # Regular components
            def regular_wrapper(*args: Any, **kwargs: Any) -> None:
                obj = component_class(self._cli.theme, *args, **kwargs)
                self._cli.stream.render(obj)
            wrapper = regular_wrapper

        wrapper.__name__ = name
        wrapper.__doc__ = f"Display {name.replace('_', ' ')}."

        # Cache and return
        setattr(self, name, wrapper)
        return wrapper

    def _handle_special_function(self, name: str, sentinel: object) -> Any:
        """Handle special functions that are not auto-discovered."""
        if name == "json":
            from clicycle.components.code import json_code

            def json_wrapper(data: Any, title: str | None = None) -> None:
                self._cli.stream.render(json_code(self._cli.theme, data, title))

            setattr(self, name, json_wrapper)
            return json_wrapper

        # Interactive components
        if name == "select":
            from clicycle.interactive.select import interactive_select

            setattr(self, name, interactive_select)
            return interactive_select

        if name == "multi_select":
            from clicycle.interactive.multi_select import interactive_multi_select

            setattr(self, name, interactive_multi_select)
            return interactive_multi_select

        # Special handling for multi_progress that returns Progress object
        if name == "multi_progress":
            from clicycle.components.multi_progress import MultiProgress

            def multi_progress_wrapper(description: str = "Processing") -> Any:
                obj = MultiProgress(self._cli.theme, description, self._cli.console)
                self._cli.stream.render(obj)
                return obj

            setattr(self, name, multi_progress_wrapper)
            return multi_progress_wrapper

        # Group context manager
        if name == "group":
            def group_wrapper() -> Any:
                return self._cli.group()

            setattr(self, name, group_wrapper)
            return group_wrapper

        return sentinel


# Replace this module with our wrapper
sys.modules[__name__] = _ModuleInterface(sys.modules[__name__])
