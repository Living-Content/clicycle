# Release Notes - v2.0.1

## Type Annotation Fixes

This patch release addresses type annotation issues discovered after the v2.0.0 release.

### What's Fixed

- **Full mypy strict mode compliance**: All functions and methods now have proper type annotations
- **Fixed `__exit__` methods**: Updated to use `Literal[False]` return type as required by mypy
- **Interactive component imports**: Fixed module import approach to avoid attribute errors
- **Test compatibility**: Updated tests to match new type annotation behavior

### Installation

```bash
pip install --upgrade clicycle
```

### Notes

This is a patch release with no breaking changes. All v2.0.0 code will continue to work without modification.