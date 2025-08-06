# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2025-01-06

**Added:**

- `multi_progress()` context manager for tracking multiple concurrent tasks
- `group()` context manager for rendering components without spacing (formerly `block()`)
- New `modifiers` module for non-component rendering modifiers
- Dedicated example for demonstrating group functionality (`examples/features/groups.py`)
- Multi-task progress tracking in all_components example

**Fixed:**

- Progress bar context manager now properly handles updates
- Menu example no longer displays ANSI codes when arrow keys are pressed after "Press Enter to continue"
- All linting issues resolved (ruff and mypy clean)

**Changed:**

- Refactored menu.py to reduce complexity by extracting helper functions
- Improved code organization with separate `modifiers` directory

## [2.0.2] - 2025-01-05

**Fixed:**

- Updated PyPI version badge to use shields.io instead of badge.fury.io for better reliability
- Badge now correctly shows the latest PyPI version without caching delays

## [2.0.1] - 2025-01-05

**Fixed:**

- Added comprehensive type annotations for mypy strict mode compliance
- Fixed type compatibility issues in prompt and interactive components
- Updated all `__exit__` methods to use `Literal[False]` return type
- Fixed module import approach in interactive components to avoid attribute errors
- Ensured all components pass mypy strict mode checks

**Changed:**

- Updated test assertions to match new type annotation behavior

## [2.0.0] - 2025-01-05

**Added:**

- Component-based architecture with automatic spacing management
- Interactive components with arrow-key navigation (`select` and `multi_select`)
- Disappearing spinners feature with `disappearing_spinners` theme option
- Convenient module-level API (`import clicycle as cc`)
- Debug component that respects Click's verbose mode
- Comprehensive test suite with 96% coverage
- Full type hints throughout the codebase
- Python 3.11+ support

**Changed:**

- Complete architectural refactor from monolithic to component-based design
- Moved from class-based to function-based API for better ergonomics
- Components now self-manage spacing based on theme rules
- Spinners now properly handle transient display when disappearing
- Improved Rich integration with better theme customization
- Updated minimum Python version from 3.10 to 3.11

**Fixed:**

- Double messaging issue with spinners
- Spacing issues between components
- Interactive menu display issues across different terminals
- Test coverage gaps and import errors

**Removed:**

- Legacy monolithic `core.py` module
- Old class-based API (though Clicycle class still available for advanced use)
- Python 3.10 support

## [1.0.0] - 2024-12-12

**Added:**

- Initial release
- Basic CLI rendering with Rich styling
- Header, section, and text components
- Progress bars and spinners
- Table and summary components
- Theme system with customizable icons and colors
